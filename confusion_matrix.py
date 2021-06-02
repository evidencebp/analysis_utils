"""
    Implements a confusion matrix.
    For details see https://en.wikipedia.org/wiki/Confusion_matrix
"""
import json
import math
from pandas import DataFrame

def ifnull(var, val=0):
  if var is None:
    return val

  return var

def safe_divide(numerator, divisor, default=None):
    if divisor != 0 and divisor is not None:
        return ifnull(numerator)/ifnull(divisor)
    else:
        return default

def sk_to_grouped_df(labels
                     , predictions
                     , classifier='classifier'
                     , concept='concept'
                     , count='count'
                     ):
    dict = {concept: labels
            , classifier : predictions}
    df = DataFrame(dict)
    df = df.reset_index()
    grouped_df = group_df_for_cm(df
                                 , classifier
                                 , concept
                                 , count)

    return grouped_df

BINARY_BASE = 2

def entropy(probability):
    ent = 0
    if probability not in (0, 1):
        ent = -(probability*math.log(probability, BINARY_BASE)
                + (1 -probability)*math.log((1 -probability), BINARY_BASE))

    return ent

def pointwise_mutual_information(joint_prob
                                 , ind_prob):
    pointwise = 0.0

    if (joint_prob is not None
            and joint_prob > 0.0
            and ind_prob is not None
            and ind_prob > 0.0):
        pointwise = joint_prob * math.log(joint_prob / ind_prob, BINARY_BASE)

    return pointwise


def group_df_for_cm(df
                    , classifier
                    , concept
                    , count='count'):
    grouped_df = df.groupby([concept, classifier], as_index=False).agg({'index': 'count'})
    grouped_df = grouped_df.rename(columns={'index': count})

    return grouped_df


class ConfusionMatrix(object):
    def __init__(self
                 , classifier
                 , concept
                 , count=None
                 , g_df=None
                 , comment=None
                 , digits=2):

        COUNT_COLUMN = 'count'

        self.classifier = classifier
        self.concept = concept
        self.count = count
        self.comment = comment
        self.digits = digits

        # The be extended to enable many initialzations
        # Using a raw dataframe, sk-learn parameters, confusion matrix values
        if g_df is not None:
            self.g_df = g_df
            if self.count is None:
                self.count = COUNT_COLUMN
                self.g_df[self.count] = 1

    def tp(self):
        """
            Return True Positives (TP)
        """
        tp = 0
        if  len(self.g_df[(self.g_df[self.classifier] == True) & (self.g_df[self.concept] == True)]) == 1:
            tp = self.g_df[(self.g_df[self.classifier] == True)
                           & (self.g_df[self.concept] == True)].iloc[0][self.count]

        return tp

    def tn(self):
        """
            Return True Negatives (TN)
        """
        tn = 0
        if  len(self.g_df[(self.g_df[self.classifier] == False) & (self.g_df[self.concept] == False)]) == 1:
            tn = self.g_df[(self.g_df[self.classifier] == False)
                           & (self.g_df[self.concept] == False)].iloc[0][self.count]

        return tn

    def fp(self):
        """
            Return False Positives (FP)
        """
        fp = 0
        if  len(self.g_df[(self.g_df[self.classifier] == True) & (self.g_df[self.concept] == False)]) == 1:
            fp = self.g_df[(self.g_df[self.classifier] == True)
                           & (self.g_df[self.concept] == False)].iloc[0][self.count]

        return fp

    def fn(self):
        """
            Return False Negatives (FN)
        """
        fn = 0
        if  len(self.g_df[(self.g_df[self.classifier] == False) & (self.g_df[self.concept] == True)]) == 1:
            fn = self.g_df[(self.g_df[self.classifier] == False)
                           & (self.g_df[self.concept] == True)].iloc[0][self.count]

        return fn

    def positives(self):
        return (ifnull(self.tp()) + ifnull(self.fn()))

    def positive_rate(self):
        return safe_divide(ifnull(self.positives()), ifnull(self.samples()))

    def negatives(self):
        return (ifnull(self.tn()) + ifnull(self.fp()))

    def hits(self):
        return (ifnull(self.tp()) + ifnull(self.fp()))

    def hit_rate(self):
        return safe_divide(ifnull(self.hits()), ifnull(self.samples()))

    def precision(self):
        return safe_divide(self.tp(), self.hits())

    def precision_lift(self):
        return ifnull(safe_divide(ifnull(self.precision()), self.positive_rate())) - 1.0

    def recall(self):
        return safe_divide(self.tp(), self.positives())

    def samples(self):
        return self.positives() + self.negatives()

    def accuracy(self):
        return safe_divide(self.tp() + self.tn(), self.samples())

    def fpr(self):
        """
            False Positive Rate
        :return:
        """
        return safe_divide(self.fp() , self.negatives())

    def jaccard(self):
        return safe_divide(self.tp() , self.tp() + self.fp() + self.fn())

    def independent_prob(self):
        return (ifnull(self.positive_rate())*ifnull(self.hit_rate())) +  ((1- ifnull(self.positive_rate()))*(1-ifnull(self.hit_rate())))

    def lift_over_independent(self):
        return ifnull(self.accuracy())/self.independent_prob() -1

    def lift_over_majority(self):
        majority = max(ifnull(self.positive_rate()), 1 - ifnull(self.positive_rate()))
        return ifnull(self.accuracy())/majority -1

    def concept_entropy(self):
        return entropy(ifnull(self.positive_rate()))

    def classifier_entropy(self):
        return entropy(ifnull(self.hit_rate()))

    def mutual_information(self):
        mu = 0

        # True positives
        joint_prob = safe_divide(self.tp(),self.samples())
        ind_prob = ifnull(self.positive_rate())*ifnull(self.hit_rate())
        point_wise = pointwise_mutual_information(joint_prob
                                 , ind_prob)
        mu += point_wise

        # False positives
        joint_prob = self.fp()/self.samples()
        ind_prob = (1 - self.positive_rate())*self.hit_rate()
        point_wise = pointwise_mutual_information(joint_prob
                                 , ind_prob)
        mu += point_wise

        # False negatives
        joint_prob = self.fn()/self.samples()
        ind_prob = self.positive_rate()*(1 - self.hit_rate())
        point_wise = pointwise_mutual_information(joint_prob
                                 , ind_prob)
        mu += point_wise

        # True negatives
        joint_prob = self.tn()/self.samples()
        ind_prob = (1 - self.positive_rate())*(1 - self.hit_rate())
        point_wise = pointwise_mutual_information(ifnull(joint_prob)
                                 , ifnull(ind_prob))
        mu += point_wise

        return mu

    def summarize(self
                  , output_file=None):

        sum_dict = {'true_positives' : int(self.tp())
                , 'true_negatives' : int(self.tn())
                , 'false_positives' : int(self.fp())
                , 'false_negatives' : int(self.fn())
                , 'samples' : int(self.samples())
                , 'accuracy' : round(ifnull(self.accuracy()), self.digits)
                , 'positive_rate' : round(ifnull(self.positive_rate()), self.digits)
                , 'hit_rate' : round(ifnull(self.hit_rate()), self.digits)
                , 'precision' : round(ifnull(self.precision()), self.digits)
                , 'precision_lift' : round(ifnull(self.precision_lift()), self.digits)
                , 'recall' : round(ifnull(self.recall()), self.digits)
                , 'fpr' : round(ifnull(self.fpr()), self.digits)
                , 'jaccard' : round(ifnull(self.jaccard()), self.digits)
                , 'independent_prob' : round(ifnull(self.independent_prob()), self.digits)
                , 'lift_over_independent' : round(ifnull(self.lift_over_independent()), self.digits)
                , 'lift_over_majority' : round(ifnull(self.lift_over_majority()), self.digits)
                , 'concept_entropy': round(ifnull(self.concept_entropy()), self.digits)
                , 'classifier_entropy': round(ifnull(self.classifier_entropy()), self.digits)
                , 'mutual_information': round(ifnull(self.mutual_information()), self.digits)

            , 'comment' : self.comment
                }

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(sum_dict, f, ensure_ascii=False, indent=4)

        return sum_dict

    def to_latex(self
                 , caption):

        print(r"\begin {table}[h!]\centering")
        print(r"\caption{", caption, "}")
        print(r"\begin {tabular} { | l | l | l |}")
        print(r"\hline")
        print(r"		&\multicolumn{2}{c|}{Classification}		  \\ \cline{2-3}")
        print(r"Concept & True(Corrective) & False              \\ \hline")
        print(r"True & ", self.tp(), "(", round(100*self.tp()/self.samples(), self.digits) ,"\% ) TP")
        print(r"& ", self.fn(), "(", round(100*self.fn()/self.samples(), self.digits) ,r"\% ) FN      \\ \hline")
        print(r"False & ", self.fp(), "(" , round(100*self.fp()/self.samples(), self.digits) ,r"\% ) FP")
        print(r"& ", self.tn(),  "(" , round(100*self.tn()/self.samples(), self.digits) ,r"\% ) TN \\ \hline")
        print(r"\end {tabular}")
        print(r"\end {table}")
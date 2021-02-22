"""

Implementing the self supervised algorithm of
https://patents.google.com/patent/US20190164086A1/en
(Patent is for the application of the algorithm in the cyber-security domain).

The algorithm look for a set of parameters that will maximize classifiers agreement, with the absence of labels.

The classifiers are aggregated by some family, in this case Logistic regression.
Since we don't have labels, we cannot train the model.
Instead we inject the parameters into the model and use grid search to find the parameters that maximize agreement.
Agreement is measured using the some of the entropy of the confidence.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
#from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils.extmath import cartesian
from sklearn.utils.validation import check_X_y
from sklearn.model_selection import GridSearchCV

from confusion_matrix import entropy

def confidence_entropy(y, y_pred, **kwargs):
    ent = [entropy(i) for i in y_pred]

    return sum(ent)


from sklearn.metrics import make_scorer

# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html#sklearn.metrics.make_scorer
ent_scorer = make_scorer(confidence_entropy
                         , greater_is_better=False
                         , needs_proba=True)

class FixedLogisticRegression(LogisticRegression):
    """
        Based on https://scikit-learn.org/stable/developers/develop.html
    """
    def __init__(self
                 , fixed_intercept=None
                 , fixed_coef=None
                 , fixed_classes=None
                 , multi_class='auto'):
        self.fixed_intercept = fixed_intercept
        self.fixed_coef = fixed_coef
        self.fixed_classes = fixed_classes
        self.multi_class = multi_class

    def fit(self, X, y):
        """A reference implementation of a fitting function.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,) or (n_samples, n_outputs)
            The target values (class labels in classification, real numbers in
            regression).

        Returns
        -------
        self : object
            Returns self.
        """
        X, y = check_X_y(X, y, accept_sparse=True)
        self.is_fitted_ = True
        self.set_params(fixed_intercept=self.fixed_intercept
                            , fixed_coef=self.fixed_coef
                            , fixed_classes=self.fixed_classes)

        return self

    def set_params(self
                   , **params):

        INTERCEPT = 'fixed_intercept'
        COEF = 'fixed_coef'
        CLASSES = 'fixed_classes'
        fixed_parameters = [INTERCEPT, COEF, CLASSES]
        if not params:
            return self

        original_params = params.copy()
        super_params = params

        for i in fixed_parameters:
            super_params.pop(i, None)
        super().set_params(**super_params)

        if INTERCEPT in original_params and (original_params[INTERCEPT] is not None):
            self.intercept_ = original_params[INTERCEPT]

        if COEF in original_params and (original_params[COEF] is not None):
            self.coef_ = original_params[COEF]
        if CLASSES in original_params and (original_params[CLASSES] is not None):
            self.classes_ = original_params[CLASSES]

        return self

def generate_logistic_parameters(features_num
                                 , step_size=0.2
                                 , min_val=-1.0
                                 , max_val=1.0
                                 , digits=1
                                 , items_as_np=True
                                 , include_zero=False):
    """
       i = round(max_val, digits)
        while i <= min_val:
            if include_zero or i != 0:
                feature_values.append(i)
            i -= step_size
            i = round(i ,digits)

    """

    feature_values = []

    i = round(max_val,digits)
    while i >= min_val:
         if include_zero or i != 0:
             feature_values.append(i)
         i -= step_size
         i = round(i ,digits)

    feature_values = np.array(feature_values)
    features = (feature_values for _ in range(features_num))
    grid = cartesian(features)

    if items_as_np:
        grid = [np.array(i) for i in grid]

    return grid


def generate_logistic_classifier_parameters(features_num
                                 , step_size=0.2
                                 , min_val=-1.0
                                 , max_val=1.0
                                 , digits=1
                                 , items_as_np=True
                                 , include_zero=False):

    fixed_intercept = generate_logistic_parameters(1
                                                   , step_size=step_size
                                                   , min_val=min_val
                                                   , max_val=max_val
                                                   , digits=digits
                                                   , items_as_np=items_as_np
                                                   , include_zero=include_zero
                                                   )
    fixed_coef = generate_logistic_parameters(features_num
                                              , step_size=step_size
                                              , min_val=min_val
                                              , max_val=max_val
                                              , digits=digits
                                              , include_zero=include_zero
                                              , items_as_np=False
                                              )

    fixed_coef = [np.array([x]) for x in fixed_coef]
    parameters = {'fixed_intercept': fixed_intercept
        , 'fixed_coef': fixed_coef
        , 'fixed_classes': [np.array([0, 1])]
                  }

    return parameters

def minimize_classifiers_entropy(X
                                 , step_size=0.2
                                 , min_val=-1.0
                                 , max_val=1.0
                                 , digits=1
                                 , include_zero=False
                                 , verbose=0
                                 ):
    y = [0]*len(X)
    features_num = len(X[0])

    parameters = generate_logistic_classifier_parameters(features_num
                                 , step_size=step_size
                                 , min_val=min_val
                                 , max_val=max_val
                                 , digits=digits
                                 , items_as_np=True
                                 , include_zero=include_zero)

    gs_clf = GridSearchCV(FixedLogisticRegression()
                          , parameters
                          , scoring=ent_scorer
                          , verbose=verbose
                          )
    gs_clf.fit(X, y)

    return gs_clf.best_params_


"""
from sklearn.datasets import load_breast_cancer

X, y = load_breast_cancer(return_X_y=True)

features_num = 3
idx_IN_columns = range(features_num)
X = X[:,idx_IN_columns]

clf = LogisticRegression(random_state=0
                         , multi_class='auto').fit(X, y)
clf.predict(X[:2, :])

clf.predict_proba(X[:2, :])


clf.score(X, y)
print(clf)


print(minimize_classifiers_entropy(X
                                 , step_size=0.2
                                 , min_val=-1.0
                                 , max_val=1.0
                                 , digits=1
                                 , include_zero=False
                                 ))

"""

"""
                  generate_logistic_parameters(1
                                 , step_size=0.5
                                 , min_val=-1.0
                                 , max_val=1.0
                                 , digits=1
                                 , include_zero=False)


parameters = {'fixed_intercept': [-1.0, 0.0, 1.0]
    , 'fixed_coef': generate_logistic_parameters(features_num
                                 , step_size=0.5
                                 , min_val=-1.0
                                 , max_val=1.0
                                 , digits=1
                                 , include_zero=False)
              }

"""


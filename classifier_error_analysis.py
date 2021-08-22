"""
    While metrics give overall performance of a classifier, there is interest in finding where
    the classifier perform better or worse.
    In order to find out, we apply machine learning again, this time trying to predict were the classifier
    will make mistakes.
    Success in finding such areas can help boost the performance.
    Not being able to do that means that the classifier doesn't have a specific weak area.
"""

from functools import partial
import pandas as pd

from ml_utils import get_predictive_columns, build_and_eval_model

def classification_mistake_function(record
                                   , prediction_column
                                   , concept_column):
    return record[prediction_column] != record[concept_column]

def regression_too_far_mistake_function(record
                                   , prediction_column
                                   , concept_column
                                   , threshold=0.25):

    if record[concept_column] == 0.0:
        if record[prediction_column] == 0.0:
            threshold_rel_diff =False
        else:
            threshold_rel_diff = None
    else:
        rel_diff = record[prediction_column]/record[concept_column]
        threshold_rel_diff = rel_diff < (1 - threshold) or rel_diff > (1 + threshold)

    return threshold_rel_diff

def classifier_error_analysis(df: pd.DataFrame
                                , error_classifier
                                , excluded_features
                                , concept_column: str
                                , filtering_function=None
                                , allow_concept_usage: bool = False
                                , prediction_column: str = 'prediction_column'
                                , allow_prediction_usage: bool = False
                                , incorrect_prediction_column: str = 'incorrect_prediction_column'
                                , test_size=0.2
                                , random_state=1
                                , mistake_function=classification_mistake_function
                              ):
    """

    :param df: A dataframe containing the base classifier prediction, the concept and the needed features.
    :param filtering_function: A function used to focus areas of error analysis. Examples are, just positives
    , just hits, and of course True, meaning analysing all the data.
    :param error_classifier: The classifier to use to characterize the errors of the base classifier
    :param excluded_features: Feature to exclude from analysis (e.g., keys)
    :param concept_column: The concept that the base classifier tries to predict.
    :param allow_concept_usage: Can the concept be used as a feature in the error analysis?
    :param prediction_column: The column storing the base classifier's predictions.
    :param allow_prediction_usage: Can the prediction be used as a feature in the error analysis?
    :param incorrect_prediction_column: name of the correct prediction column
    :param test_size: Test size for evaluation
    :param random_state: Random state for model fit and evaluation
    :return:
    """

    scope_column = 'in_scope'

    df['incorrect_prediction_column'] = df.apply(lambda x: 1 if mistake_function(x
                                                                                           , prediction_column
                                                                                           , concept_column) else 0
                                               , axis=1)
    df = df.rename(columns={'incorrect_prediction_column' : incorrect_prediction_column})
    df[incorrect_prediction_column] = df[incorrect_prediction_column].astype('int')
    if filtering_function:
        df[scope_column] = df.apply(lambda x: filtering_function(x)
                                    , axis=1)
        df = df[df[scope_column] ==1]
        df = df.drop(columns=[scope_column])

    error_excluded_features = excluded_features
    if not allow_concept_usage:
        error_excluded_features = set(list(error_excluded_features) + [concept_column])
    if not allow_prediction_usage:
        error_excluded_features = set(list(error_excluded_features) + [prediction_column])

    error_excluded_features = set(list(error_excluded_features) + [incorrect_prediction_column])
    error_get_predictive_columns = partial(get_predictive_columns
                                             , excluded_features=set(error_excluded_features))
    #print("error_excluded_features", error_excluded_features)
    #print("used features", error_get_predictive_columns(df))
    classifier, performance = build_and_eval_model(df=df
                         , classifier=error_classifier
                         , concept=incorrect_prediction_column
                         , test_size=test_size
                         , random_state=random_state
                         , get_predictive_columns_func=error_get_predictive_columns
                         , performance_file=None
                         )

    return classifier, performance


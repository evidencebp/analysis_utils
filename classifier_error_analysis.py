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

def classifier_error_analysis(df: pd.DataFrame
                                , filtering_function
                                , error_classifier
                                , excluded_features
                                , concept_column: str
                                , allow_concept_usage: bool = False
                                , prediction_column: str = 'prediction_column'
                                , allow_prediction_usage: bool = False
                                , correct_prediction_column: str = 'correct_prediction_column'
                                , test_size=0.2
                                , random_state=1
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
    :param correct_prediction_column: name of the correct prediction column
    :param test_size: Test size for evaluation
    :param random_state: Random state for model fit and evaluation
    :return:
    """
    
    scope_column = 'in_scope'

    error_excluded_features = excluded_features
    if not allow_concept_usage:
        error_excluded_features = set(list(error_excluded_features) + [concept_column])
    if not allow_prediction_usage:
        error_excluded_features = set(list(error_excluded_features) + [prediction_column])

    error_get_predictive_columns = partial(get_predictive_columns
                                             , excluded_features=set(error_excluded_features))


    df['correct_prediction_column'] = df.apply(lambda x: x[prediction_column] == x[concept_column]
                                               , axis=1)
    df = df.rename(columns={'correct_prediction_column' : correct_prediction_column})

    df[scope_column] = df.apply(lambda x: filtering_function(x)
                                , axis=1)
    df = df[df[scope_column]]
    df = df.drop(columns=[scope_column])

    classifier, performance = build_and_eval_model(df=df
                         , classifier=error_classifier
                         , concept=correct_prediction_column
                         , test_size=test_size
                         , random_state=random_state
                         , get_predictive_columns_func=error_get_predictive_columns
                         , performance_file=None
                         )

    return classifier, performance


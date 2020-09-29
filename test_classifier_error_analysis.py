"""
Test classifier_error_analysis
"""
import pandas as pd
import pytest
from sklearn.tree import DecisionTreeClassifier

from classifier_error_analysis import classifier_error_analysis

TEST_SIZE = 0.2
RANDOM_STATE = 123

@pytest.mark.parametrize(('df'
                                , 'filtering_function'
                                , 'error_classifier'
                                , 'excluded_features'
                                , 'concept_column'
                                , 'allow_concept_usage'
                                , 'prediction_column'
                                , 'allow_prediction_usage'
                                , 'expected')
    , [
pytest.param(
    pd.DataFrame( [
        [0, 1, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 1, 1, 0],
        ]
        , columns=['a1', 'a2', 'always_wrong', 'prediction', 'concept'])
     , lambda x: True
     , DecisionTreeClassifier(random_state=RANDOM_STATE)
    , set([])
    , 'concept'
    , False
    , 'prediction'
    , False
    , 1.0
            , id='reg1')
                         ])
def test_classifier_error_analysis(df
                                , filtering_function
                                , error_classifier
                                , excluded_features
                                , concept_column
                                , allow_concept_usage
                                , prediction_column
                                , allow_prediction_usage
                                , expected
                                ):
    """

    :param first_df:
    :param second_df:
    :param concept_column:
    :param expected:
        The indices are different and therefore removed before comparision.
        assert_frame_equal is used instead of assert in order to compare data frames.
    :return:
    """
    #classifier = DecisionTreeClassifier(random_state=random_state)
    classifier, performance = classifier_error_analysis(df=df
                                , filtering_function=filtering_function
                                , error_classifier=error_classifier
                                , excluded_features=excluded_features
                                , concept_column=concept_column
                                , allow_concept_usage=allow_concept_usage
                                , prediction_column=prediction_column
                                , allow_prediction_usage=allow_prediction_usage
                               )

    assert performance['accuracy'] == expected

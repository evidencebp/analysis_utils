"""
    Testing build_comparison_dataset
"""
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
from sklearn.tree import DecisionTreeClassifier

from compare_datasets import build_comparison_dataset, compare_datasets

TEST_SIZE = 0.2
RANDOM_STATE = 123


@pytest.mark.parametrize(('first_df'
                            , 'second_df'
                            , 'concept_column'
                            , 'expected')
    , [
pytest.param(
    pd.DataFrame( [
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0]
        ]
        , columns=['a1', 'a2', 'a3', 'b1', 'b2'])
    , pd.DataFrame([
         [2, 1, 1, 0, 0],
         [2, 0, 1, 0, 0],
         [2, 0, 0, 0, 0],
         [2, 0, 0, 0, 1],
         [2, 0, 0, 0, 0]
        ]
         , columns=['a1', 'a2', 'a3', 'b1', 'b2'])
    , 'who_is_in_the_first'
    , pd.DataFrame([
        [0, 1, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 1],
        [2, 1, 1, 0, 0, 0],
        [2, 0, 1, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 1, 0],
        [2, 0, 0, 0, 0, 0]
    ]
        , columns=['a1', 'a2', 'a3', 'b1', 'b2', 'who_is_in_the_first'])

            , id='reg1')
                         ])
def test_build_comparison_dataset(first_df
                             , second_df
                             , concept_column
                            , expected):
    """

    :param first_df:
    :param second_df:
    :param concept_column:
    :param expected:
        The indices are different and therefore removed before comparision.
        assert_frame_equal is used instead of assert in order to compare data frames.
    :return:
    """

    actual = build_comparison_dataset(first_df
                             , second_df
                             , concept_column)

    assert_frame_equal(actual.reset_index(drop=True)
                       , expected.reset_index(drop=True))


@pytest.mark.parametrize(('first_df'
                             , 'second_df'
                             , 'classifier'
                             , 'excluded_features'
                             , 'test_size'
                             , 'random_state'
                             , 'expected')
    , [
pytest.param(
    pd.DataFrame( [
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0]
        ]
        , columns=['a1', 'a2', 'a3', 'b1', 'b2'])
    , pd.DataFrame([
         [2, 1, 1, 0, 0],
         [2, 0, 1, 0, 0],
         [2, 0, 0, 0, 0],
         [2, 0, 0, 0, 1],
         [2, 0, 0, 0, 0]
        ]
         , columns=['a1', 'a2', 'a3', 'b1', 'b2'])
    , DecisionTreeClassifier(random_state=RANDOM_STATE)
    , set(['b2'])
    , TEST_SIZE
    , RANDOM_STATE
    , 1.0
            , id='reg1')
                         ])
def test_compare_datasets(first_df
                             , second_df
                             , classifier
                             , excluded_features
                             , test_size
                             , random_state
                             , expected):
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
    classifier, performance = compare_datasets(first_df=first_df
                             , second_df=second_df
                             , classifier=classifier
                             , excluded_features=excluded_features
                             , test_size=test_size
                             , random_state=random_state)

    assert performance['accuracy'] == expected

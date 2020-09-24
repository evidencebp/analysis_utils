"""
    Testing build_comparison_dataset
"""
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from build_comparison_dataset import build_comparison_dataset

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

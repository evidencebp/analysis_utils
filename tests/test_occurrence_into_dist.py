"""
    Testing occurrence_into_dist
"""
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from occurrence_into_dist import occurrence_into_dist

@pytest.mark.parametrize(('df'
                         , 'group_column'
                            , 'expected')
    , [
pytest.param(
    pd.DataFrame( [
        [1, 25],
        [2, 15],
        [3, 5],
        [4, 3],
        [5, 2],
        ]
        , columns=['f', 'cnt'])
    , 'f'
    , pd.DataFrame([
        [1, 25, 0.5, 0.5],
        [2, 15, 0.3, 0.8],
        [3, 5, 0.1, 0.9],
        [4, 3, 0.06, 0.96],
        [5, 2, 0.04, 1.0],
    ]
         , columns=['f', 'cnt', 'probability', 'agg_probability'])
            , id='reg1')
                         ])
def test_occurrence_into_dist(df
                         , group_column
                            , expected):

    actual = occurrence_into_dist(df
                         , group_column)

    assert_frame_equal(actual.reset_index(drop=True)
                       , expected.reset_index(drop=True))

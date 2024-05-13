import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from analysis_utils.relative_mean import analyze_relative_mean, StringsList

@pytest.mark.parametrize(('df'
                            , 'concepts'
                            , 'metrics'
                            , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [True, False, 4.0, 10.0]
                , [False, True, 15.0, 5.0]
                , [False, True, 5.0, 15.0]
            ], columns=['m1', 'm2', 'c1', 'c2'])
            , ['c1', 'c2']
            , ['m1', 'm2']
            , pd.DataFrame([
                    ['m1', 4.0, -4.0, 10.0, 0.0]
                     , ['m2', 10.0, 2.0, 10.0, 0.0]
    ], columns=['feature', 'cond_mean_c1', 'cond_mean_diff_c1', 'cond_mean_c2', 'cond_mean_diff_c2'])

, id='reg1')
                         ])
def test_analyze_correlation(df: pd.DataFrame
                          , concepts: StringsList
                          , metrics: StringsList
                                , expected):

    actual = analyze_relative_mean(df
                          , concepts
                          , metrics)

    assert_frame_equal(actual.reset_index(drop=True)
                       , expected.reset_index(drop=True))



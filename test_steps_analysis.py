import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from steps_analysis import build_two_steps_ds

@pytest.mark.parametrize(('metric_per_year_df'
                             , 'keys'
                             , 'metrics'
                                , 'expected'
                            , 'expected')
    , [
pytest.param(

    pd.DataFrame([(2021, 'a', 200, 150)
                     , (2020, 'a', 100, 50)
                     , (2019, 'a', 50, 50)
                     , (2019, 'b', 100, 50)
                     , (2018, 'b', 50, 50)
                     , (2019, 'c', 100, 50)
                     , (2018, 'b', None, 0)
                  ]
        , columns=['year', 'repo_name', 'commits', 'authors'])
        ,keys= ['repo_name']
        ,metrics = ['commits', 'authors']

, id='reg1')
                         ])
def test_analyze_correlation(metric_per_year_df
                             , keys
                             , metrics
                             , expected):


    actual = build_two_steps_ds(metric_per_year_df
                               , keys
                               , metrics
                               , time_column='year'
                               , minimal_time=-1
                               , control_variables=[])


    assert_frame_equal(actual.reset_index(drop=True)
                       , expected.reset_index(drop=True))



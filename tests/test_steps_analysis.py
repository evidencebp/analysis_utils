import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from analysis_utils.steps_analysis import build_two_steps_ds

@pytest.mark.parametrize(('metric_per_year_df'
                             , 'keys'
                             , 'metrics'
                            , 'expected')
    , [
pytest.param(

    pd.DataFrame([(2021, 'a', 200, 150)
                     , (2020, 'a', 100, 50)
                     , (2019, 'a', 50, 50)
                     , (2019, 'b', 100, 50)
                     , (2018, 'b', 50, 50)
                     , (2019, 'c', 100, 50)
                     , (2018, 'c', None, 0)
                  ]
        , columns=['year', 'repo_name', 'commits', 'authors'])
        ,['repo_name']
        ,['commits', 'authors']
        , pd.DataFrame([('a', 200, 150, 2021, 2020, 100, 50, 1.0, 2.0)
                     , ('a', 100, 50, 2020, 2019, 50, 50, 1.0, 0.0)
                     , ('b', 100, 50, 2019, 2018, 50, 50, 1.0, 0.0)
                     , ('c', 100, 50, 2019, 2018, None, 0, None, None)
                  ]
        , columns=['repo_name', 'cur_commits', 'cur_authors', 'cur_year', 'prev_year',
       'prev_commits', 'prev_authors', 'rel_commits', 'rel_authors'])

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


    assert_frame_equal(actual#.reset_index(drop=True)
                       , expected#.reset_index(drop=True)
                       , check_dtype=False  )



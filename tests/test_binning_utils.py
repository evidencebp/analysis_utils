import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from analysis_utils.binning_utils import sides_binning, side_binning_by_direction, SIDES_SUFFIX
from analysis_utils.cochange_analysis import the_lower_the_better, the_higher_the_better

@pytest.mark.parametrize(('df'
                  , 'column'
                  , 'labels'
                  , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [1]
                , [2]
                , [3]
                , [4]
            ], columns=['c1'])
            , 'c1'
            , [0, 1, 2]
            , pd.Series([0, 1, 1, 2])

, id='reg1')
,pytest.param(
 pd.DataFrame([
     [1]
     , [1]
     , [1]
     , [1]
     , [1]
     , [3]
     , [3]
     , [3]
     , [4]
 ], columns=['c1'])
 , 'c1'
 , [0, 1, 2]
 , pd.Series([0, 0, 0,0, 0,1,  1, 1, 2])

 , id='too_large_25')
                         ])
def test_sides_binning(df: pd.DataFrame
                  , column:str
                  , labels
                  , expected):

    actual = sides_binning(df=df
                  , column=column
                  , labels=labels)

    assert actual.tolist() == expected.tolist()


@pytest.mark.parametrize(('df'
                  , 'metrics'
                  , 'suffix'
                  , 'labels'
                  , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [1, 1]
                , [2, 2]
                , [3, 3]
                , [4, 4]
            ], columns=['lower_better', 'higher_better'])
            , {'lower_better' : the_lower_the_better, 'higher_better' : the_higher_the_better}
            , SIDES_SUFFIX
            , ['Bad', 'Medium', 'Good']
            , pd.DataFrame([
                [1, 1, 'Good', 'Bad']
                , [2, 2, 'Medium', 'Medium']
                , [3, 3, 'Medium', 'Medium']
                , [4, 4, 'Bad', 'Good']
            ], columns=['lower_better', 'higher_better', 'lower_better_SIDES', 'higher_better_SIDES'])

, id='reg1')
                         ])
def test_side_binning_by_direction(df: pd.DataFrame
                  , metrics
                  , suffix
                  , labels
                  , expected):

    actual = side_binning_by_direction(df=df
                            , metrics=metrics
                            , suffix=suffix
                            , labels=labels)

    assert_frame_equal(actual, expected)


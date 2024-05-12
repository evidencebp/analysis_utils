import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from file_utils import join_dataframes, Strings, DataFrames

@pytest.mark.parametrize(('dataframes'
                            , 'keys'
                            , 'how'
                            , 'expected')
    , [
pytest.param(
            [
            pd.DataFrame([
                [1, 1]
                , [2, 1]
                , [3, 1]
            ], columns=['key', 'f1'])
            , pd.DataFrame([
                [1, 2]
                , [2, 2]
                , [3, 2]
            ], columns=['key', 'f2'])
            , pd.DataFrame([
                [1, 3]
                , [2, 3]
                , [3, 3]
            ], columns=['key', 'f3'])
            ]
            , ['key']
            , 'inner'
            , pd.DataFrame([
                    [1, 1, 2, 3]
                    , [2, 1, 2, 3]
                    , [3, 1, 2, 3]
    ], columns=['key', 'f1', 'f2', 'f3'])

, id='reg1')
                         ])
def test_join_dataframes(dataframes: DataFrames
                                , keys:Strings
                                , how:str
                                , expected: pd.DataFrame):

    actual = join_dataframes(dataframes
                    , keys
                    , how)

    assert_frame_equal(actual.reset_index(drop=True)
                       , expected.reset_index(drop=True))



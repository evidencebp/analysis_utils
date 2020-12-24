import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal
import pytest

from binning_utils import sides_binning

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
                         ])
def test_sides_binning(df: pd.DataFrame
                  , column:str
                  , labels
                  , expected):

    actual = sides_binning(df=df
                  , column=column
                  , labels=labels)

    assert actual.tolist() == expected.tolist()



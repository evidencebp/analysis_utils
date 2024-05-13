from typing import List

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from analysis_utils.classifiers_agreement_stats import classifiers_agreement_stats


@pytest.mark.parametrize(('df'
                            , 'classifiers_columns'
                            , 'count_column'
                            , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [1, 1, 1, 100]
                , [1, 0, 1, 20]
                , [1, 1, 0, 30]
                , [-1, 1, 1, 32]
                , [-1, -1, -1, 1000]
                ], columns=['f1', 'f2', 'f3', 'count'])
            , ['f1', 'f2', 'f3']
            , 'count'
            , pd.DataFrame([
                [3, 0, 0, 100]
                , [2, 1, 0, 50]
                , [2, 0, 1, 32]
                , [0, 0, 3, 1000]
    ], columns=[1, 0, -1, 'count'])

, id='reg1')
                         ])
def test_classifiers_agreement_stats(df: pd.DataFrame
                                , classifiers_columns: List[str]
                                , count_column: str
                                , expected):
    actual = classifiers_agreement_stats(df=df
                                , classifiers_columns=classifiers_columns
                                , count_column=count_column)


    assert_frame_equal(actual.reset_index(drop=True)
                       , expected.reset_index(drop=True))



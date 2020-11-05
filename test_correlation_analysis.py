import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from correlation_analysis import analyze_correlation, StringsList

@pytest.mark.parametrize(('metrics_df'
                                , 'concept_column'
                                , 'metrics'
                                , 'correlation_stats_file'
                                , 'concept_display'
                            , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [1, 1, -1, 1, 3]
                , [2, 2, -2, None, 3]
                , [3, 3, -3, None, 3]
                , [-1, -1, 1, -1, 3]
                , [-2, -2, 2, None, 3]
                , [-3, -3, 3, None, 3]
            ], columns=['concept', 'same_concept', 'minus_concept', 'concept_with_none', 'constant'])
            , 'concept'
            , ['concept', 'same_concept', 'minus_concept', 'concept_with_none', 'constant']
            , None
            , 'Pearson'
            , pd.DataFrame([
                                ['concept', 1.0]
                                , ['concept_with_none', 1.0]
                                , ['same_concept', 1.0]
                                , ['minus_concept', -1.0]
                                , ['constant', np.NaN]
                ], columns=['metric', 'Pearson'])

, id='reg1')
                         ])
def test_analyze_correlation(metrics_df: pd.DataFrame
                                , concept_column: str
                                , metrics: StringsList
                                , correlation_stats_file: str
                                , concept_display: str
                                , expected):

    actual = analyze_correlation(metrics_df
                                , concept_column
                                , metrics
                                , correlation_stats_file
                                , concept_display)

    assert_frame_equal(actual.reset_index(drop=True)
                       , expected.reset_index(drop=True))



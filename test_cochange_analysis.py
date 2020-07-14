import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from cochange_analysis import cochange_analysis

@pytest.mark.parametrize(('per_year_df'
                         , 'metrics_dict'
                         , 'keys'
                         , 'control_variables'
                         , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [2010, 10, 10, 1],
                [2009, 9, 9, 1],
                [2008, 8, 8, 1],
                ], columns=['year', 'f1', 'f2', 'k'])
            , {'f1' : lambda prev, cur :prev < cur
               , 'f2' : lambda prev, cur :prev < cur}
            , ['k']
            , []
            , {'f2': {'true_positives': 2, 'true_negatives': 0, 'false_positives': 0, 'false_negatives': 0
            , 'samples': 2, 'accuracy': 1.0, 'positive_rate': 1.0, 'hit_rate': 1.0, 'precision': 1.0
            , 'precision_lift': 0.0, 'recall': 1.0, 'fpr': 0, 'jaccard': 1.0, 'independent_prob': 1.0
            , 'lift_over_independent': 0.0, 'lift_over_majority': 0.0, 'comment': None}}

, id='reg1')
                         ])
def test_cochange_analysis(per_year_df
                         , metrics_dict
                         , keys
                         , control_variables
                         , expected
                         ):
    actual = cochange_analysis(per_year_df
                         , metrics_dict
                         , keys
                         , control_variables=[]
                         )

    assert actual == expected



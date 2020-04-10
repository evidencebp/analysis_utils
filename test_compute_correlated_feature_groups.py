import pandas as pd
import pytest

from compute_correlated_feature_groups import compute_correlated_feautre_groups, graph_to_groups

@pytest.mark.parametrize(('df'
                      , 'expected')
    , [
pytest.param(
            pd.DataFrame( [
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0]
    ]
            , columns=['a1', 'a2', 'a3', 'b1', 'b2'])

            , [['a1', 'a2', 'a3'], ['b1', 'b2']]
            , id='reg1')
                         ])
def test_graph_to_groups(df
                                           , expected):
   actual = graph_to_groups(df
                            , df.columns)

   assert actual == expected
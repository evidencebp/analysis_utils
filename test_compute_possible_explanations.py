from typing import List

import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from compute_possible_explanations import compute_possible_explanations, equality


@pytest.mark.parametrize(('df'
                            , 'concept_column'
                            , 'keys'
                            , 'comparison_function'
                            , 'features'
                            , 'expected')
    , [

pytest.param(
            pd.DataFrame([
                [0, 1, 1, 1, 1]
                , [1, 1, 0, 1, 1]
                ], columns=['id', 'f1', 'f2', 'f3', 'concept'])
            , 'concept'
            , ['id']
            , equality
            , None
            , pd.DataFrame(None
    , columns=['id_x', 'id_y', 'feature'])
, id='same_concept')


, pytest.param(
            pd.DataFrame([
                [0, 1, 1, 1, 1]
                , [3, 1, 1, 1, 0]
                ], columns=['id', 'f1', 'f2', 'f3', 'concept'])
            , 'concept'
            , ['id']
            , equality
            , None
            , pd.DataFrame(None
    , columns=['id_x', 'id_y', 'feature'])
, id='different_pair_no_explanation')


, pytest.param(
            pd.DataFrame([
                [0, 1, 1, 1, 1]
                , [4, 1, 0, 1, 0]
                ], columns=['id', 'f1', 'f2', 'f3', 'concept'])
            , 'concept'
            , ['id']
            , equality
            , None
            , pd.DataFrame([
                    [0, 4, 'f2']
                    , [4, 0, 'f2']

    ], columns=['id_x', 'id_y', 'feature'])
, id='different_pair')

, pytest.param(
            pd.DataFrame([
                [0, 1, 1, 1, 1]
                , [3, 1, 1, 1, 0]
                , [4, 1, 0, 1, 0]
                ], columns=['id', 'f1', 'f2', 'f3', 'concept'])
            , 'concept'
            , ['id']
            , equality
            , None
            , pd.DataFrame([
                     [0, 4, 'f2']
                    , [4, 0, 'f2']

            ], columns=['id_x', 'id_y', 'feature'])
, id='one_with_some')

, pytest.param(
            pd.DataFrame([
                [1, 1, 0, 1, 1]
                , [3, 1, 1, 1, 0]
                , [4, 1, 0, 1, 0]
                ], columns=['id', 'f1', 'f2', 'f3', 'concept'])
            , 'concept'
            , ['id']
            , equality
            , None
            , pd.DataFrame([
                     [1, 3, 'f2']
                    , [3, 1, 'f2']

            ], columns=['id_x', 'id_y', 'feature'])
, id='second_with_some')


, pytest.param(
            pd.DataFrame([
                [2, 1, 1, 0, 1]
                , [3, 1, 1, 1, 0]
                , [4, 1, 0, 1, 0]
                ], columns=['id', 'f1', 'f2', 'f3', 'concept'])
            , 'concept'
            , ['id']
            , equality
            , None
            , pd.DataFrame([
                    [2, 3, 'f3']
                    , [2, 4, 'f2']
                    , [2, 4, 'f3']
                    , [3, 2, 'f3']
                    , [4, 2, 'f2']
                    , [4, 2, 'f3']

    ], columns=['id_x', 'id_y', 'feature'])
, id='third_with_some')


, pytest.param(
            pd.DataFrame([
                [0, 1, 1, 1, 1]
                , [1, 1, 0, 1, 1]
                , [2, 1, 1, 0, 1]
                , [3, 1, 1, 1, 0]
                , [4, 1, 0, 1, 0]
                ], columns=['id', 'f1', 'f2', 'f3', 'concept'])
            , 'concept'
            , ['id']
            , equality
            , None
            , pd.DataFrame([
                [0, 4, 'f2']
                , [1, 3, 'f2']
                , [2, 3, 'f3']
                , [2, 4, 'f2']
                , [2, 4, 'f3']

                , [3, 1, 'f2']
                , [3, 2, 'f3']

                , [4, 0, 'f2']
                , [4, 2, 'f2']
                , [4, 2, 'f3']

            ], columns=['id_x', 'id_y', 'feature'])
, id='all_three')
                         ])
def test_compute_possible_explanations(df: pd.DataFrame
                                        , concept_column: str
                                        , keys: List[str]
                                        , comparison_function
                                        , features: List[str]
                                        , expected):

    actual = compute_possible_explanations(df=df
                                  , concept_column=concept_column
                                  , keys=keys
                                  , comparison_function=comparison_function
                                  , features=features)


    assert_frame_equal(actual.reset_index(drop=True)
                       , expected.reset_index(drop=True))

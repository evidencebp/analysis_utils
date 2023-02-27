import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from compare_twin_behaviours import compare_twin_behaviours, build_cartesian_product_twin_ds\
    , build_distinct_cartesian_product_twin_ds, build_twins_identification_ds

@pytest.mark.parametrize(('first_behaviour'
                          , 'second_behaviour'
                          , 'keys'
                          , 'comparison_columns'
                          , 'comparison_function'
                      , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [1, 1, 1, 0, 0],
                [2, 0, 1, 0, 0],
                [3, 0, 0, 0, 0],
                [4, 0, 0, 0, 1],
                [5, 0, 0, 0, 0]
                ], columns=['k', 'a1', 'a2', 'a3', 'a4'])
            , pd.DataFrame([
                 [1, 1, 0, 0, 0],
                 [2, 0, 1, 5, 0],
                 [3, 0, 0, 0, 4],
                 [4, 0, 1, 0, 1],
                 [5, 0, 0, 0, 0]
             ], columns=['k', 'a1', 'a2', 'a3', 'a4'])
            , ['k']
            , ['a1', 'a2', 'a3']
            , lambda x, y : x == y
            , pd.DataFrame([
                [1, True, False, True],
                [2, True, True, False],
                [3, True, True, True],
                [4, True, False, True],
                [5, True, True, True]
            ], columns=['k', 'a1_cmp', 'a2_cmp', 'a3_cmp'])

, id='reg1')
                         ])
def test_compare_twin_behaviours(first_behaviour
                          , second_behaviour
                          , keys
                          , comparison_columns
                          , comparison_function
                      , expected):
    actual = compare_twin_behaviours(first_behaviour
                          , second_behaviour
                          , keys
                          , comparison_columns
                          , comparison_function)

    assert_frame_equal(actual, expected)



@pytest.mark.parametrize(('first_behaviour'
                          , 'second_behaviour'
                          , 'comparison_columns'
                          , 'comparison_function'
                      , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [1]
                , [2]
                , [3]
                ], columns=['f1'])
            , pd.DataFrame([
                [1]
                , [2]
             ], columns=['f1'])
            , ['f1']
            , None #lambda x: x['f1' + '_x'] == x['f1' + '_y']
            , pd.DataFrame([
                [1, 1]
                , [1, 2]
                , [2, 1]
                , [2, 2]
                , [3, 1]
                , [3, 2]
    ], columns=['f1_x', 'f1_y'])
, id='reg1')
, pytest.param(
            pd.DataFrame([
                [1, 1]
                , [2, 0]
                ], columns=['id', 'concept'])
            , pd.DataFrame([
                [3, 1]
                , [4, 0]
             ], columns=['id', 'concept'])
            , ['id', 'concept']
            , lambda x: x['concept' + '_x'] == x['concept' + '_y']
            , pd.DataFrame([
                [1, 1, 4, 0]
                , [2, 0, 3, 1]
    ], columns=['id_x', 'concept_x', 'id_y', 'concept_y'])
            , id='remove_same_concept')
                         ])
def test_build_cartesian_product_twin_ds(first_behaviour
                          , second_behaviour
                          , comparison_columns
                          , comparison_function
                      , expected):
    actual = build_cartesian_product_twin_ds(first_behaviour
                          , second_behaviour
                          , comparison_columns
                          , comparison_function)


    assert_frame_equal(actual.reset_index(drop=True)
                       , expected.reset_index(drop=True))



@pytest.mark.parametrize(('first_behaviour'
                          , 'second_behaviour'
                          , 'comparison_columns'
                          , 'id_column'
                      , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [1, 4]
                , [2, 0]
                ], columns=['id', 'concept'])
            , pd.DataFrame([
                [1, 5]
                , [3, 0]
             ], columns=['id', 'concept'])
            , ['id', 'concept']
            , 'id'
            , pd.DataFrame([
                [1, 4, 3, 0]
                , [2, 0, 1, 5]
                , [2, 0, 3, 0]
    ], columns=['id_x', 'concept_x', 'id_y', 'concept_y'])
            , id='remove_same_concept')
                         ])
def test_build_distinct_cartesian_product_twin_ds(first_behaviour
                          , second_behaviour
                          , comparison_columns
                          , id_column
                      , expected):
    actual = build_distinct_cartesian_product_twin_ds(first_behaviour
                          , second_behaviour
                          , comparison_columns
                          , id_column)


    assert_frame_equal(actual.reset_index(drop=True)
                       , expected.reset_index(drop=True))




@pytest.mark.parametrize(('first_behaviour'
                          , 'second_behaviour'
                          , 'matching_function'
                          , 'filtering_function'
                      , 'expected')
    , [
pytest.param(
           pd.DataFrame([
               [1, 1, 1, 4]
               , [2, 1, 2, 5]
               , [3, 2, 1, 3]
               ], columns=['evaluation_id', 'entity_id', 'evaluator_id', 'val'])
           , pd.DataFrame([
               [1, 1, 1, 4]
               , [2, 1, 2, 5]
               , [3, 2, 1, 3]
               ], columns=['evaluation_id', 'entity_id', 'evaluator_id', 'val'])
           , lambda x: 1 if x['entity_id_x'] == x['entity_id_y'] else 0
           , lambda x: x['evaluation_id_x'] == x['evaluation_id_y']
           , pd.DataFrame([
               [1, 1, 1, 4, 2, 1, 2, 5, 1]
               , [1, 1, 1, 4, 3, 2, 1, 3, 0]
               , [2, 1, 2, 5, 1, 1, 1, 4, 1]
               , [2, 1, 2, 5, 3, 2, 1, 3, 0]
               , [3, 2, 1, 3, 1, 1, 1, 4, 0]
               , [3, 2, 1, 3, 2, 1, 2, 5, 0]
   ], columns=['evaluation_id_x', 'entity_id_x', 'evaluator_id_x', 'val_x'
               , 'evaluation_id_y', 'entity_id_y','evaluator_id_y', 'val_y', 'Is_Twin'])
           , id='match_by_entity')

, pytest.param(
            pd.DataFrame([
                [1, 1, 1, 4]
                , [2, 2, 1, 5]
                , [3, 1, 1, 3]
                ], columns=['evaluation_id', 'entity_id', 'evaluator_id', 'val'])
            , pd.DataFrame([
                [1, 1, 1, 4]
                , [2, 2, 1, 5]
                , [3, 1, 1, 3]
                ], columns=['evaluation_id', 'entity_id', 'evaluator_id', 'val'])
            , lambda x: 1 if (x['entity_id_x'] == x['entity_id_y']
                                and x['evaluator_id_x'] == x['evaluator_id_y']) else 0
            , lambda x: x['evaluation_id_x'] == x['evaluation_id_y']
            , pd.DataFrame([
                [1, 1, 1, 4, 2, 2, 1, 5, 0]
                , [1, 1, 1, 4, 3, 1, 1, 3, 1]
                , [2, 2, 1, 5, 1, 1, 1, 4, 0]
                , [2, 2, 1, 5, 3, 1, 1, 3, 0]
                , [3, 1, 1, 3, 1, 1, 1, 4, 1]
                , [3, 1, 1, 3, 2, 2, 1, 5, 0]
    ], columns=['evaluation_id_x', 'entity_id_x', 'evaluator_id_x', 'val_x'
                , 'evaluation_id_y', 'entity_id_y','evaluator_id_y', 'val_y', 'Is_Twin'])
            , id='match_by_entity_and_evaluator')


                         ])
def test_build_twins_identification_ds(first_behaviour
                            , second_behaviour
                            , matching_function
                            , filtering_function
                            , expected):


    actual = build_twins_identification_ds(first_behaviour
                            , second_behaviour
                            , matching_function
                            , filtering_function)

    assert_frame_equal(actual.sort_index(axis=1).reset_index(drop=True)
                       , expected.sort_index(axis=1).reset_index(drop=True))
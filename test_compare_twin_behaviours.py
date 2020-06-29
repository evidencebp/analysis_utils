import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from compare_twin_behaviours import compare_twin_behaviours

@pytest.mark.parametrize(('first_behaviour'
                          , 'second_behaviour'
                          , 'keys'
                          , 'comparision_columns'
                          , 'comparision_function'
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
                          , comparision_columns
                          , comparision_function
                      , expected):
    actual = compare_twin_behaviours(first_behaviour
                          , second_behaviour
                          , keys
                          , comparision_columns
                          , comparision_function)

    assert_frame_equal(actual, expected)



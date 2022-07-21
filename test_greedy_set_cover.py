import pytest

from greedy_set_cover import greedy_set_cover

@pytest.mark.parametrize(('sets_to_cover'
                            , 'expected')
    , [
pytest.param(
            []
            , []
, id='empty')
, pytest.param(
            [frozenset([1]), frozenset([2]), frozenset([3])]
            , [1, 2, 3]
, id='reg1')
, pytest.param(
            [frozenset([1, 4]), frozenset([2, 4]), frozenset([3, 4])]
            , [4]
            , id='cover_all')
, pytest.param(
            [frozenset([2*i for i in range(7)])
            , frozenset([1 + 2*i for i in range(7)])
            , frozenset([0, 7])
            , frozenset([1, 2, 8, 9])
            , frozenset([3, 4, 5, 6, 10, 11, 12, 13])]
            , [0, 1, 3]
            , id='classic_not_optimal')
                         ])
def test_greedy_set_cover(sets_to_cover
                             , expected):

    actual = greedy_set_cover(sets_to_cover)

    assert actual == expected


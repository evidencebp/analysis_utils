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
            [set([1]), set([2]), set([3])]
            , [1, 2, 3]
, id='reg1')
, pytest.param(
            [set([1, 4]), set([2, 4]), set([3, 4])]
            , [4]
            , id='cover_all')
, pytest.param(
            [set([2*i for i in range(7)])
            , set([1 + 2*i for i in range(7)])
            , set([0, 7])
            , set([1, 2, 8, 9])
            , set([3, 4, 5, 6, 10, 11, 12, 13])]
            , [0, 1, 3]
            , id='classic_not_optimal')
                         ])
def test_greedy_set_cover(sets_to_cover
                             , expected):

    actual = greedy_set_cover(sets_to_cover)

    assert actual == expected


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
                         ])
def test_greedy_set_cover(sets_to_cover
                             , expected):

    actual = greedy_set_cover(sets_to_cover)

    assert actual == expected


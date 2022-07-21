from typing import List, Set
from functools import partial

import pytest

from greedy_set_cover import greedy_set_cover, any_item_covers_set, covers_threshold

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


@pytest.mark.parametrize(('set_to_cover'
                            , 'covering_items'
                            , 'expected')
    , [
pytest.param(
            []
            , []
            , False
, id='empty')
, pytest.param(
            frozenset([1,2 ,3])
            , [2]
            , True
, id='reg1')
                         ])
def test_any_item_covers_set(set_to_cover: set[int]
                             , covering_items: list[int]
                             , expected):

    actual = any_item_covers_set(set_to_cover
                                 , covering_items)

    assert actual == expected


@pytest.mark.parametrize(('set_to_cover'
                            , 'covering_items'
                            , 'ratio_map'
                            , 'threshold'
                            , 'expected')
    , [
pytest.param(
            frozenset([1,2 ,3])
            , [1]
            , {hash(frozenset([1,2 ,3])): {1 : 0.8 , 2:0.1, 3: 0.1}}
            , 0.8
            , True
, id='reg1')
, pytest.param(
            frozenset([1,2 ,3])
            , [1]
            , {hash(frozenset([1, 2,3])): {1: 0.8, 2: 0.1, 3: 0.1}}
            , 0.9
            , False
, id='reg2')
                             , pytest.param(
            frozenset([1, 2, 3])
            , [1, 2]
            , {hash(frozenset([1, 2, 3])): {1: 0.8, 2: 0.1, 3: 0.1}}
            , 0.9
            , True
            , id='reg3')
                         ])
def test_covers_threshold(set_to_cover: Set[int]
                , covering_items: list[int]
                , ratio_map: dict
                , threshold
                , expected):

    actual = covers_threshold(set_to_cover
                , covering_items
                , ratio_map
                , threshold)

    assert actual == expected


@pytest.mark.parametrize(('sets_to_cover'
                            , 'ratio_map'
                            , 'threshold'
                            , 'expected')
    , [
pytest.param(
            [frozenset([1,2 ,3])]
            , {hash(frozenset([1,2 ,3])): {1 : 0.8 , 2:0.1, 3: 0.1}}
            , 0.8
            , [1]
, id='reg1')
, pytest.param(
            [frozenset([1,2 ,3])]
            , {hash(frozenset([1, 2,3])): {1: 0.8, 2: 0.1, 3: 0.1}}
            , 0.9
            , [1, 2]
, id='reg2')
                         ])
def test_greedy_set_cover_by_covers_threshold(sets_to_cover: Set[int]
                , ratio_map: dict
                , threshold
                , expected):

    covering_func = partial(covers_threshold
                            , ratio_map=ratio_map
                            , threshold=threshold)

    actual = greedy_set_cover(sets_to_cover
                     , is_covered=covering_func)

    assert actual == expected

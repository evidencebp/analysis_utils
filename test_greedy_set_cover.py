from typing import List, Set, Dict
from functools import partial

import pytest

from greedy_set_cover import greedy_set_cover, any_item_covers_set, covers_threshold\
    , item_covers_ratios_sum, reduce_new_item

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
def test_greedy_set_cover(sets_to_cover: Set[int]
                             , expected: List[int]):

    actual: List[int] = greedy_set_cover(sets_to_cover)

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
                             , expected: bool):

    actual: bool = any_item_covers_set(set_to_cover
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
                , threshold: float
                , expected: bool):

    actual: bool = covers_threshold(set_to_cover
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
            [frozenset([1, 2, 3])]
            , {hash(frozenset([1, 2, 3])): {1: 0.09, 2: 0.8, 3: 0.11}}
            , 0.8
            , [2]
, id='reg1')
, pytest.param(
            [frozenset([1, 2,3])]
            , {hash(frozenset([1, 2, 3])): {1: 0.8, 2: 0.1, 3: 0.1}}
            , 0.9
            , [1, 2]
, id='reg2')
                         ])
def test_greedy_set_cover_by_covers_threshold(sets_to_cover: Set[int]
                , ratio_map: dict
                , threshold: float
                , expected: List[int]):

    scoring_func = partial(item_covers_ratios_sum
                            , ratio_map=ratio_map)
    covering_func = partial(covers_threshold
                            , ratio_map=ratio_map
                            , threshold=threshold)

    actual: bool = greedy_set_cover(sets_to_cover
                                     , is_covered=covering_func
                                     , cover_score=scoring_func)

    assert actual == expected

@pytest.mark.parametrize(('items'
                , 'new_item'
                , 'count_dict'
                , 'expected_items'
                , 'expected_count_dict')
    , [
pytest.param(
            frozenset([1, 2, 3])
            , 2
            , {1: 1, 2: 7, 3: 4}
            , frozenset([1, 2, 3])
            , {1: 1, 2: 6, 3: 4}
, id='has_more_items')
, pytest.param(
            frozenset([1, 2, 3])
            , 2
            , {1: 1, 2: 1, 3: 4}
            , frozenset([1, 3])
            , {1: 1, 3: 4}
, id='last_item')

                         ])
def test_reduce_new_item(items: Set[int]
                , new_item: int
                , count_dict: Dict[int, int]
                , expected_items: Set[int]
                , expected_count_dict: Dict[int, int]):

    actual_items: Set[int] = reduce_new_item(items
                                   , new_item
                                   , count_dict)

    assert actual_items == expected_items
    assert count_dict == expected_count_dict


@pytest.mark.parametrize(('items'
                , 'new_item'
                , 'count_dict')
    , [
pytest.param(
            frozenset([1, 2, 3])
            , 7
            , {1: 1, 2: 7, 3: 4}
, id='item_not_in_items')
, pytest.param(
            frozenset([1, 2, 3])
            , 3
            , {1: 1, 2: 1}
, id='item_not_in_dict')

                         ])
def test_reduce_new_item_exception(items: Set[int]
                , new_item: int
                , count_dict: Dict[int, int]):
    with pytest.raises(Exception):
        reduce_new_item(items
                           , new_item
                           , count_dict)



@pytest.mark.parametrize(('sets_to_cover'
                            , 'ratio_map'
                            , 'threshold'
                            , 'count_dict'
                            , 'expected')
    , [
pytest.param(
            [frozenset([1, 2, 3])]
            , {hash(frozenset([1, 2, 3])): {1: 0.09, 2: 0.4, 3: 0.11}}
            , 0.8
            , {1: 1, 2: 2, 3: 1}
            , [2, 2]
, id='reg1')
, pytest.param(
             [frozenset([1, 2, 3])]
             , {hash(frozenset([1, 2, 3])): {1: 0.09, 2: 0.4, 3: 0.11}}
             , 0.9
             , {1: 1, 2: 2, 3: 1}
             , [2, 2, 3]
 , id='reg2')
                         ])
def test_greedy_set_cover_by_reduce_new_item(sets_to_cover: Set[int]
                , ratio_map: dict
                , threshold: float
                , count_dict: dict
                , expected: List[int]):

    reduction_func = partial(reduce_new_item
                            , count_dict=count_dict)

    scoring_func = partial(item_covers_ratios_sum
                            , ratio_map=ratio_map)
    covering_func = partial(covers_threshold
                            , ratio_map=ratio_map
                            , threshold=threshold)

    actual: List[int] = greedy_set_cover(sets_to_cover
                     , is_covered=covering_func
                     , cover_score=scoring_func
                     , update_available_items=reduction_func)


    assert actual == expected


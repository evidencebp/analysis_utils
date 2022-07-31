"""
Implementation of the classical greedy set cover algorithm
https://en.wikipedia.org/wiki/Set_cover_problem#Greedy_algorithm
"""

from typing import List, Set, Callable, Dict

"""
These are auxiliary methods, used to make the set cover algorithm more flexible 
"""


def covered_sets_score(set_to_cover: Set[int]
                       , item: int) -> float:
    """
        This is the default coverage method.
        The coverage of an item is the number of sets containing it.
    """
    return len([cur_set for cur_set in set_to_cover if item in cur_set])

def covers_ratios_sum(set_to_cover: Set[int]
                , covering_items: List[int]
                , ratio_map: dict) -> float:
    """
        In this method the ratio map allows partial coverage.
        From example, an ingredient (item) is 80% of the material (set)
    """
    set_ratio_map = ratio_map[hash(set_to_cover)]
    coverage = sum([set_ratio_map.get(item, 0) for item in covering_items])

    return coverage

def item_covers_ratios_sum(set_to_cover: Set[int]
                , item: int
                , ratio_map: dict) -> float:
    """
        Auxiliary method.
        Computes how much an item covers
    """
    return sum([covers_ratios_sum(cur_set
        , covering_items=[item]
        , ratio_map=ratio_map) for cur_set in set_to_cover])

"""
    Coverage methods.
"""

def any_item_covers_set(set_to_cover: Set[int]
                , covering_items: List[int]) -> bool:
    """
        The default coverage: A set is covered if an item is contained in it.
    """
    return any([(item in set_to_cover) for item in covering_items])

def covers_threshold(set_to_cover: Set[int]
                , covering_items: List[int]
                , ratio_map: dict
                , threshold: float = 0.8) -> bool:
    """
        A set is covered if the ratio of the items in it sum to more than the desired level
    """
    coverage = covers_ratios_sum(set_to_cover
                , covering_items
                , ratio_map)

    return coverage >= threshold
"""
    Methods checking when an item should be removed and not used again.
"""
def remove_new_item(items: Set[int]
                    , new_item: int) -> Set[int]:
    """
        The default - an item is used only once and then remove.
        This is the sensible method in single coverage were nothing is gained from using the sem item
        more than once.
    """
    return items - set([new_item])

def reduce_new_item(items: Set[int]
                    , new_item: int
                    , count_dict: Dict[int, int]) -> Set[int]:
    """
        In this method we have the same item few time, stored in the count dict.
        If ratio coverage is used in combined, we can use the same item few times, to increase coverage ratio.
    """
    new_items: Set[int] = items

    if new_item in count_dict and new_item in items:
        if count_dict[new_item] > 1:
            count_dict[new_item] -= 1
        else:
            count_dict.pop(new_item)
            new_items = items - set([new_item])
    else:
        raise Exception("New item not in current items"
                        , new_item
                        , items
                        , count_dict)

    return new_items

def greedy_set_cover(sets_to_cover: List[Set]
                     , is_covered: Callable[[Set[int], List[int]], bool] = any_item_covers_set
                     , cover_score: Callable[[Set[int], int], float] = covered_sets_score
                     , update_available_items: Callable[[Set[int], int], Set[int]] = remove_new_item) -> List:
    """
        The algorithm here is the classical greedy set cover.
        Function is abstracted to allow more flexible use cases.
    """
    covering_items: List[int] = []
    to_cover: List[Set] = sets_to_cover
    items: Set[int] = set([i for cur_set in sets_to_cover for i in cur_set])

    while (items != []  # Has more items
           and to_cover != []  # More sets to cover
    ):
        # Finding the item that covers most
        most_covering = max(items
                            , key=lambda item: cover_score(to_cover, item))

        # Bookkeeping
        covering_items.append(most_covering)
        items = update_available_items(items
                                        , most_covering)
        to_cover = [cur_set for cur_set in to_cover if not is_covered(cur_set
                                                            , covering_items)]

    return covering_items


def is_coverable(sets_to_cover: List[Set]
                          , items: Set[int]) -> bool:

    for cur_set in sets_to_cover:
        if not any([i in cur_set for i in items]):
            return False

    return True

def brute_force_set_cover(sets_to_cover: List[Set]
                          , allowed_depth: int = None
                          , verbose: bool = False) -> List:

    items = set([i for cur_set in sets_to_cover for i in cur_set])
    if not allowed_depth:
        allowed_depth = min(len(sets_to_cover), min(items))

    return _brute_force_set_cover(sets_to_cover
                          , items
                          , allowed_depth)

def _brute_force_set_cover(sets_to_cover: List[Set]
                          , items: Set[int]
                          , allowed_depth: int = None
                          , verbose: bool = False) -> List:
    """
        The algorithm here is a brute force set cover.
        It goes up to a specified depth
    """
    if verbose:
        print("Entering"
              , "sets" ,sets_to_cover
              , "items" ,items
              , "depth", allowed_depth)



    # no sets
    if len(sets_to_cover) == 0:
        return []

    # no items
    if len(items) == 0:
        return None

    # reached allowed depth
    if allowed_depth == 0:
        return None

    if not is_coverable(sets_to_cover
                          , items):
        return None

    # try recursively with and without first item
    possible_items = items.intersection(set([item for cur_set in sets_to_cover for item in cur_set ]))
    current_item: int = list(possible_items)[0]

    uncovered_sets = set([cur_set for cur_set in sets_to_cover if current_item not in cur_set])
    possible_items = possible_items - set([current_item])

    ## with
    if verbose:
        print("with")
    with_cover = _brute_force_set_cover(uncovered_sets
                                            , items=possible_items
                                            , allowed_depth=allowed_depth -1)
    ## Without
    if verbose:
        print("without")
    without_cover = _brute_force_set_cover(sets_to_cover
                                            , items=possible_items
                                            , allowed_depth=allowed_depth)
    # Aggregate
    if with_cover is None:
        return without_cover # With cover failed, maybe without is ok
    else:
        if without_cover is None:
            # without failed, maybe with is ok
            # Adding current item which is used in the cover
            return [current_item] + with_cover
        else:
            # Both ok, return the shorter
            if len(with_cover) + 1 < len(without_cover):
                return [current_item] + with_cover
            else:
                return without_cover

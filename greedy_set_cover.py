"""
Implementation of the classical greedy set cover algorithm
https://en.wikipedia.org/wiki/Set_cover_problem#Greedy_algorithm
"""

from typing import List, Set

def any_item_covers_set(set_to_cover: Set[int]
                , covering_items: List[int]) -> bool:
    return any([(item in set_to_cover) for item in covering_items])

def covers_threshold(set_to_cover: Set[int]
                , covering_items: List[int]
                , ratio_map: dict
                , threshold: float = 0.8) -> bool:
    set_ratio_map = ratio_map[hash(set_to_cover)]
    coverage = sum([set_ratio_map.get(item, 0) for item in covering_items])

    return coverage >= threshold


def greedy_set_cover(sets_to_cover: List[Set]
                     , is_covered=any_item_covers_set) -> List:
    covering_items: List[int] = []
    to_cover: List[Set] = sets_to_cover
    items: Set[int] = set([i for cur_set in sets_to_cover for i in cur_set])

    while (items != []  # Has more items
           and to_cover != []  # More sets to cover
    ):
        # Finding the item that covers most
        most_covering = max(items
                            , key=lambda item: len([cur_set for cur_set in to_cover if item in cur_set]))

        # Bookkeeping
        covering_items.append(most_covering)
        items = items - set([most_covering])
        to_cover = [cur_set for cur_set in to_cover if not is_covered(cur_set
                                                            , covering_items)]

    return covering_items

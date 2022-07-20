"""
Implementation of the classical greedy set cover algorithm
https://en.wikipedia.org/wiki/Set_cover_problem#Greedy_algorithm
"""

from typing import List, Set


def greedy_set_cover(sets_to_cover: List[Set]):
    covering_items = []
    to_cover = sets_to_cover
    items = set([i for cur_set in sets_to_cover for i in cur_set])

    while (items != []  # Has more items
           and to_cover != []  # More sets to cover
    ):
        # Finding the item that covers most
        most_covering = max(items
                            , key=lambda item: len([cur_set for cur_set in to_cover if item in cur_set]))

        # Bookkeeping
        covering_items.append(most_covering)
        items = items - set([most_covering])
        to_cover = [cur_set for cur_set in to_cover if most_covering not in cur_set]

    return covering_items

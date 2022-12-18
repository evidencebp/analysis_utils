"""
The definition of possible explanation is based on:
Dhagat, Aditi, and Lisa Hellerstein.
"PAC learning with irrelevant attributes."
Proceedings 35th Annual Symposium on Foundations of Computer Science. IEEE, 1994.
https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=365704&casa_token=kmRP7e1Us70AAAAA:lZ29c6ifsdARKNliITWQL9UFQU2vi-HjYRRYhDieRcpCUbyeTNG5OOg8IuXzbVv0nQmcgq7H&tag=1

Given samples classified differently, the features in which they differ are possible
explanations of the difference in the concept.
This definition does not require the feature to be weak classifiers.
Hence, it will work on cases like XOR.
"""

from typing import List

import pandas as pd

from compare_twin_behaviours import build_cartesian_product_twin_ds


def equality(x, y):

    return x == y

def compute_possible_explanations(df: pd.DataFrame
                                  , concept_column: str
                                  , keys: List[str]
                                  , comparison_function=equality
                                  , features: List[str] = None):

    if not features:
        features = sorted(list(set(df.columns) - set(keys + [concept_column])))


    different_concepts = build_cartesian_product_twin_ds(first_behaviour=df
                    , second_behaviour=df
                    , comparison_columns=keys + features + [concept_column]
                    , filtering_function=lambda x: x[concept_column + '_x'] == x[concept_column + '_y'])
    """
    different_concepts = build_cartesian_product_twin_ds(first_behaviour=df
                    , second_behaviour=df
                    , comparison_columns=keys + features + [concept_column])

    different_concepts = different_concepts[different_concepts[concept_column + '_x']
                                            != different_concepts[concept_column + '_y']] # TODO - bug in the twins?
    """
    rows = []
    for _, r in different_concepts.iterrows():
        for f in features:
            row = []
            if not comparison_function(r[f + '_x'], r[f + '_y']):
                for k in keys:
                    row.append(r[k + '_x'])
                for k in keys:
                    row.append(r[k + '_y'])

                row.append(f)

                rows.append(row)

    explanation_columns = [k + '_x' for k in keys] \
                                 + [k + '_y' for k in keys] \
                                 + ['feature']
    explanation_df = pd.DataFrame(rows
                      , columns=(explanation_columns))

    return explanation_df.sort_values(explanation_columns)

"""

Comparing the behaviour of twins in different environments.

In SE usage, the twin is usually the same developer, working in two repositories.
The twin analysis enable to factor out the influence of the developer
and examine that of the repository.

For more explanation on the methodology and its usage, see https://arxiv.org/pdf/2007.10912.pdf


"""

import pandas as pd

from cochange_analysis import features_confusion_matrix_analysis

COMPARISON_SUFFIX = '_cmp'


def compare_twin_behaviours(first_behaviour: pd.DataFrame
                            , second_behaviour: pd.DataFrame
                            , keys: list
                            , comparision_columns: list
                            , comparision_function
                            , filtering_function=None
                            , differences_num: str = None) -> pd.DataFrame:
    """

    :param first_behaviour: A data frame that describes the behaviour of twin in an environment.
    :param second_behaviour: A data frame that he behaviour of twin in an environment.
    Many time similar to first one.
    :param keys: Identifiers of the twins.
    :param comparision_columns: The behaviour columns to compare.
    :param comparision_function: A function that compares the behaviour in the two environments.
    :param filtering_function: A function to exclude records (e.g., same repository).
    :param differences_num: Counts the number od different columns.
    :return: A data frame with the twins behaviour comparision.
    """

    first_to_match = first_behaviour[keys + comparision_columns].copy()
    second_to_match = second_behaviour[keys + comparision_columns].copy()
    joint = pd.merge(first_to_match, second_to_match, on=keys)

    if filtering_function:
        filter_column = 'filter'
        joint[filter_column] = joint.apply(filtering_function, axis=1)
        joint = joint[~joint[filter_column]]
        joint = joint.drop(columns=[filter_column])

    joint_cols = keys.copy()
    for i in comparision_columns:
        key = i + COMPARISON_SUFFIX
        joint_cols.append(key)
        joint[key] = joint.apply(lambda x: comparision_function(x[i + '_x'], x[i + '_y'])
                                , axis=1)

    if differences_num:
        joint[differences_num] = joint[
            [i + COMPARISON_SUFFIX for i in comparision_columns]].sum(axis=1)
        relevant_columns = joint_cols + [differences_num]
    else:
        relevant_columns = joint_cols

    return joint[relevant_columns]


def compute_confusion_matrics(df: pd.DataFrame
                              , concept: str
                              , columns: list
                              , keys: list):
    """
        Compute the confusion matrix of a set of features with respect to a concept.
        Useful for twin behaviour too.

    :param df: Data frame
    :param concept: Concept to predict
    :param columns: A list of decision stump classifiers.
    :param keys:
    :return:
    """

    stats = {}
    for i in columns:
        stats[i] = features_confusion_matrix_analysis(df
                       , first_metric=i
                       , second_metric=concept
                       , keys=keys)

    return stats

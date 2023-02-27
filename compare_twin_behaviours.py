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


def build_twin_ds(first_behaviour: pd.DataFrame
                            , second_behaviour: pd.DataFrame
                            , keys: list
                            , comparision_columns: list
                            , filtering_function=None) -> pd.DataFrame:
    """

    :param first_behaviour: A data frame that describes the behaviour of twin in an environment.
    :param second_behaviour: A data frame that the behaviour of twin in an environment.
    Many times similar to first one.
    :param keys: Identifiers of the twins.
    :param comparision_columns: The behaviour columns to compare.
    :param comparision_function: A function that compares the behaviour in the two environments.
    :param filtering_function: A function to exclude records (e.g., same repository).
    :param differences_num: Counts the number od different columns.
    :return: A data frame with the twins' behavior comparision.
    """

    first_to_match = first_behaviour[keys + comparision_columns].copy()
    second_to_match = second_behaviour[keys + comparision_columns].copy()
    joint = pd.merge(first_to_match, second_to_match, on=keys)

    if filtering_function:
        filter_column = 'filter'
        joint[filter_column] = joint.apply(filtering_function, axis=1)
        joint = joint[~joint[filter_column]]
        joint = joint.drop(columns=[filter_column])

    return joint

def build_cartesian_product_twin_ds(first_behaviour: pd.DataFrame
                            , second_behaviour: pd.DataFrame
                            , comparison_columns: list
                            , filtering_function=None) -> pd.DataFrame:
    """
        Build a Cartesian product by using a constant joint column and reducing to build_twin_ds.
    """

    SAME_VALUE_COLUMN = 'SAME_VALUE_COLUMN'

    first_behaviour[SAME_VALUE_COLUMN] = SAME_VALUE_COLUMN
    second_behaviour[SAME_VALUE_COLUMN] = SAME_VALUE_COLUMN

    twins_df = build_twin_ds(first_behaviour
                            , second_behaviour
                            , keys=[SAME_VALUE_COLUMN]
                            , comparision_columns=comparison_columns
                            , filtering_function=filtering_function)

    twins_df.drop(columns=[SAME_VALUE_COLUMN]
                  , inplace=True)

    return twins_df


def build_distinct_cartesian_product_twin_ds(first_behaviour: pd.DataFrame
                            , second_behaviour: pd.DataFrame
                            , comparison_columns: list
                            , id_column) -> pd.DataFrame:
    """
        Build a Cartesian product by using a constant joint column and reducing to build_twin_ds.
    """

    SAME_VALUE_COLUMN = 'SAME_VALUE_COLUMN'

    first_behaviour[SAME_VALUE_COLUMN] = SAME_VALUE_COLUMN
    second_behaviour[SAME_VALUE_COLUMN] = SAME_VALUE_COLUMN

    twins_df = build_twin_ds(first_behaviour
                            , second_behaviour
                            , keys=[SAME_VALUE_COLUMN]
                            , comparision_columns=comparison_columns
                            , filtering_function=lambda x: x[id_column + '_x'] == x[id_column + '_y'])

    twins_df.drop(columns=[SAME_VALUE_COLUMN]
                  , inplace=True)

    return twins_df

def compare_twin_behaviours(first_behaviour: pd.DataFrame
                            , second_behaviour: pd.DataFrame
                            , keys: list
                            , comparison_columns: list
                            , comparison_function
                            , filtering_function=None
                            , differences_num: str = None) -> pd.DataFrame:
    """

    :param first_behaviour: A data frame that describes the behaviour of twin in an environment.
    :param second_behaviour: A data frame that describes the behaviour of twin in an environment.
    Many times similar to first one.
    :param keys: Identifiers of the twins.
    :param comparison_columns: The behaviour columns to compare.
    :param comparison_function: A function that compares the behaviour in the two environments.
    :param filtering_function: A function to exclude records (e.g., same repository).
    :param differences_num: Counts the number od different columns.
    :return: A data frame with the twins' behaviour comparison.
    """

    joint = build_twin_ds(first_behaviour=first_behaviour
                            , second_behaviour=second_behaviour
                            , keys=keys
                            , comparision_columns=comparison_columns
                            , filtering_function=filtering_function)

    joint_cols = keys.copy()
    for i in comparison_columns:
        key = i + COMPARISON_SUFFIX
        joint_cols.append(key)
        joint[key] = joint.apply(lambda x: comparison_function(x[i + '_x'], x[i + '_y'])
                                , axis=1)

    if differences_num:
        joint[differences_num] = joint[
            [i + COMPARISON_SUFFIX for i in comparison_columns]].sum(axis=1)
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

def build_twins_identification_ds(first_behaviour
                                     , second_behaviour
                                     , matching_function
                                     , filtering_function):
    """
    The following function create a dataset whose concept is "Is_Twin".
    Twins are pairs of samples that match according to a key.
    For example, evaluations of the same entity
    or evaluation of the same entity by the same evaluators.
    The cross product of the rest are the negative samples.
    """
    SAME_VALUE_COLUMN = 'SAME_VALUE_COLUMN'

    first_behaviour[SAME_VALUE_COLUMN] = SAME_VALUE_COLUMN
    second_behaviour[SAME_VALUE_COLUMN] = SAME_VALUE_COLUMN

    twins_df = build_twin_ds(first_behaviour=first_behaviour
                 , second_behaviour=second_behaviour
                 , keys=[SAME_VALUE_COLUMN]
                 , comparision_columns=list(set(list(first_behaviour.columns)) - set([SAME_VALUE_COLUMN]))
                 , filtering_function=filtering_function)

    twins_df.drop(columns=[SAME_VALUE_COLUMN]
                  , inplace=True)


    twins_df['Is_Twin'] = twins_df.apply(matching_function
                                  , axis=1)

    return twins_df




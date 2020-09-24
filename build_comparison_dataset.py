"""
A utility that concat two dataframes and adds a column indicating the source of each record.
This a bit odd functionality is very helpful when given two data sets
and there is uncertainty if the represent the same source.
This is common with concept drift and domain adaptation.

One can create this joint data set and use a classifier in order to try to distinguish among them.
If the classifier can do it, there are considerable differences.
An interpretable classifier can point out these differences.

If the classifier cannot distinguish between them either:
1. They represent the same source.
2. The classifier and features are not strong enough to distinguish between them.
In this case, optimistic people will hope that the difference is not strong enough to
hurt a model based on this data.
"""
import pandas as pd


def build_comparison_dataset(first_df: pd.DataFrame
                             , second_df: pd.DataFrame
                             , concept_column='is_first') -> pd.DataFrame:
    """
    :param first_df:
    :param second_df:
    :param concept_column:
            The function joins the data sets after asining the source to each one.
    :return:
    """

    first_df['concept_column'] = 1
    second_df['concept_column'] = 0

    joint = pd.concat([first_df, second_df])

    # Pandas doesn't allow second_df[concept_column] = 0
    # --> assignment to a column with a variable name
    # Therefore a temporary name is used and then renamed to the desired one
    joint = joint.rename(columns={'concept_column': concept_column})

    return joint

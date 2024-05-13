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

from analysis_utils.ml_utils import build_and_eval_model, get_predictive_columns

def build_comparison_dataset(first_df: pd.DataFrame
                             , second_df: pd.DataFrame
                             , concept_column='is_first'
                             ,should_shuffle=False) -> pd.DataFrame:
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
    if should_shuffle:
        joint = joint.sample(frac=1).reset_index(drop=True)

    return joint

def compare_datasets(first_df: pd.DataFrame
                             , second_df: pd.DataFrame
                             , classifier
                             , excluded_features=set()
                             , test_size=0.2
                             , random_state=123
                             , performance_file=None
                             , concept_column='is_first'):

    predictive_columns_func = lambda df: get_predictive_columns(df
                           , excluded_features=set(list(excluded_features) + [concept_column]))

    joint = build_comparison_dataset(first_df
                             , second_df
                             , concept_column=concept_column)

    classifier, performance = build_and_eval_model(df=joint
                         , classifier=classifier
                         , concept=concept_column
                         , test_size=test_size
                         , random_state=random_state
                         , get_predictive_columns_func=predictive_columns_func
                         , performance_file=performance_file
                         )

    return classifier, performance

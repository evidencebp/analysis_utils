import pandas as pd


def build_comparison_dataset(first_df: pd.DataFrame
                             , second_df:pd.DataFrame
                             , concept_column='is_first') -> pd.DataFrame:

    first_df['concept_column'] = 1
    second_df['concept_column'] = 0


    joint = pd.concat([first_df, second_df])
    joint = joint.rename(columns={'concept_column': concept_column})

    return joint
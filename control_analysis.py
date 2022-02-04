import math
import numpy as np
import pandas as pd
from functools import partial


def compute_functions_dict(df
                         , functions_dict
                         , verbose=False):

    stats = {}
    for i in functions_dict.keys():
        if verbose:
            print(i)
        stats[i] = [functions_dict[i](df)]

    stats_df = pd.DataFrame.from_dict(stats)

    return stats_df


def control_analysis_by_value(df
                         , functions_dict
                         , control_variable
                         , control_values=None
                         , output_file:str = None
                         , all_vall:str='All'
                         , verbose=False
                         ):
    if control_values:
        values = control_values
    else:
        values = [i for i in df[control_variable].unique() if str(i) != 'nan'] # df[control_variable].unique()

    # Compute for each control value
    dataframes = []
    for i in values:
        if verbose:
            print(i)
        fixed_df = df[df[control_variable] == i]
        controlled_df = compute_functions_dict(fixed_df
                         , functions_dict
                         , verbose=verbose)

        controlled_df[control_variable] = str(i)
        dataframes.append(controlled_df)

    # Compute for entire set
    controlled_df = compute_functions_dict(df
                     , functions_dict)

    controlled_df[control_variable] = all_vall
    dataframes.append(controlled_df)

    stats_df = pd.concat(dataframes)
    stats_df = stats_df.sort_values([control_variable])

    if output_file:
        stats_df.to_csv(output_file
                    , index=False)

    return stats_df

def check_controlled_results(df
                            , functions_columns
                            , control_variable
                            , output_file:str = None
                            , all_vall:str='All'
                            , verbose=False
                            , none_as_consistent=True):

    inconsistency = {}
    for i in functions_columns:
        if verbose:
            print(i)
        all_result = df[df[control_variable]==all_vall].iloc[0][i]
        if none_as_consistent:
            df[i+ "_consistent"] = df[i].map(lambda x: (x is None or x == '' or x==all_result))
        else:
            df[i + "_consistent"] = df[i].map(lambda x: x == all_result)
        inconsistency[i + "_inconsisetent_values"] =  str(list(df[df[i+ "_consistent"] ==False][control_variable].unique()))
        inconsistency[i + "_inconsisetent_num"] =  len(list(df[df[i+ "_consistent"] ==False][control_variable].unique()))

    inconsistency_df = pd.DataFrame.from_dict(inconsistency, orient='index').reset_index()
    inconsistency_df.columns = ['metric', 'value']

    if output_file:
        inconsistency_df.to_csv(output_file
                    , index=False)

    return inconsistency_df

def controlled_performance(df
                            , control_variable
                            , features
                            , feature_evaluation_function
                            , control_value_output_file
                            , control_summary_output_file
                            , verbose=False
                            , none_as_consistent=True):

    functions_dict = {}
    for i in sorted(features):
        functions_dict[i] = partial(feature_evaluation_function, features=[i])

    controlled_result = control_analysis_by_value(df=df
                         , functions_dict=functions_dict
                         , control_variable=control_variable
                         , output_file=control_value_output_file
                         , verbose=verbose
                         )
    inconsistency_df = check_controlled_results(df=controlled_result
                            , functions_columns=functions_dict.keys()
                            , control_variable=control_variable
                            , output_file=control_summary_output_file
                            , verbose=verbose
                            , none_as_consistent=none_as_consistent
                            )

    return inconsistency_df


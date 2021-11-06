import pandas as pd


def compute_functions_dict(df
                         , functions_dict):

    stats = {}
    for i in functions_dict.keys():
        stats[i] = [functions_dict[i](df)]

    stats_df = pd.DataFrame.from_dict(stats)

    return stats_df


def control_analysis_by_value(df
                         , functions_dict
                         , control_variable
                         , control_values=None
                         , output_file:str = None
                         , all_vall:str='All'
                         ):
    if control_values:
        values = control_values
    else:
        values = df[control_variable].unique()

    # Compute for each control value
    dataframes = []
    for i in values:
        fixed_df = df[df[control_variable] == i]
        controlled_df = compute_functions_dict(fixed_df
                         , functions_dict)

        controlled_df[control_variable] = i
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
                            , all_vall:str='All'):

    inconsistency = {}
    for i in functions_columns:
        all_result = df[df[control_variable]==all_vall].iloc[0][i]
        df[i+ "_consistent"] = df[i].map(lambda x: x==all_result)
        inconsistency[i + "_inconsisetent_values"] =  str(list(df[df[i+ "_consistent"] ==False][control_variable].unique()))
        inconsistency[i + "_inconsisetent_num"] =  len(list(df[df[i+ "_consistent"] ==False][control_variable].unique()))

    inconsistency_df = pd.DataFrame.from_dict(inconsistency, orient='index')

    if output_file:
        inconsistency_df.to_csv(output_file
                    , index=False)

    return inconsistency_df

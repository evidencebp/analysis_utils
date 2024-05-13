import pandas as pd

from analysis_utils.binning_utils import sides_binning

def evaluate_monotonocity(df : pd.DataFrame
                           , relevant_columns
                           , monotone_column
                           , monotone_order
                           , output_file:str=None):

    g = df.groupby(monotone_column, as_index=False).agg(
        {i: 'mean' for i in relevant_columns})

    monotonicity = []
    for i in relevant_columns:
        monotone = True
        for group in range(len(monotone_order) -1):

            has_prior = len(g[(g[monotone_column] == monotone_order[group])])
            if len(g[(g[monotone_column] == monotone_order[group])]):
                prior_in_order = g[(g[monotone_column] == monotone_order[group])].iloc[0][i]

            has_cur = len(g[(g[monotone_column] == monotone_order[group + 1])].iloc[0])
            if len(g[(g[monotone_column] == monotone_order[group + 1])].iloc[0]):
                cur_in_order = g[(g[monotone_column] == monotone_order[group + 1])].iloc[0][i]
            if  (has_prior and has_cur) and(prior_in_order > cur_in_order):
                monotone = False

        monotonicity.append((i, monotone))

    monotone_df = pd.DataFrame(monotonicity)
    monotone_df.columns = ['feature', 'monotonicity']
    monotone_df = monotone_df.sort_values(['monotonicity', 'feature'], ascending=[False, True])

    if output_file:
        monotone_df.to_csv(output_file
                           , index=False)

    return monotone_df

def evaluate_monotonocity_vs_concept(df : pd.DataFrame
                           , relevant_columns
                           , concepts_dict
                           , output_file_template:str=None):

    dfs = []
    for i in concepts_dict.keys():
        output_file = None
        if output_file_template:
            output_file = output_file_template.format(monotone_column=i)
        dfs.append(evaluate_monotonocity(df=df
                                            , relevant_columns=relevant_columns
                                            , monotone_column=i
                                            , monotone_order=concepts_dict[i]
                                            , output_file=output_file)
                   )
    return dfs


def evaluate_sides_monotonocity_vs_concept(df : pd.DataFrame
                           , relevant_columns
                           , concepts_list
                           , output_file_template:str=None
                           ,labels=[0,1,2]):

    side_suffix = '_SIDES'

    dfs = []
    for i in concepts_list:
        df[i + side_suffix] = sides_binning(df=df
                  , column=i
                  , labels=labels)
        output_file = None
        if output_file_template:
            output_file = output_file_template.format(monotone_column=i)
        dfs.append(evaluate_monotonocity(df=df
                                            , relevant_columns=relevant_columns
                                            , monotone_column=i + side_suffix
                                            , monotone_order=labels
                                            , output_file=output_file)
                   )
    return dfs

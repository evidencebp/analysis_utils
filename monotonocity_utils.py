import pandas as pd

def evaluate_monotonocity(df : pd.DataFrame
                           , relevant_columns
                           , monotone_column
                           , monotone_order):

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

    return monotone_df


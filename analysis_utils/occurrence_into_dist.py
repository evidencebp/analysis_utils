"""
    Takes occurrence data set (typically the result of count(*)...group by sql query)
    and turn is into distribution - adds the probability and aggregated probability.

"""

import pandas as pd

def occurrence_into_dist(df: pd.DataFrame
                         , group_column: str = None
                         , occurrence_column : str ='cnt'
                         , probability_column : str ='probability'
                         , agg_column : str ='agg_probability') -> pd.DataFrame:

    sum = df[occurrence_column].sum()
    df[probability_column] = df[occurrence_column].map(lambda x: x/sum)

    if group_column:
        df[agg_column] = 1.0
        for ind, r in df.iterrows():
            agg_sum = df[df[group_column] <= r[group_column]][occurrence_column].sum()
            df.at[ind, agg_column] = agg_sum/sum


    return df
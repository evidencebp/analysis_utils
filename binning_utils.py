"""
Utilities ofr values binning

"""

import pandas as pd

def sides_binning(df: pd.DataFrame
                  , column:str
                  , labels=[0,1,2]):
    """
        Bins values in to the lower 25%, higher 25% and the middle
    :param df:
    :param column:
    :param labels:
    :return:
    """
    quantiles = [ .25, 0.75, 1]
    quantiles_vals = [df[column].min() -1]

    for i in quantiles:
        cur_val = df[column].quantile(i)
        if len(quantiles_vals) and cur_val == max(quantiles_vals):
            # the current value is the same as the previous (e.g., when the first value is the same for 30%).
            # we choose the next value.
            cur_val = df[df[column] > cur_val][column].min()
        quantiles_vals.append(cur_val)


    return pd.cut(df[column],
            bins=quantiles_vals,
            labels=labels)
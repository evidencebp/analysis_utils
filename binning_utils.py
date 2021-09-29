"""
Utilities for values binning

"""

import pandas as pd

from cochange_analysis import the_lower_the_better

SIDES_SUFFIX = '_SIDES'

def sides_binning(df: pd.DataFrame
                  , column:str
                  , labels=[0,1,2]
                  , quantiles=[ .25, 0.75, 1]):
    """
        Bins values in to the lower 25%, higher 25% and the middle
    :param df: Dataframe to aggregate
    :param column: Columns to aggregate
    :param labels: The labels to assign to each group
    :return:
    """

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


def columns_sides_binning(df: pd.DataFrame
                  , columns
                  , labels=[0,1,2]
                  , quantiles = [ .25, 0.75, 1]):

    for i in columns:
        df[i] = sides_binning(df
                  , column=i
                  , labels=labels
                  , quantiles=quantiles)

    return df

def side_binning_by_direction(df: pd.DataFrame
                            , metrics
                            , labels=['Bad', 'Medium', 'Good'] # values should be ordered from bad to good.
                            , suffix=SIDES_SUFFIX):
    """

    :param df: The data frame with the row values of the metrics
    :param metrics: A dictionary with a "direction" function of the metric
            - the lower the better of the higher the better
    :param labels: Labels to assign to the groups. Values should be the same to all metric by their semantic meaning.
                   Hence, for the higher the better, high values should get good, the last value.
                   For the lower the better, high values should get bad, the first value.
    :param suffix: A suffix of the new tables.
    :return:
    """

    for i in metrics:

        cur_col = i + suffix
        # Checking that the metric is better when lower
        if (the_lower_the_better(1,0) == metrics[i](1,0)):
            metric_labels = labels[::-1]
        else:
            metric_labels = labels

        df[cur_col] = sides_binning(df=df
                                        , column=i
                                        , labels=metric_labels)
        df[cur_col] = df[cur_col].astype(str)

    return df

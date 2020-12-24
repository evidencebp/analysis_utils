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
    return pd.qcut(df[column],
            q=[0, .25, 0.75, 1],
            labels=labels)
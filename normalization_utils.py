import pandas as pd

def normalize_by_ref(df: pd.DataFrame
                     , ref_column:str
                     , ref_val:str
                     , features):
    """
        Normalize a datafarem by the value of a certain row.
        Make the values relative to this row.
    :param df: Datafarme to normalize
    :param ref_column: The column by which the normalization row is found
    :param rev_val: The value of the normalization row
    :param features: The features to normalize
    :return:
    """

    ndf = df.copy()

    for i in features:
        ndf[i] = df[i]/df[df[ref_column] == ref_val][i].iloc[0]

    return ndf

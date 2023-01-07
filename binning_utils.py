"""
Utilities for values binning

"""

import pandas as pd

from cochange_analysis import the_lower_the_better
from feature_pair_analysis import pair_features_vs_concept, features_stats_to_cm_df
from ml_utils import extract_relevent_features

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



def analyze_halves_prediction_of_concept(df
                                        , concept
                                        , features=None
                                        , na_val=None
                                        , output_file=None
                                        , verbose=False):
    """

        Splits all features to two halves and computes their confusion matrix
    :param df: A dataframe with feature
    :param concept: the name of the concept column
    :param features: The list of features to use as classifiers. If None relevant features are used
    :param na_val: A replacement for na values (optional)
    :param output_file: output file for the statistics (optional)
    :param verbose: Log computation
    :return: a dataframe with the confusion metrics statistics
    """

    if features is None:
        features = extract_relevent_features(df)

    df = df[~df[concept].isnull()]
    if na_val:
        df = df.fillna(na_val)

    df = columns_sides_binning(df=df
                  , columns=features + [concept]
                  , labels=[0,1]
                  , quantiles = [ .5, 1])

    for i in features + [concept] :
        df[i] = df[i].map(lambda x: True if x == 1 else False)

    stats = pair_features_vs_concept(df
                             , features=set(features) - {concept}
                             , concept=concept
                             , verbose=verbose
                             )
    stats_df = features_stats_to_cm_df(stats)

    if output_file:
        stats_df.to_csv(output_file)

    return stats_df

def analyze_halves_prediction_of_concepts(df
                                        , concepts
                                        , features=None
                                        , na_val=None
                                        , output_template=None
                                        , verbose=False):
    """
        Compute confusion matrices of a list of concepts with features

    :param df: A dataframe with feature
    :param concept: the name of the concept column
    :param na_val: A replacement for na values (optional)
    :param output_file: output file for the statistics (optional)
    :param verbose: Log computation
    :return: a dataframe with the confusion metrics statistics

    :param df: A dataframe with feature
    :param concepts: A list of the names of the concept columns
    :param features:
    :param na_val:
    :param output_template:
    :param verbose:
    :return:
    """

    for i in concepts:

        if verbose:
            print("Computing halve predictions of {concept}".format(concept=i))

        analyze_halves_prediction_of_concept(df
                                                , concept=i
                                                , features=features
                                                , na_val=na_val
                                                , output_file=None if output_template is None else
                                                    output_template.format(concept=i)
                                                , verbose=verbose)


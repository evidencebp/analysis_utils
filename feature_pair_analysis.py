import json
import numpy as np
import os
import pandas as pd

from confusion_matrix import ConfusionMatrix


def pair_analysis(df
                       , first_metric
                       , second_metric
                       , metrics=None):
    ldf = df.copy()
    result = {}
    if ((df[first_metric].dtype in (np.float64, np.int64)) and
            (df[second_metric].dtype in (np.float64, np.int64))):
        if metrics is None or 'Pearson' in metrics:
            result['Pearson'] = ldf.corr()[first_metric][second_metric]
        if metrics is None or 'Samples' in metrics:
            result['Samples'] = len(ldf)
        if metrics is None or 'avg_diff' in metrics:
            ldf['diff'] = ldf[first_metric] - ldf[second_metric]
            result['avg_diff'] = ldf['diff'].mean()
        if metrics is None or 'abs_avg_diff' in metrics:
            ldf['diff'] = ldf[first_metric] - ldf[second_metric]
            ldf['abs_diff'] = ldf['diff'].map(lambda x: abs(x))
            result['abs_avg_diff'] = ldf['abs_diff'].mean()
    elif (df[first_metric].dtype in (np.float64, np.int64)):

        q95 = ldf[first_metric].quantile(0.95)
        capped_metric = 'capped_95_' + first_metric
        ldf[capped_metric] = ldf[first_metric].map(lambda x: q95 if x > q95 else x)
        g = ldf.groupby([second_metric]).agg(mean=(first_metric, 'mean')
                                            , std=(first_metric, 'std')
                                            , count=(first_metric, 'count')
                                            , mean_capped_95 = (capped_metric, 'mean')
                                            , std_capped_95 = (capped_metric, 'std')
                                            , count_capped_95 = (capped_metric, 'count')
                                            #, min=(first_metric, 'min')
                                            #, max=(first_metric, 'max')
                                            )

        result = g.to_json()
    elif (df[second_metric].dtype in (np.float64, np.int64)):
        # Symetric version of the case above
        q95 = ldf[second_metric].quantile(0.95)
        capped_metric = 'capped_95_' + second_metric
        ldf[capped_metric] = ldf[second_metric].map(lambda x: q95 if x > q95 else x)

        g = ldf.groupby([first_metric]).agg(mean=(second_metric, 'mean')
                                            , std=(second_metric, 'std')
                                            , count=(second_metric, 'count')
                                            , mean_capped_95=(capped_metric, 'mean')
                                            , std_capped_95=(capped_metric, 'std')
                                            , count_capped_95=(capped_metric, 'count')
                                            #, min=(second_metric, 'min')
                                            # , max=(second_metric, 'max')
                                            )

        result = g.to_json()
    elif ((df[first_metric].nunique() < 3) and (df[first_metric].dtype == 'bool')
          and (df[second_metric].nunique() < 3) and (df[second_metric].dtype == 'bool')):
        count_column = 'count'
        g = ldf.groupby([first_metric
                            , second_metric], as_index=False).size().reset_index(name=count_column)

        cm = ConfusionMatrix(g_df=g
        , classifier = first_metric
        , concept = second_metric, count = count_column)
        result = cm.summarize()
    else:
        count_column = 'count'
        g = ldf.groupby([first_metric
                            , second_metric], as_index=False).size().reset_index(name=count_column)
        result = g.to_json()

    return result

def pair_analysis_by_value(df
                       , first_metric
                       , second_metric
                       , fixed_variable
                       , fixed_values=None
                         ):

    analysis_results = {}
    if fixed_values:
        values = fixed_values
    else:
        values = df[fixed_variable].unique()

    for i in values:
        cur_df = df[df[fixed_variable] == i]
        result = pair_analysis(df=cur_df
         , first_metric=first_metric
         , second_metric=second_metric)
        analysis_results[i] = result
        
    return analysis_results

def pretty_print(parsed):
    print(json.dumps(parsed, indent=4, sort_keys=True))

def bin_metric_by_quantiles(df
                          , first_metric
                          , output_metric
                          , bins=10
                          , top_val=np.inf
                            ):
    cuts = sorted([0.0] + [df[first_metric].quantile((1.0/bins)*i) for i in range(1, bins)] + [top_val])
    #print(cuts)
    df[output_metric] = pd.cut(df[first_metric]
                               , cuts
                               , duplicates='drop')

    return df

def pair_analysis_by_bins(df
                       , first_metric
                       , second_metric
                       , bins=10
                       , metrics=None):
    ldf = df.copy()
    output_metric = first_metric + "_by_" + str(bins)
    ldf = bin_metric_by_quantiles(df=ldf
                          , first_metric=first_metric
                          , output_metric=output_metric
                          , bins=bins
                            )
    return pair_analysis(ldf
                  , output_metric
                  , second_metric
                  , metrics=metrics)

def pair_analysis_by_bins_to_file(df
                       , first_metric
                       , second_metric
                       , output_file
                       , bins=10
                                  ):
    ldf = df.copy()
    output_metric = first_metric + "_by_" + str(bins)
    ldf = bin_metric_by_quantiles(df=ldf
                          , first_metric=first_metric
                          , output_metric=output_metric
                          , bins=bins
                            )
    g = ldf.groupby([output_metric]).agg(mean=(second_metric, 'mean')
                                        , std=(second_metric, 'std')
                                        , count=(second_metric, 'count')
                                        )

    g.to_csv(output_file)


def pair_features_vs_concept(df
                       , features
                       , concept
                       , metrics=None):
    """
        Computes each of the features with respect o the concept on the data frame.
    :param df:
    :param features:
    :param concept:
    :param metrics:
    :return:
    """
    result = {}
    for i in features:
        result[i] = pair_analysis(df
                      , i
                      , concept
                      , metrics=metrics)

    return result

def features_stats_to_cm_df(features_stats):
    """
        Selects the confusion matrix stats (identified by accuracy)
        and provide them as a data frame.
    :param features_stats:
    :return:
    """

    cm_features = {}
    for i in features_stats.keys():
        if "accuracy" in features_stats[i]:
            cm_features[i] = features_stats[i]

    cm_df = pd.DataFrame(cm_features)
    cm_df = cm_df.T

    return cm_df

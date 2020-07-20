import pandas as pd

from confusion_matrix import ConfusionMatrix, ifnull, safe_divide
from stability_analysis import build_two_years_df, PREV_PREFIX, CUR_PREFIX


IMPROVED_PREFIX = 'improved_'
MAIN_METRIC_POS = 0

def cochange_analysis(per_year_df
                         , metrics_dict
                         , keys
                         , control_variables=[]
                         ):
    metrics_names = [*metrics_dict]
    two_years = build_two_years_df(metric_per_year_df=per_year_df
                       , metrics=metrics_names
                       , keys=keys
                       , control_variables=control_variables)

    main_metric =  metrics_names[MAIN_METRIC_POS]
    two_years[IMPROVED_PREFIX + main_metric] = two_years.apply(lambda x: metrics_dict[main_metric](x[PREV_PREFIX + main_metric]
                                                                       , x[CUR_PREFIX + main_metric])
                                , axis=1
                                )

    stats = {}
    for i in metrics_names[MAIN_METRIC_POS + 1:]:
        improved_first_metric = IMPROVED_PREFIX + i
        two_years[improved_first_metric] = two_years.apply(lambda x: metrics_dict[i](x[PREV_PREFIX + i], x[CUR_PREFIX +i])
            , axis=1
        )
        stats[i] = features_confusion_matrix_analysis(two_years
                       , improved_first_metric
                       , IMPROVED_PREFIX + main_metric
                       , keys)

    return stats


def features_confusion_matrix_analysis(two_years_df
                       , first_metric
                       , second_metric
                       , keys):
    g = two_years_df.groupby([first_metric, second_metric]
                             , as_index=False).agg({keys[0] : 'count'})

    cm = ConfusionMatrix(g_df=g
                             , classifier=first_metric
                             , concept=second_metric, count=keys[0])

    return cm.summarize()

def cochange_analysis_by_value(per_year_df
                         , metrics_dict
                         , fixed_variable
                         , fixed_values
                         , keys
                         , control_variables=[]
                         ):
    stats = {}

    for i in fixed_values:
        fixed_per_year_df = per_year_df[per_year_df[fixed_variable] == i]
        stats[i] = cochange_analysis(per_year_df=fixed_per_year_df
                          , metrics_dict=metrics_dict
                          , keys=keys
                          , control_variables=control_variables
                          )
    return stats



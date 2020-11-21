import pandas as pd

from confusion_matrix import ConfusionMatrix, ifnull, safe_divide
from stability_analysis import build_two_years_df, PREV_PREFIX, CUR_PREFIX


IMPROVED_PREFIX = 'improved_'
MAIN_METRIC_POS = 0

def the_lower_the_better(prev
                         , cur
                         , required_gap=0):

    return (prev - required_gap) > cur


def the_higher_the_better(prev
                         , cur
                         , required_gap=0):
    return prev < (cur - required_gap)


def cochange_analysis(per_year_df
                        , metrics_dict
                        , keys
                        , control_variables=[]
                        , min_cnt_column=None
                        , min_cnt_threshold=None
                      ):
    metrics_names = [*metrics_dict]

    if min_cnt_column:
        per_year_df = per_year_df[per_year_df[min_cnt_column] >= min_cnt_threshold]

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


def cochange_to_df(stats
                   , outputfile=None
                   , lead_column='metric'):
    stats_df = pd.DataFrame.from_dict(stats, orient='index')
    stats_df = (stats_df.reset_index()).rename(columns={'index': lead_column})
    stats_df = stats_df.sort_values(['precision_lift',lead_column]
                                        , ascending=[False, True])
    if outputfile:
        stats_df.to_csv(outputfile
                    , index=False)
    return stats_df


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


def cochange_by_value_to_df(stats
                            , fixed_variable
                            , outputfile=None
                            , lead_column='metric'
                            ):
    dataframes = []
    for i in stats.keys():
        df= cochange_to_df(stats[i]
                       , outputfile=None
                       , lead_column='metric')
        df[fixed_variable] = i
        dataframes.append(df)

    stats_df = pd.concat(dataframes)

    if outputfile:
        stats_df.to_csv(outputfile
                    , index=False)

    return stats_df

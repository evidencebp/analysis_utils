import numpy as np
import pandas as pd

PREV_PREFIX = 'prev_'
CUR_PREFIX = 'cur_'

from regression_utils import pred_by_rel_distance

def analyze_stability(metric_per_year_df
                      , keys
                      , metrics
                      , time_column='year'
                      , minimal_time=-1
                      , control_variables=[]
                      , min_cnt_column=None
                      , min_cnt_threshold=None):

    if min_cnt_column:
        metric_per_year_df = metric_per_year_df[metric_per_year_df[min_cnt_column] >= min_cnt_threshold]

    two_years_df = build_two_years_df(metric_per_year_df=metric_per_year_df
                       , keys=keys
                       , metrics=metrics
                       , time_column=time_column
                       , minimal_time=minimal_time
                       , control_variables=control_variables
                                      )
    all_stats = {}
    for i in metrics:
        cur_metric = CUR_PREFIX + i
        prev_metric = PREV_PREFIX + i
        stats = {}
        stats['Pearson'] = two_years_df.corr()[cur_metric][prev_metric]

        two_years_df['diff'] = two_years_df[cur_metric] - two_years_df[prev_metric]
        stats['diff_avg'] = two_years_df['diff'].mean()
        stats['diff_std'] = two_years_df['diff'].std()

        two_years_df['relative_diff'] = two_years_df['diff'].divide(two_years_df[prev_metric])
        two_years_df.loc[~np.isfinite(two_years_df['relative_diff']), 'relative_diff'] = np.nan
        stats['relative_diff_avg'] = two_years_df['relative_diff'].mean()
        stats['relative_diff_std'] = two_years_df['relative_diff'].std()


        two_years_df['abs_diff'] = two_years_df['diff'].map(abs)
        stats['abs_diff_avg'] = two_years_df['abs_diff'].mean()
        stats['abs_diff_std'] = two_years_df['abs_diff'].std()

        two_years_df['abs_relative_diff'] = two_years_df['abs_diff'].divide(two_years_df[prev_metric])
        two_years_df.loc[~np.isfinite(two_years_df['abs_relative_diff']), 'abs_relative_diff'] = np.nan
        stats['abs_relative_diff_avg'] = two_years_df['abs_relative_diff'].mean()
        stats['abs_relative_diff_avg'] = two_years_df['abs_relative_diff'].std()

        stats['pred_05'] = pred_by_rel_distance(y_test=two_years_df[prev_metric]
                             , test_pred=two_years_df[cur_metric]
                             , threshold=0.05)
        stats['pred_25'] = pred_by_rel_distance(y_test=two_years_df[prev_metric]
                             , test_pred=two_years_df[cur_metric]
                             , threshold=0.25)
        stats['pred_50'] = pred_by_rel_distance(y_test=two_years_df[prev_metric]
                             , test_pred=two_years_df[cur_metric]
                             , threshold=0.50)

        all_stats[i] = stats.copy()

    return all_stats

def build_two_years_df(metric_per_year_df
                       , keys
                       , metrics
                       , time_column='year'
                       , minimal_time=-1
                       , control_variables=[]):

    metric_per_year_df = metric_per_year_df[keys + metrics + [time_column] + control_variables]
    #metric_per_year_df = metric_per_year_df.dropna() # TODO - drops all
    metric_per_year_df = metric_per_year_df[metric_per_year_df[time_column] >= minimal_time]

    cur_df = metric_per_year_df.copy()
    cur_df[PREV_PREFIX + 'year'] = cur_df[time_column] -1
    cur_update = {time_column : CUR_PREFIX +'year'}
    cur_update.update(generate_rename_map(metrics
                        , prefix=CUR_PREFIX))
    cur_df = cur_df.rename(columns=cur_update)

    prev_df = metric_per_year_df.copy()
    prev_update = {time_column : PREV_PREFIX + 'year'}
    prev_update.update(generate_rename_map(metrics
                        , prefix=PREV_PREFIX))
    prev_df = prev_df.rename(columns=prev_update)

    two_years = pd.merge(cur_df, prev_df
                         , left_on=keys +[PREV_PREFIX + 'year'] + control_variables
                         , right_on=keys + [PREV_PREFIX + 'year'] + control_variables)

    return two_years

def generate_rename_map(metrics
                        , prefix):
    rename_map = {}
    for i in metrics:
        rename_map[i] = prefix + i

    return rename_map
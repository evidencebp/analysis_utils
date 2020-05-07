import pandas as pd

def analyze_stability(metric_per_year_df
                      , key
                      , metric_name
                      , time_column='year'
                      , minimal_time=-1
                      , control_variables=[]
                      , min_cnt_column=None
                      , min_cnt_threshold=None):

    if min_cnt_column:
        metric_per_year_df = metric_per_year_df[metric_per_year_df[min_cnt_column] >= min_cnt_threshold]
    stats = {}
    two_years_df = build_two_years_df(metric_per_year_df=metric_per_year_df
                       , key=key
                       , metric_name=metric_name
                       , time_column=time_column
                       , minimal_time=minimal_time
                       , control_variables=control_variables
                                      )

    stats['Pearson'] = two_years_df.corr()['cur_' + metric_name]['prev_' + metric_name]

    two_years_df['diff'] = two_years_df['cur_' + metric_name] - two_years_df['prev_' + metric_name]
    stats['diff_avg'] = two_years_df['diff'].mean()
    stats['diff_std'] = two_years_df['diff'].std()

    two_years_df['abs_diff'] = two_years_df['diff'].map(abs)
    stats['abs_diff_avg'] = two_years_df['abs_diff'].mean()
    stats['abs_diff_std'] = two_years_df['abs_diff'].std()

    return stats

def build_two_years_df(metric_per_year_df
                       , key
                       , metric_name
                       , time_column='year'
                       , minimal_time=-1
                       , control_variables=[]):

    metric_per_year_df = metric_per_year_df[[key, time_column, metric_name] + control_variables]
    metric_per_year_df = metric_per_year_df.dropna()
    metric_per_year_df = metric_per_year_df[metric_per_year_df[time_column] >= minimal_time]

    cur_df = metric_per_year_df.copy()
    cur_df['prev_year'] = cur_df[time_column] -1
    cur_df = cur_df.rename(columns={time_column : 'cur_year'
        , metric_name : 'cur_' + metric_name})

    prev_df = metric_per_year_df.copy()
    prev_df = prev_df.rename(columns={time_column : 'prev_year'
        , metric_name : 'prev_' + metric_name})

    two_years = pd.merge(cur_df, prev_df
                         , left_on=[key, 'prev_year'] + control_variables
                         , right_on=[key, 'prev_year'] + control_variables)

    return two_years


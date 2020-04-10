import pandas as pd

from confusion_matrix import ConfusionMatrix, ifnull, safe_divide


def cochange_preperation(cochange_file
                         , first_metric
                         , second_metric
                         , first_the_higher_the_better
                         , second_the_higher_the_better
                         , first_sig_threshold
                         , second_sig_threshold
                         , key='repo_name'
                         ):

    print("Over the years", first_metric, " and ", second_metric," co-change")
    per_year_df= build_repo_per_year_df(cochange_file
                           , key)
    cochange_analysis(per_year_df
                      , first_metric
                      , second_metric
                      , first_the_higher_the_better
                      , second_the_higher_the_better
                      , first_sig_threshold
                      , second_sig_threshold
                      , key='repo_name'
                      )

def cochange_analysis(per_year_df
                         , first_metric
                         , second_metric
                         , first_the_higher_the_better
                         , second_the_higher_the_better
                         , first_sig_threshold
                         , second_sig_threshold
                         , key='repo_name'
                         , control_variables=[]
                         ):

    two_years = build_two_years_df(per_year_df=per_year_df
                       , first_metric=first_metric
                       , second_metric=second_metric
                       , key=key
                       , control_variables=control_variables)

    improved_first_metric = 'improved_' + first_metric
    improved_sig_first_metric = 'improved_sig_' + first_metric
    if first_the_higher_the_better:
        two_years[improved_first_metric] = two_years['cur_' + first_metric] > two_years['prev_' + first_metric]
        two_years[improved_sig_first_metric] = two_years['cur_' + first_metric] > two_years['prev_' + first_metric]\
                                               + first_sig_threshold
    else:
        two_years[improved_first_metric] = two_years['cur_' + first_metric] < two_years['prev_' + first_metric]
        two_years[improved_sig_first_metric] = two_years['cur_' + first_metric] < two_years['prev_' + first_metric]\
                                               - first_sig_threshold

    improved_second_metric = 'improved_' + second_metric
    improved_sig_second_metric = 'improved_sig_' + second_metric
    if second_the_higher_the_better:
        two_years[improved_second_metric] = two_years['cur_' + second_metric] > two_years['prev_' + second_metric]
        two_years[improved_sig_second_metric] = two_years['cur_' + second_metric] > two_years['prev_' + second_metric]\
                                               + second_sig_threshold
    else:
        two_years[improved_second_metric] = two_years['cur_' + second_metric] < two_years['prev_' + second_metric]
        two_years[improved_sig_second_metric] = two_years['cur_' + second_metric] < two_years['prev_' + second_metric]\
                                               - second_sig_threshold

    two_years_analysis(two_years
                       , improved_first_metric
                       , improved_second_metric
                       , key)


    two_years_analysis(two_years
                       , improved_sig_first_metric
                       , improved_sig_second_metric
                       , key)


def two_years_analysis(two_years_df
                       , first_metric
                       , second_metric
                       , key):
    print()
    print("Co-change"
          , first_metric
          , second_metric)
    g = two_years_df.groupby([first_metric, second_metric]
                             , as_index=False).agg({key : 'count'})

    print(g)

    cm = ConfusionMatrix(g_df=g
                             , classifier=first_metric
                             , concept=second_metric, count=key)

    print(cm.summarize())
    print()
    print("Samples", cm.samples())
    print("Both metrics increment match", cm.accuracy())
    print(second_metric
            , " improvement given "
            , first_metric
            , " improvement", cm.precision(), "lift", cm.precision_lift())
    print(first_metric
            , " improvement given "
            , second_metric
            , "improvement",  cm.recall(), "lift", ifnull(safe_divide(ifnull(cm.recall()),cm.hit_rate())) - 1)
    print()

def build_two_years_df(per_year_df
                       , first_metric
                       , second_metric
                       , key
                       , control_variables=[]):

    per_year_df = per_year_df[[key, 'year', first_metric, second_metric] + control_variables]
    per_year_df = per_year_df.dropna()

    cur_df = per_year_df.copy()
    cur_df['prev_year'] = cur_df.year -1
    cur_df = cur_df.rename(columns={'year' : 'cur_year'
        , first_metric : 'cur_' + first_metric
        , second_metric : 'cur_' + second_metric})

    prev_df = per_year_df.copy()
    prev_df = prev_df.rename(columns={'year' : 'prev_year'
        , first_metric : 'prev_' + first_metric
        , second_metric : 'prev_' + second_metric})

    two_years = pd.merge(cur_df, prev_df
                         , left_on=[key, 'prev_year'] + control_variables
                         , right_on=[key, 'prev_year'] + control_variables)

    return two_years


def build_repo_per_year_df(cochange_file
                           , key
                           , earliaest_analyzed_year=-1
                           , control_variables=[]):
    trep = get_valid_repos()
    trep = trep[[key] + control_variables]
    cochange_df = pd.read_csv(cochange_file)
    cochange_df = cochange_df[cochange_df.year > earliaest_analyzed_year]
    df = pd.merge(cochange_df, trep, on=key)

    return df


def cochange_analysis_by_value(per_year_df
                         , first_metric
                         , second_metric
                         , first_the_higher_the_better
                         , second_the_higher_the_better
                         , first_sig_threshold
                         , second_sig_threshold
                         , fixed_variable
                         , fixed_values
                         , key='repo_name'
                         , control_variables=[]
                         ):
    print()
    print("Co-change analysis by ", fixed_variable)
    print()

    for i in fixed_values:
        print()
        print("Co-change analysis for value", i, " of ", fixed_variable)
        fixed_per_year_df = per_year_df[per_year_df[fixed_variable] == i]
        cochange_analysis(per_year_df=fixed_per_year_df
                          , first_metric=first_metric
                          , second_metric=second_metric
                          , first_the_higher_the_better=first_the_higher_the_better
                          , second_the_higher_the_better=second_the_higher_the_better
                          , first_sig_threshold=first_sig_threshold
                          , second_sig_threshold=second_sig_threshold
                          , key=key
                          , control_variables=control_variables
                          )



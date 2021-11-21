import pandas as pd

from stability_analysis import build_two_years_df

def build_two_steps_ds(metric_per_year_df
                       , keys
                       , metrics
                       , time_column='year'
                       , minimal_time=-1
                       , control_variables=[]):

    joint = build_two_years_df(metric_per_year_df
                       , keys
                       , metrics
                       , time_column='year'
                       , minimal_time=-1
                       , control_variables=[])

    for i in metrics:
        joint['rel_'+ i] = joint.apply(lambda x: None if (x['prev_'+ i] is None or x['prev_'+ i] ==0) else
                                                    (x['cur_'+ i] - x['prev_'+ i])/x['prev_'+ i]
            , axis=1
        )

    return joint

if __name__ == "__main__":
    metric_per_year_df = pd.DataFrame([(2021, 'a', 200, 150)
                                        , (2020, 'a', 100, 50)
                                        , (2019, 'a', 50, 50)
                                        , (2019, 'b', 100, 50)
                                        , (2018, 'b', 50, 50)
                                        , (2019, 'c', 100, 50)
                                        , (2018, 'b', None, 0)
                                       ]
                                   , columns=['year', 'repo_name', 'commits', 'authors'])
    keys=['repo_name']
    metrics=['commits', 'authors']

    joint = build_two_steps_ds(metric_per_year_df
                       , keys
                       , metrics
                       , time_column='year'
                       , minimal_time=-1
                       , control_variables=[])
    print(joint)
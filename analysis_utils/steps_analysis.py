import pandas as pd

from analysis_utils.stability_analysis import build_two_years_df

def build_two_steps_ds(metric_per_year_df
                       , keys
                       , metrics
                       , time_column='year'):

    joint = build_two_years_df(metric_per_year_df
                       , keys
                       , metrics
                       , time_column=time_column
                       , minimal_time=-1
                       , control_variables=[])

    for i in metrics:
        joint['rel_'+ i] = joint.apply(lambda x: None if (x['prev_'+ i] is None or x['prev_'+ i] ==0) else
                                                    (x['cur_'+ i] - x['prev_'+ i])/x['prev_'+ i]
            , axis=1
        )

    return joint

import os
import pandas as pd
import time
from typing import Callable, Dict

def perform_regression_ablations(df : pd.DataFrame
                                    , ablations : Dict
                                    , regressors : Dict
                                    , build_basic_model : Callable
                                    , performance_path : str = ''):

    results = []
    cur_round :int = 1
    rounds : int = len(ablations.keys())*len(regressors.keys())
    for ablation in ablations.keys():
        print(ablation)
        for model_name in regressors.keys():
            print("Round {cur_round} out of {rounds}".format(cur_round=cur_round
                                                             , rounds=rounds))
            cur_round += 1

            print(model_name)
            start = time.time()
            regressor = regressors[model_name]
            regressor, performance = build_basic_model(df
                                                       , regressor=regressor
                                                       , model_file_name='{}.pkl'.format(model_name)
                                                       , ablation_columns=ablations[ablation]
                                                       , performance_file=os.path.join(performance_path
                                                                                       , '{}.json'.format(model_name))
                                                       )

            results.append((regressor, performance))
            print(performance)
            end = time.time()
            print("Model duration", end - start)

    return results

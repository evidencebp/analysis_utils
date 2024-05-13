"""
A utility for ablations, the performance of models when some of the features are being removed.
"""

import os
import time
from typing import Callable, Dict
import pandas as pd

def perform_regression_ablations(df: pd.DataFrame
                                 , ablations: Dict
                                 , classifiers: Dict
                                 , build_basic_model: Callable
                                 , performance_path: str = ''):
    """

    :param df: the data set to use
    :param ablations: a dictionary with sets of features to remove
    :param classifiers: classifiers to use for model building
    :param build_basic_model: A reference to a function that builds and evaluate a model
    (see common implementation in ml_utils).
    :param performance_path: The directory of performance results.
    :return:
    """

    results = []
    cur_round: int = 1
    rounds: int = len(ablations.keys())*len(classifiers.keys())

    for ablation in ablations.keys():
        print(ablation)
        for model_name in classifiers.keys():
            print("Round {cur_round} out of {rounds}".format(cur_round=cur_round
                                                             , rounds=rounds))
            cur_round += 1

            print(model_name)
            start = time.time()
            classifier = classifiers[model_name]
            classifier, performance = build_basic_model(df
                                           , regressor=classifier
                                           , model_file_name='{}.pkl'.format(model_name)
                                           , ablation_columns=ablations[ablation]
                                           , performance_file=os.path.join(performance_path
                                                                    , '{}.json'.format(model_name))
                                           )

            results.append((classifier, performance))
            print(performance)
            end = time.time()
            print("Model duration", end - start)

    return results

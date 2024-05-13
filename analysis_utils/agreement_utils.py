"""
A utility to compute agreement between concepts and metric.
For each metric, the agreement is computed with each concept.

The basic definition of agreement is accuracy.
That works well for categorial values.

For continuous values we use side binning first, yet other categorizations are also ok.

"""

import pandas as pd
from sklearn.metrics import accuracy_score

from analysis_utils.binning_utils import sides_binning, side_binning_by_direction, SIDES_SUFFIX


def compute_agreement(df: pd.DataFrame
                       , concepts
                       , metrics):
    """
    Computes the accuracy between concepts and metrics.

    :param df: The data frame containing the metrics and concepts
    :param concepts: A *dictionary* of concepts. Each concept dictionary value is a direction function
                    (the_lower_the_better/the_higher_the_better).
    :param metrics: A *dictionary* of metrics. Each metric dictionary value is a direction function
                    (the_lower_the_better/the_higher_the_better).
                    The metrics can include the concepts.
    :return: A data frame of the accuracy of concepts with respect to metrics.
    """

    rows = []

    for metric in metrics:

        row = [metric]

        for concept in concepts:
            agreement = accuracy_score(df[metric]
                                       , df[concept])
            row.append(agreement)

        rows.append(row)

    agreement_df = pd.DataFrame(rows
                               , columns=['metric'] + concepts).sort_values('metric')

    return agreement_df


def agreement_with_concepts(df
                          , concepts
                          , metrics
                          , stats_file=None
                          , suffix=SIDES_SUFFIX):
    """
    Does sides binning for categorial concepts and compute accuracy on them.

    :param df: The data frame containing the metrics and concepts
    :param concepts: A *dictionary* of concepts. Each concept dictionary value is a direction function
                    (the_lower_the_better/the_higher_the_better).
    :param metrics: A *dictionary* of metrics. Each metric dictionary value is a direction function
                    (the_lower_the_better/the_higher_the_better).
                    The metrics can include the concepts.
    :return: A data frame of the accuracy of concepts with respect to metrics.

    :param stats_file: Location to store the result, None if not needed.
    :param suffix: A suffix for the side_binning resulting columns.
    :return: A data frame of the accuracy of concepts with respect to metrics, on the side_binning values.
    """

    df = side_binning_by_direction(df
                            , metrics=metrics
                            , suffix=suffix)

    agreement_df = compute_agreement(df
                       , [i + suffix for i in concepts.keys()]
                       , [i + suffix for i in metrics.keys()])
    if stats_file:
        agreement_df.to_csv(stats_file
                            , index=False)

    return agreement_df

"""
Computes the Pearson correlation between a concept and a list of metrics
"""
from typing import List

import pandas as pd


StringsList = List[str]


def analyze_correlation(metrics_df: pd.DataFrame
                        , concept_column: str
                        , metrics: StringsList
                        , correlation_stats_file: str = None
                        , concept_display: str = None):
    """
    :param metrics_df: A data frame of the entities
    :param concept_column: The column with respect to we compute correlation
    :param metrics: The metrics to compute correlation with the concept
    :param correlation_stats_file: Where to store the results
    :return:
    """

    stats_df = metrics_df[metrics].corr()[concept_column]
    if not concept_display:
        concept_display = "Preason_with_" + concept_column
    stats_df = stats_df.reset_index()
    stats_df = stats_df.rename(columns={'index': 'metric'
                                                            , concept_column : concept_display})
    stats_df = stats_df.sort_values([concept_display, 'metric'], ascending=[False, True])
    if correlation_stats_file:
        stats_df.to_csv(correlation_stats_file
                        , index=False)

    return stats_df

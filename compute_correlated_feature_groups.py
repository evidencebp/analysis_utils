import os
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

from configuration import DATA_PATH, PIVOT_FILE


def high_correlations(correlations
                      , threshold=0.7):
    high_correlations = correlations.copy()
    for i in high_correlations.columns:
        try:
            high_correlations[i] = high_correlations[i] > threshold
            high_correlations[i]= high_correlations[i].astype(int)
        except:
            # Non numeric columns
            pass

    return high_correlations

def compute_features_groups(columns_names
                           , n_components
                           , labels):
    components = []
    for group in range(n_components):
        curr = [columns_names[i] for i in range(len(labels)) if labels[i] == group]
        if len(curr) > 1:
            components.append(curr)

    return components

def graph_to_groups(graph
                    , columns_names):
    graph = csr_matrix(graph)

    n_components, labels = connected_components(csgraph=graph, directed=False, return_labels=True)

    return compute_features_groups(columns_names
                            , n_components
                            , labels)

def compute_correlated_feautre_groups(df
                            , threshold=0.7):
    df = df.fillna(0)
    correlations = df.corr()
    correlations = correlations.fillna(0)
    hcorr = high_correlations(correlations
                              , threshold=threshold)

    graph = csr_matrix(hcorr)
    print(graph)

    n_components, labels = connected_components(csgraph=graph, directed=False, return_labels=True)

    return compute_features_groups(hcorr.columns
                            , n_components
                            , labels)


"""
Finding groups of related features.
Features are related if their Pearson correlation is above a threshold.
Features are in a group of related features if they belong to the same connected component.
The connected components are on a graph of features where node are connected
if they have high correlation.
Not that features A and B might be in the same connected component even if
they are not correlated if they both correlated with the feature C.
"""

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


def high_correlations(correlations
                      , threshold=0.7):
    """
        Computes the induced graph.
        A correlation is high if it is above the threshold
    :param correlations:
    :param threshold:
    :return:
    """
    high_correlations_graph = correlations.copy()
    for i in high_correlations_graph.columns:
        try:
            high_correlations_graph[i] = high_correlations_graph[i] > threshold
            high_correlations_graph[i] = high_correlations_graph[i].astype(int)
        except Exception as e:
            # Non numeric columns
            print("Not including feature ", i, e)

    return high_correlations_graph

def compute_features_groups(columns_names
                           , n_components
                           , labels):
    """
        Translate groups indices into names.
    :param columns_names:
    :param n_components:
    :param labels:
    :return:
    """
    components = []
    for group in range(n_components):
        curr = [columns_names[i] for i in range(len(labels)) if labels[i] == group]
        if len(curr) > 1:
            components.append(curr)

    return components

def graph_to_groups(graph
                    , columns_names):
    """
        Compute connected components on graphs.
    :param graph:
    :param columns_names:
    :return:
    """
    graph = csr_matrix(graph)

    n_components, labels = connected_components(csgraph=graph, directed=False, return_labels=True)

    return compute_features_groups(columns_names
                            , n_components
                            , labels)

def correlated_feature_groups(df
                            , threshold=0.7):
    """
        Compute the graph and its connected components.
    :param df:
    :param threshold:
    :return:
    """
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

def print_features_groups(features_groups
                          , translation_function=None
                          , all_features=None):

    group_num = 1
    unrelated_features = set()

    for group in features_groups:

        if all_features is not None:
            unrelated_features = set(all_features) -set(group)

        if translation_function:
            translated_group = [translation_function(i) for i in group]
        else:
            translated_group = group

        print("Group #", group_num, translated_group)
        group_num = group_num + 1

    if all_features is not None:
        if translation_function:
            print("Unrelated features", [translation_function(i) for i in unrelated_features])
        else:
            print("Unrelated features", unrelated_features)


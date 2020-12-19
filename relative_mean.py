from typing import List

import pandas as pd

StringsList = List[str]

def analyze_relative_mean(df: pd.DataFrame
                          , concepts: StringsList
                          , metrics: StringsList
                          , output_file: str = None):
    features = []
    concepts_mean = {}
    for c in concepts:
        concepts_mean[c] = df[c].mean()
        features.append('cond_mean_' + c)
        features.append('cond_mean_diff_' + c)

    feature_stats = []
    for i in metrics:
        record = []
        record.append(i)

        g = df[df[i]].groupby([i]).agg({j : 'mean' for j in concepts})
        g = g.reset_index()

        for c in concepts:
            val = None
            diff = None
            if len(g):
                val = g[c].iloc[0]
                diff = val - concepts_mean[c]
            record.append(val)
            record.append(diff)



        feature_stats.append(record)

    features_df = pd.DataFrame(feature_stats)
    features_df.columns = ['feature'] + features

    if output_file:
        features_df.to_csv(output_file
                           , index=False)

    return features_df

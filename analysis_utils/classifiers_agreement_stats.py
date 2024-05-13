from collections import Counter
from typing import List

import numpy as np
import pandas as pd


def classifiers_agreement_stats(df: pd.DataFrame
                                , classifiers_columns: List[str] = None
                                , count_column: str = 'count'):

    # Use all columns but count as default
    if not classifiers_columns:
        classifiers_columns = list(set(df.columns) - set([count_column]))

    # Find all values used by the classifiers
    classifiers_values = sorted(list(np.unique(df[classifiers_columns].values))
                                , reverse=True)

    rows = []
    for _, i in df.iterrows():
        row = []
        cnt = Counter(i[classifiers_columns])
        for col in classifiers_values:
            row.append(cnt[col])

        row.append(i[[count_column]].iloc[0])
        rows.append(row)

    df = pd.DataFrame(rows
                      , columns=(classifiers_values + [count_column]))
    g = df.groupby(classifiers_values
                   , as_index=False).agg({count_column: 'sum'}).sort_values(classifiers_values
                                                                            , ascending=False)
    cases = df[count_column].sum()
    g['probability'] = g[count_column]/cases

    return g.reset_index(drop=True)

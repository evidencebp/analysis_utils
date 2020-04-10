import os
import pandas as pd

def analyze_twins_file(twins_file
                               , match_column
                               , mismatch_column
                               , time_column='year'
                               , minimal_time=-1):
    df = pd.read_csv(twins_file)
    df = df[df[time_column]> minimal_time]
    df['pairs'] = df[match_column] + df[mismatch_column]
    df['match_ratio'] = df[match_column] / df.cap_pairs

    print(df)

    return df

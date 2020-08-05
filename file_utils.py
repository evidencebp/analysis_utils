"""
Utilities for general file handling

"""
import pandas as pd
from typing import List

Strings = List[str]

def merge_csv_files(files_list :Strings) -> pd.DataFrame:
    """
    :param files_list: List of csv file to merge
    :return: A data frame of the files content
    """

    data_frames = []
    for i in files_list:
        df = pd.read_csv(i)
        data_frames.append(df)

    joint = pd.concat(data_frames)

    return joint
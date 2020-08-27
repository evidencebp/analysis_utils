"""
Utilities for general file handling

"""
import os

from typing import List

import pandas as pd

Strings = List[str]


def merge_csv_files(files_list: Strings) -> pd.DataFrame:
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


def merge_csv_directory(files_directory: str
                        , verify_extension: bool=True) -> pd.DataFrame:
    """

    :param files_directory:
    :param verify_extension:
    :return:
    """
    files_list = [os.path.join(files_directory, file) for file in os.listdir(files_directory)]
    if verify_extension:
        files_list = [file for file in files_list if file.endswith(".csv") ]

    joint = merge_csv_files(files_list)

    return joint

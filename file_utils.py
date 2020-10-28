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
        file_df = pd.read_csv(i)
        data_frames.append(file_df)

    joint = pd.concat(data_frames)

    return joint


def merge_csv_directory(files_directory: str
                        , verify_extension: bool = True) -> pd.DataFrame:
    """

    :param files_directory: The directory containing the input files
    :param verify_extension: Whether to verify that the files end with ".csv"
    :return: A data frame of the files content
    """
    files_list = [os.path.join(files_directory, file) for file in os.listdir(files_directory)]
    if verify_extension:
        files_list = [file for file in files_list if file.endswith(".csv")]

    joint = merge_csv_files(files_list)

    return joint


def apply_function_to_file(input_file
                        , applied_function
                        , output_file=None):

    df = pd.read_csv(input_file)
    out_df = applied_function(df)

    if output_file:
        out_df.to_csv(output_file
                  , index=False)
    return out_df



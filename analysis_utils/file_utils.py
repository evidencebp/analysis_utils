"""
Utilities for general file handling

"""
import os
from os.path import join

from typing import List

import pandas as pd

Strings = List[str]
DataFrames = List[pd.DataFrame]


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
    """
        Apply a function to the row in CSV file
    :param input_file: The rows file
    :param applied_function: The applied function
    :param output_file: The file after application (if provided)
    :return: The rows after application
    """

    df = pd.read_csv(input_file)
    out_df = applied_function(df)

    if output_file:
        out_df.to_csv(output_file
                  , index=False)
    return out_df

def join_dataframes(dataframes: DataFrames
                                , keys: Strings
                                , how: str = 'inner'):
    """
        Joins the data frames into a single one based on common keys
    :param dataframes: A ist of data frames to join
    :param keys: Common keys
    :param how: Join type
    :return:
    """

    joint_df = dataframes[0]
    for i in range(1, len(dataframes)):
        joint_df = pd.merge(joint_df
                            , dataframes[i]
                            , on=keys
                            , how=how)

    return joint_df


def prefix_columns(df: pd.DataFrame
                   , prefix : str
                   , columns : list) -> pd.DataFrame :
    rename = {i: prefix + i for i in columns}
    df = df.rename(columns=rename)

    return df

def concat_text_files(file_names: Strings
                      , output_file: str
                      , input_directory: str = None):
    if input_directory:
        file_names = [join(input_directory, i) for i in file_names]
    with open(output_file, 'w') as outfile:
        for cur_file in file_names:
            with open(cur_file) as infile:
                outfile.write(infile.read())
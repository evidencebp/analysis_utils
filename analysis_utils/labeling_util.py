import pandas as pd

from typing import List
string_list = List[str]

def label_dataset(df : pd.DataFrame
                        , classifier
                        , features
                        , classifier_column : str) -> pd.DataFrame:
    """

    :param df:
    :param classifier:
    :param features: Some other features, keys, concept should be kept but not used.
    These are the feature to use in prediction.
    :param classifier_column:
    :return:
    """

    df[classifier_column] = classifier.predict(df[features])

    return df

def get_false_positives(df : pd.DataFrame
                        , classifier_column : str
                        , concept_column : str) -> pd.DataFrame:
    return df[(df[classifier_column] == True) & (df[concept_column] == False)]

def get_false_negatives(df : pd.DataFrame
                        , classifier_column : str
                        , concept_column : str) -> pd.DataFrame:
    return df[(df[classifier_column] == False) & (df[concept_column] == True)]

def get_labeling_df(keys :string_list
                    , concept : str) -> pd.DataFrame :
    """
    Create a new labeling data frame
    :return:
    """

    df = pd.DataFrame(columns=keys + [concept] + ['comment'])

    return df

def label_sample(samples_df : pd.DataFrame
                  , sample_position : int
                  , labels_df : pd.DataFrame
                  , comment : str
                  , keys :string_list
                  , concept : str) -> pd.DataFrame :

    new_dict = {}
    for i in keys:
        new_dict[i] = samples_df.iloc[sample_position][i]

    new_dict[concept] = samples_df.iloc[sample_position][concept]
    new_dict['comment'] = comment

    labels_df = labels_df.append(new_dict, ignore_index=True)
    labels_df = labels_df.drop_duplicates()

    return labels_df

def get_samples_to_label(samples_df : pd.DataFrame
                          , labels_df : pd.DataFrame
                          , keys :string_list) -> pd.DataFrame:

    df_all = samples_df.merge(labels_df[keys]
                              , on=keys
                              ,how='left'
                              , indicator=True)

    samples_to_label = df_all[(df_all._merge == 'left_only')]
    samples_to_label = samples_to_label.drop(columns=['_merge'])

    return samples_to_label

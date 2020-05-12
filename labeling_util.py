import pandas as pd


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

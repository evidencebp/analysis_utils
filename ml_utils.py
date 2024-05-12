"""
    Utilities for building machine learning models
"""
from cloudpickle import dump, load
import numpy as np
import pandas as pd
import os

from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz
import time


from analysis_utils.confusion_matrix import ConfusionMatrix, sk_to_grouped_df
from analysis_utils.transform_tree import models_to_text


def load_model(model_file_name
               , directory):
    with open(os.path.join(directory, model_file_name), 'rb') as f:
        model = load(f)

    return model

def save_model(model
               , output_file_name
               , directory):
    with open(os.path.join(directory, output_file_name), "wb") as f:
        dump(model, f)

def save_models(model_dict
               , file_name_format
               , directory):

    for model_name in model_dict.keys():
        save_model(model=model_dict[model_name]['model']
                   , output_file_name=file_name_format.format(model_name=model_name)
                   , directory=directory)


def save_performance(model_dict
                    , output_file: str = None):

    performance_dict = {}
    for model_name in model_dict.keys():
        performance_dict[model_name] =model_dict[model_name]['performance']

    df = pd.DataFrame(performance_dict)
    df = df.T.reset_index()
    df.rename(columns={'index': 'model'}
              , inplace=True)

    if output_file:
        df.to_csv(output_file
                  , index=False)

    return df


def get_predictive_columns(df
                           , excluded_features=set()):
    return sorted(list(set(df.columns.tolist()) - excluded_features))


def df_to_sk_structuring(df
                  , concept
                  , test_size
                  , random_state
                  ):
    X = df[[i for i in df.columns if i != concept]]
    y = df[concept]
    if test_size:
        X_train, X_test, y_train, y_test = train_test_split(X
                                                            , y
                                                            , test_size=test_size
                                                            , random_state=random_state)
    else:
        struct = pd.DataFrame(data=None
                              , columns=df.columns
                              , index=df.index).dropna()
        X_train = X
        X_test = struct[[i for i in struct.columns if i != concept]]

        y_train = y
        y_test = struct[concept]

    return X_test, X_train, y_test, y_train


def df_to_sk_form(df
                  , concept
                  , test_size
                  , random_state
                  , get_predictive_columns_func
                  ):
    if get_predictive_columns_func is not None:
        df = df[get_predictive_columns_func(df) + [concept]]

    return df_to_sk_structuring(df
                  , concept
                  , test_size
                  , random_state
                  )


def evaluate_model(classifier
                   , X_test
                   , y_test
                   , get_predictive_columns_func=None
                   , performance_file=None
                   , classifier_name='classifier'
                   , concept='concept'
                   , count='count'
                   ):

    if get_predictive_columns_func:
        df = X_test[get_predictive_columns_func(X_test)]
    else:
        df = X_test

    test_pred = classifier.predict(df)
    grouped_df = sk_to_grouped_df(labels=y_test
                     , predictions=test_pred
                     , classifier=classifier_name
                     , concept=concept
                     , count=count
                     )
    cm = ConfusionMatrix(classifier=classifier_name
                     , concept=concept
                     , count=count
                 , g_df=grouped_df)

    return cm.summarize(performance_file)


def train_and_eval_models_on_datasets(concept
                                      , train_df
                                      , test_df
                                      , classifiers
                                      , evaluation_function=evaluate_model
                                      , random_state=0
                                      , verbose=True):
    results = {}

    for model_name in classifiers.keys():
        if verbose:
            print(model_name)

        start = time.time()
        model = classifiers[model_name]

        _, X_train, _, y_train = df_to_sk_structuring(df=train_df
                                                      , concept=concept
                                                      , test_size=0
                                                      , random_state=random_state
                                                      )

        model.fit(X_train, y_train)

        _, X_test, _, y_test = df_to_sk_structuring(df=test_df
                                                    , concept=concept
                                                    , test_size=0
                                                    , random_state=random_state
                                                    )

        performance = evaluation_function(model
                                          , X_test
                                          , y_test)

        results[model_name] = {'model': model
            , 'performance': performance}

        end = time.time()

        if verbose:
            print("Model build time"
                  , model_name
                  , end - start)

    return results


def build_and_eval_model(df
                                , classifier
                                , concept
                                , test_size
                                , random_state
                                , get_predictive_columns_func
                                , performance_file=None
                                , evaluation_function=evaluate_model):

    X_test, X_train, y_test, y_train = df_to_sk_form(df=df
                  , concept=concept
                  , test_size=test_size
                  , random_state=random_state
                  , get_predictive_columns_func=get_predictive_columns_func)

    classifier.fit(X_train, y_train)
    performance = evaluation_function(classifier
                   , X_test
                   , y_test
                   , performance_file=performance_file
                    )

    return classifier, performance

def build_and_eval_models(df
                                , classifiers
                                , concept
                                , test_size
                                , random_state
                                , evaluation_function=evaluate_model
                                , verbose: bool = True):

    train_df, test_df = train_test_split(df
                                         , test_size=test_size)

    results = train_and_eval_models_on_datasets(concept
                                      , train_df
                                      , test_df
                                      , classifiers
                                      , evaluation_function=evaluation_function
                                      , random_state=random_state
                                      , verbose=verbose)

    return results

def same_set_build_and_eval_model(df
                                , classifier
                                , concept
                                 , random_state
                                , get_predictive_columns_func
                                , performance_file=None
                         ):
    """
        Trains and evaluate the model on the same data set, the train data set.
        Used to see if the model has enough capacity to overfit and represent
        the concept given the features.
    :param df:
    :param classifier:
    :param concept:
    :param random_state:
    :param get_predictive_columns_func:
    :param performance_file:
    :return:
    """
    _, X_train, _, y_train = df_to_sk_form(df=df
                  , concept=concept
                  , test_size=1 # Would have been zero if supported
                  , random_state=random_state
                  , get_predictive_columns_func=get_predictive_columns_func)

    classifier.fit(X_train, y_train)
    performance = evaluate_model(classifier
                   , X_train
                   , y_train
                   , performance_file=performance_file
                   , get_predictive_columns_func=get_predictive_columns_func)

    return classifier, performance

def cross_validation(df
                    , classifier
                    , concept
                    , get_predictive_columns_func
                    , scoring=None
                    , cv=None
                    , return_train_score=False
                     ):

    X_test, X_train, y_test, y_train = df_to_sk_form(df
                  , concept
                  , test_size=1
                  , random_state=0
                  , get_predictive_columns_func=get_predictive_columns_func
                  )

    cv = cross_validate(estimator=classifier
                          , X=X_train
                          , y=y_train
                          , scoring=scoring
                          , cv=cv
                          , return_train_score=return_train_score)

    test_std = cv['test_score'].std()

    if return_train_score:
        train_std = cv['train_score'].std()
        diff_mean = (cv['train_score'] - cv['test_score']).mean()
    else:
        train_std = None
        diff_mean = None

    return cv, test_std, train_std, diff_mean

def plot_tree(clf
              , dot_file_path
              , png_file_path
              , feature_names=None
              , class_names=None):
    export_graphviz(clf
                        , feature_names=feature_names
                        , out_file=dot_file_path
                        , class_names=class_names
                        , impurity=False
                        #, proportion=True
                        , filled=True
                        , rounded=True
                    )
    #dot_to_ps_command = "dot -Tps {} -o {}".format(dot_file_path
    #                                               , png_file_path)
    dot_to_png_command = "dot -Tpng {} > {}".format(dot_file_path
                                                        , png_file_path)

    os.system(dot_to_png_command)


def plot_random_forest(rf
                       , dot_files_prefix
                       , png_files_prefix
                       , feature_names=None):
    for i in range(rf.n_estimators):
        plot_tree(clf=rf.estimators_[i]
                  , dot_file_path="{}_{}.dot".format(dot_files_prefix
                                           , i)
                  , png_file_path="{}_{}.png".format(png_files_prefix
                                                    , i)
                  , feature_names=feature_names)

def extract_relevent_features(df
                              , excluded_features=[]
                              , superset=None
                              , allowed_types=[np.float64, np.int64]):
    """
        A utility to extract from a dataframe the columns suitable for ML
    :param df: A datafarme for analysis
    :param excluded_features: Optional list of feature to exclude anyway (e.g., keys)
    :param superset: A set that all selectted columns should belong to
    :param allowed_types: Allowed types of columns
    :return: list of suitable for analysis columns of the dataframe.
    """
    features = df.columns
    none_suitable_columns = excluded_features

    for i in features:
        if (df[i].dtype not in allowed_types):
            none_suitable_columns.append(i)

    features = list(set(features) - set(none_suitable_columns))
    if superset:
        features = list(set(superset).intersection(set(features)))

    return features


def build_models(df:pd.DataFrame
                          , classifiers
                          , concept
                          , test_size
                          , random_state
                          , verbose: bool = True
                          , performance_path: str = None
                          , evaluation_function=evaluate_model
                          , models_path: str = None
                          , models_format: str = None
                          , models_text_format: str = None
                          ):
    results = build_and_eval_models(df=df
                          , classifiers=classifiers
                          , concept=concept
                          , test_size=test_size
                          , random_state=random_state
                          , evaluation_function=evaluation_function
                          , verbose=verbose)

    save_performance(model_dict=results
                    , output_file=performance_path)

    if models_path and models_format:
        save_models(model_dict=results
                , file_name_format=models_format
                , directory=models_path)


    if models_path and models_text_format:
        models_to_text(models_dict=results
                   , output_path=models_path
                   , file_name_format=models_text_format)

    return results

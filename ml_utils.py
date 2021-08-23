"""
    Utilities for building machine learning models
"""
from cloudpickle import dump, load
import os
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz


from confusion_matrix import ConfusionMatrix, sk_to_grouped_df

def save_model(model
               , output_file_name
               , directory):
    with open(os.path.join(directory, output_file_name), "wb") as f:
        dump(model, f)


def load_model(model_file_name
               , directory):
    with open(os.path.join(directory, model_file_name), 'rb') as f:
        model = load(f)

    return model

def get_predictive_columns(df
                           , excluded_features=set()):
    return sorted(list(set(df.columns.tolist()) - excluded_features))

def df_to_sk_form(df
                  , concept
                  , test_size
                  , random_state
                  , get_predictive_columns_func
                  ):
    X = df[get_predictive_columns_func(df)]
    y = df[concept]
    X_train, X_test, y_train, y_test = train_test_split(X
                                                        , y
                                                        , test_size=test_size
                                                        , random_state=random_state)
    return X_test, X_train, y_test, y_train


def evaluate_model(classifier
                   , X_test
                   , y_test
                   , get_predictive_columns_func
                   , performance_file=None
                   , classifier_name='classifier'
                   , concept='concept'
                   , count='count'
                   ):
    df = X_test[get_predictive_columns_func(X_test)]
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

def build_and_eval_model(df
                                , classifier
                                , concept
                                , test_size
                                , random_state
                                , get_predictive_columns_func
                                , performance_file=None
                         ):

    X_test, X_train, y_test, y_train = df_to_sk_form(df=df
                  , concept=concept
                  , test_size=test_size
                  , random_state=random_state
                  , get_predictive_columns_func=get_predictive_columns_func)

    classifier.fit(X_train, y_train)
    performance = evaluate_model(classifier
                   , X_test
                   , y_test
                   , performance_file=performance_file
                   , get_predictive_columns_func=get_predictive_columns_func)

    return classifier, performance


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

    return cross_validate(estimator=classifier
                          , X=X_train
                          , y=y_train
                          , scoring=scoring
                          , cv=cv
                          , return_train_score=return_train_score)


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

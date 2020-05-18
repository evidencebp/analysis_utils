from cloudpickle import dump, load
import os
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz

from configuration import MODELS_PATH
from configuration import NON_PREDICTIVE_FEATURES, NON_NUMERIC_FEATURES, \
    TEST_SIZE, RANDOM_STATE, CONCEPT
from confusion_matrix import ConfusionMatrix, sk_to_grouped_df

def save_model(model
               , output_file_name
               , directory=MODELS_PATH):
    with open(os.path.join(directory, output_file_name), "wb") as f:
        dump(model, f)


def load_model(model_file_name
               , directory=MODELS_PATH):
    with open(os.path.join(directory, model_file_name), 'rb') as f:
        model = load(f)

    return model

def get_predictive_columns(df):
    return list(set(df.columns.tolist()) - NON_PREDICTIVE_FEATURES - NON_NUMERIC_FEATURES)

def df_to_sk_form(df
                  , concept
                  , test_size
                  , random_state
                  ):
    X = df[get_predictive_columns(df)]
    y = df[concept]
    X_train, X_test, y_train, y_test = train_test_split(X
                                                        , y
                                                        , test_size=test_size
                                                        , random_state=random_state)
    return X_test, X_train, y_test, y_train


def evaluate_model(classifier
                   , X_test
                   , y_test
                   , performance_file=None
                   , classifie_namer='classifier'
                   , concept='concept'
                   , count='count'
                   ):
    test_pred = classifier.predict(X_test)
    grouped_df = sk_to_grouped_df(labels=y_test
                     , predictions=test_pred
                     , classifier=classifie_namer
                     , concept=concept
                     , count=count
                     )
    cm = ConfusionMatrix(classifier=classifie_namer
                     , concept=concept
                     , count=count
                 , g_df=grouped_df)
    print(cm.summarize(performance_file))

def build_and_eval_model(df
                                , classifier
                                , performance_file=None
                                , concept=CONCEPT
                                , test_size=TEST_SIZE
                                , random_state=RANDOM_STATE
                              ):

    X_test, X_train, y_test, y_train = df_to_sk_form(df=df
                  , concept=concept
                  , test_size=test_size
                  , random_state=random_state)

    classifier.fit(X_train, y_train)
    evaluate_model(classifier
                   , X_test
                   , y_test
                   ,performance_file=performance_file)

    return classifier

def plot_tree(clf
              , dot_file_path
              , png_file_path
              , feature_names=None):
    export_graphviz(clf
                                 , feature_names=feature_names
                                 , out_file=dot_file_path)
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

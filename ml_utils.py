from cloudpickle import dump, load
import json
import os
from pandas import DataFrame
from sklearn.metrics import explained_variance_score, max_error, mean_absolute_error \
    , mean_squared_error, r2_score
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
    return list(set(df.columns.tolist()) - excluded_features)

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
    test_pred = classifier.predict(X_test)
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
    print(cm.summarize(performance_file))

def pred_25(y_test
            , test_pred):

    dict = {'concept': y_test
            , 'classifier' : test_pred}
    df = DataFrame(dict)
    df = df.reset_index()
    df['rel_diff'] = df.apply(lambda x: 0.0 if x.concept == 0.0 else x.classifier/x.concept, axis=1)
    df['25_rel_diff'] = df.rel_diff.map(lambda x: x > 0.75 and x < 1.25)

    #return len(df[df['25_rel_diff'] == 1])/len(df)
    return df['25_rel_diff'].mean()

def mmre(y_test
            , test_pred):
    """
    Mean Magnitude of Relative Error
    Definition is taken from
    https://www.researchgate.net/publication/228620836_A_ranking_stability_indicator_for_selecting_the_best_effort_estimator_in_software_cost_estimation
    :param y_test:
    :param test_pred:
    :return:
    """
    dict = {'concept': y_test
            , 'classifier' : test_pred}
    df = DataFrame(dict)
    df = df.reset_index()
    df['rel_diff'] = df.apply(lambda x: 0.0 if x.concept == 0.0 else abs(x.classifier -x.concept)/x.concept, axis=1)

    return df['rel_diff'].mean()

def evaluate_regressor(regressor
                   , X_test
                   , y_test
                   , performance_file=None
                   ):
    performace = {}
    test_pred = regressor.predict(X_test)

    performace['explained_variance_score'] = explained_variance_score(y_test, test_pred)
    performace['max_error'] = max_error(y_test, test_pred)
    performace['mean_absolute_error'] = mean_absolute_error(y_test, test_pred)
    performace['mean_squared_error'] = mean_squared_error(y_test, test_pred)
    performace['mean_squared_error'] = mean_squared_error(y_test, test_pred)
    performace['r2_score'] = r2_score(y_test, test_pred)

    performace['pred_25'] = pred_25(y_test
                                    , test_pred)
    performace['mmre'] = mmre(y_test
                                    , test_pred)

    if performance_file:
        with open(performance_file, 'w', encoding='utf-8') as f:
            json.dump(performace, f, ensure_ascii=False, indent=4)

    return performace


def build_and_eval_regressor(df
                                , regressor
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

    regressor.fit(X_train, y_train)
    performance = evaluate_regressor(regressor
                   , X_test
                   , y_test
                   , performance_file=performance_file
                   )

    return regressor, performance

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
    evaluate_model(classifier
                   , X_test
                   , y_test
                   , performance_file=performance_file
                   , get_predictive_columns_func=get_predictive_columns_func)

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

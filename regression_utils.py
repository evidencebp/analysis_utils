
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

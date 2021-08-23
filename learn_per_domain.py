import pandas as pd


def learn_per_domain(df
                                , classifier
                                , concept
                                , test_size
                                , random_state
                                , get_predictive_columns_func
                                , build_and_eval_function
                                , domain_column
                                , domain_values=None
                                , performance_file_template=None
                                , verbose=False):
    """
        Used for getting performance on different cohorts of the data set.
        Useful for domain adaptation (e.g., when comparing customers) and concet drift (e.g., when run over years).

        Note the other relevant analysis of compare_datasets which can find difference between the
        domain parts (e.g., between two customers).

    :param df:
    :param classifier:
    :param concept:
    :param test_size:
    :param random_state:
    :param get_predictive_columns_func:
    :param build_and_eval_function - build_and_eval_model for classification, build_and_eval_regressor for regression
    :param domain_column:
    :param domain_values:
    :param performance_file_template:
    :return:
    """
    values = domain_values
    performance_file = None

    if not values:
        values = df[domain_column].unique()

    all_performance = {}
    for i in values:

        if verbose:
            print("Processing ", i)

        if performance_file_template:
            performance_file = performance_file_template.format(domain=i)

        classifier, performance = build_and_eval_function(df[df[domain_column] == i]
                                , classifier
                                , concept
                                , test_size
                                , random_state
                                , get_predictive_columns_func
                                , performance_file=performance_file
                         )
        all_performance[i] = performance

    df = pd.DataFrame(all_performance).T

    return df
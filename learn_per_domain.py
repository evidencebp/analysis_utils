import pandas as pd

from ml_utils import build_and_eval_model

def learn_per_domain(df
                                , classifier
                                , concept
                                , test_size
                                , random_state
                                , get_predictive_columns_func
                                , domain_column
                                , domain_values=None
                                , performance_file_template=None):
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
        if performance_file_template:
            performance_file = performance_file_template.format(domain=i)

        classifier, performance = build_and_eval_model(df[df[domain_column] == i]
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
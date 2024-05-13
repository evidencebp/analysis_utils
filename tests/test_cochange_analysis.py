import pandas as pd
import pytest

from analysis_utils.cochange_analysis import cochange_analysis, cochange_analysis_by_value

@pytest.mark.parametrize(('per_year_df'
                         , 'metrics_dict'
                         , 'keys'
                         , 'control_variables'
                         , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [2010, 10, 10, 1],
                [2009, 9, 9, 1],
                [2008, 8, 8, 1],
                ], columns=['year', 'f1', 'f2', 'k'])
            , {'f1' : lambda prev, cur :prev < cur
               , 'f2' : lambda prev, cur :prev < cur}
            , ['k']
            , []
            , {'f2': {'true_positives': 2, 'true_negatives': 0, 'false_positives': 0, 'false_negatives': 0
                , 'samples': 2, 'accuracy': 1.0, 'positive_rate': 1.0, 'hit_rate': 1.0, 'precision': 1.0
                , 'precision_lift': 0.0, 'recall': 1.0, 'fpr': 0, 'jaccard': 1.0, 'independent_prob': 1.0
                , 'lift_over_independent': 0.0, 'lift_over_majority': 0.0, 'concept_entropy': 0
                , 'classifier_entropy': 0, 'mutual_information': 0.0, 'comment': None}}

, id='reg1')
                         ])
def test_cochange_analysis(per_year_df
                         , metrics_dict
                         , keys
                         , control_variables
                         , expected
                         ):
    actual = cochange_analysis(per_year_df
                         , metrics_dict
                         , keys
                         , control_variables=[]
                         )

    assert actual == expected



@pytest.mark.parametrize(('per_year_df'
                            , 'metrics_dict'
                            , 'fixed_variable'
                            , 'fixed_values'
                            , 'keys'
                            , 'control_variables'
                            , 'expected'
                          )
    , [
pytest.param(
            pd.DataFrame([
                [2010, 10, 10, 1, 'red'],
                [2009, 9, 9, 1, 'red'],
                [2008, 8, 8, 1, 'red'],
                [2010, 10, 1, 1, 'blue'],
                [2009, 9, 4, 1, 'blue'],
                [2008, 8, 3, 1, 'blue'],
                ], columns=['year', 'f1', 'f2', 'k', 'fixed'])
            , {'f1' : lambda prev, cur :prev < cur
               , 'f2' : lambda prev, cur :prev < cur}
            ,  'fixed'
            , ['red', 'blue']
            , ['k']
            , []
            , {'red': {'f2': {'true_positives': 2, 'true_negatives': 0, 'false_positives': 0, 'false_negatives': 0
, 'samples': 2, 'accuracy': 1.0, 'positive_rate': 1.0, 'hit_rate': 1.0, 'precision': 1.0, 'precision_lift': 0.0
, 'recall': 1.0, 'fpr': 0, 'jaccard': 1.0, 'independent_prob': 1.0, 'lift_over_independent': 0.0
, 'lift_over_majority': 0.0, 'comment': None}}
, 'blue': {'f2': {'true_positives': 1, 'true_negatives': 0, 'false_positives': 0, 'false_negatives': 1, 'samples': 2
, 'accuracy': 0.5, 'positive_rate': 1.0, 'hit_rate': 0.5, 'precision': 1.0, 'precision_lift': 0.0, 'recall': 0.5
, 'fpr': 0, 'jaccard': 0.5, 'independent_prob': 0.5, 'lift_over_independent': 0.0, 'lift_over_majority': -0.5
, 'comment': None}}}

, id='reg1')
                         ])
def cochange_analysis_by_value(per_year_df
                            , metrics_dict
                            , fixed_variable
                            , fixed_values
                            , keys
                            , control_variables
                            , expected
                         ):

    actual = cochange_analysis_by_value(per_year_df
                           , metrics_dict
                           , fixed_variable
                           , fixed_values
                           , keys
                           , control_variables)

    assert actual == expected



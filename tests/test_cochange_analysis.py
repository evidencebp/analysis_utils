import pandas as pd
import pytest

from analysis_utils.analysis_utils.cochange_analysis import (value_in_range, in_range_change
, cochange_analysis, cochange_analysis_by_value)


@pytest.mark.parametrize(('val'
                        , 'upper_bound'
                        , 'lower_bound'
                         , 'expected')
    , [
pytest.param(3 # val
             , 4 # upper_bound
             , 2 # lower_bound
             , 'in' # expected
, id='reg_in')
, pytest.param(3 # val
     , 4 # upper_bound
     , None # lower_bound
     , 'in' # expected
     , id='reg_in_just_upper')
, pytest.param(3 # val
            , None # upper_bound
            , 2 # lower_bound
            , 'in' # expected
            , id='reg_in_just_lower')
, pytest.param(5 # val
            , 4 # upper_bound
            , 2 # lower_bound
            , 'above' # expected
            , id='reg_above')
, pytest.param(5 # val
            , 4 # upper_bound
            , None # lower_bound
            , 'above'  # expected
            , id='reg_above_no_lower')
, pytest.param(1 # val
            , 4  # upper_bound
            , 2  # lower_bound
            , 'below'  # expected
            , id='reg_below')
, pytest.param(1 # val
            , None  # upper_bound
            , 2  # lower_bound
            , 'below'  # expected
            , id='reg_above_no_upper')
                         ])
def test_value_in_range(val
                        , upper_bound
                        , lower_bound
                         , expected
                         ):

    actual = value_in_range(val
                   , upper_bound=upper_bound
                   , lower_bound=lower_bound)

    assert actual == expected


def test_value_in_range_invalid_range():
    with pytest.raises(Exception):
        value_in_range(val=None
                       , upper_bound=3
                       , lower_bound=3)

@pytest.mark.parametrize(('prev'
                        , 'cur'
                        , 'upper_bound'
                        , 'lower_bound'
                         , 'expected')
    , [
pytest.param(10 # prev
             , 5 # cur
             , 6 # upper_bound
             , 2 # lower_bound
             , 1 # expected
, id='reg_to_range')
, pytest.param(3  # prev
            , 5  # cur
            , 6  # upper_bound
            , 2  # lower_bound
            , -1  # expected
            , id='reg_both_in_range')
                         ])
def test_in_range_change(prev
                    , cur
                    , upper_bound
                    , lower_bound
                    , expected):

    actual = in_range_change(prev
                    , cur
                    , upper_bound=upper_bound
                    , lower_bound=lower_bound)

    assert actual == expected

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



import numpy as np
from numpy.testing import assert_array_equal
import pandas as pd
import pytest

from maximize_classifiers_agreement import minimize_classifiers_entropy

def equal_dictionaries(dict1
                       , dict2):
    return all([v == dict1.get(k) for k,v in dict2.items()]) and len(dict1) == len(dict2)

def assert_equal_parameters(actual
                            , expected):
    assert_array_equal(actual['fixed_classes'], expected['fixed_classes'])
    assert_array_equal(actual['fixed_coef'], expected['fixed_coef'])
    assert_array_equal(actual['fixed_intercept'], expected['fixed_intercept'])

@pytest.mark.parametrize(('X'
                            , 'step_size'
                            , 'min_val'
                            , 'max_val'
                            , 'digits'
                            , 'include_zero'
                            , 'expected')
, [
pytest.param(
            pd.DataFrame([
                [1, -1],
                [ 1, -1],
                [ -1, 1],
                [-1, 1],
                [1, -1],
                [1, -1],
                [-1, 1],
                [-1, 1],
                [1, -1],
                [1, -1],
                [-1, 1],
                [-1, 1],
                [1, -1],
                [1, -1],
                [-1, 1],
                [-1, 1],
                [1, -1],
                [1, -1],
                [-1, 1],
                [-1, 1],
            ], columns=['f1', 'f2']).to_numpy()
            , 0.2
            , -1
            , 1
            , 1
            , False
            , {'fixed_classes': np.array([0, 1])
                , 'fixed_coef': np.array([[-1.,  1.]])
                , 'fixed_intercept': np.array([-0.2])}

, id='f1_and_minus_f1') # weight of w1 should b minus of f2 since they always disagree
                        # actual['fixed_coef'][0][0] == - actual['fixed_coef'][0][1]
                         ])
def test_minimize_classifiers_entropy(X
                                        , step_size
                                        , min_val
                                        , max_val
                                        , digits
                                        , include_zero
                                        , expected):

    actual = minimize_classifiers_entropy(X=X
                                 , step_size=step_size
                                 , min_val=min_val
                                 , max_val=max_val
                                 , digits=digits
                                 , include_zero=include_zero
                                 )

    assert_equal_parameters(actual
                            , expected)
    #assert equal_dictionaries(actual, expected)

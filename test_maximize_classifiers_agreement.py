import numpy as np
from numpy.testing import assert_array_equal
import pandas as pd
import pytest

from maximize_classifiers_agreement import minimize_classifiers_entropy, FixedLogisticRegression, confidence_entropy

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
                , 'fixed_coef': np.array([[1.,  -1.]])
                , 'fixed_intercept': np.array([-0.2])}

, id='f1_and_minus_f1') # weight of w1 should b minus of f2 since they always disagree
                        # actual['fixed_coef'][0][0] == - actual['fixed_coef'][0][1]
, pytest.param(
     pd.DataFrame([
         [1, -1, 0],
         [1, -1, 0],
         [-1, 1, 0],
         [-1, 1, 0],
         [1, -1, 0],
         [1, -1, 0],
         [-1, 1, 0],
         [-1, 1, 0],
         [1, -1, 0],
         [1, -1, 0],
         [-1, 1, 0],
         [-1, 1, 0],
         [1, -1, 0],
         [1, -1, 0],
         [-1, 1, 0],
         [-1, 1, 0],
         [1, -1, 0],
         [1, -1, 0],
         [-1, 1, 0],
         [-1, 1, 0],
         [1, -1, 0],
         [1, -1, 0],
         [-1, 1, 0],
         [-1, 1, 0],
     ], columns=['f1', 'f2', 'f3']).to_numpy()
     , 0.2
     , -1
     , 1
     , 1
     , False
     , {'fixed_classes': np.array([0, 1])
                , 'fixed_coef': np.array([[1.,  -1., 1.]]) # f3 coeffienect can be any value since it is multiplied by zero
                , 'fixed_intercept': np.array([-0.2])}

     , id='f1_and_minus_f1_abstaining_f3')

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

    Archimeds = FixedLogisticRegression()

    Archimeds = Archimeds.set_params(**actual)
    score = Archimeds.score(X, [0]*len(X))
    print("actual score", score)

    Archimeds = Archimeds.set_params(**expected)
    score = Archimeds.score(X, [0]*len(X))
    print("expected score", score)

    assert_equal_parameters(actual
                            , expected)

"""
, pytest.param(
     pd.DataFrame([
         [1, 1, -1],
         [-1, -1, 1],
         [1, 1, -1],
         [-1, -1, 1],
         [1, 1, -1],
         [-1, -1, 1],
         [1, 1, -1],
         [-1, -1, 1],
         [1, 1, -1],
         [-1, -1, 1],
     ], columns=['f1', 'f2', 'f3']).to_numpy()
     , 0.2
     , -1
     , 1
     , 1
     , False
     , {'fixed_classes': np.array([0, 1])
                , 'fixed_coef': np.array([[0.2,  0.2, -0.4]]) # w1 + w2 = -w3, many other values are ok here too
                , 'fixed_intercept': np.array([0])}

     , id='duplicated_f1_and_minus_f1')
"""


@pytest.mark.parametrize(('y'
                            , 'y_pred'
                            , 'expected')
, [
pytest.param(
            [None]
            , [0.5]
            , 1.0
, id='reg1')
, pytest.param(
            [None]
            , [0.5, 0.5]
            , 2.0
, id='reg2')
, pytest.param(
            [None]
            , [0.5, 0.5, 1]
            , 2.0
, id='reg3')


                         ])
def test_confidence_entropy(y
                            , y_pred
                            , expected):

    actual = confidence_entropy(y, y_pred)

    assert actual == expected


import sys
CODE_PATH = "C:/Idan/GitHub/in-work/lang"
sys.path.append(CODE_PATH)

import pandas as pd
import pytest
from confusion_matrix import ConfusionMatrix, entropy

@pytest.mark.parametrize(('classifier'
                         , 'concept'
                         , 'count'
                         , 'g_df'
                          , 'expected')
    , [
                             pytest.param(
                                 'classifier'
                                 , 'concept'
                                 , 'count'
                                 , pd.DataFrame([(True, True, 3)
                                       , (True, False, 4)
                                       , (False, True, 7)
                                       , (False, False, 16)]
                                   , columns=['classifier', 'concept', 'count'])
                                 , {'true_positives': 3, 'true_negatives': 16, 'false_positives': 4,
                                    'false_negatives': 7, 'samples': 30, 'accuracy': 0.63, 'positive_rate': 0.33,
                                    'hit_rate': 0.23, 'precision': 0.43, 'recall': 0.3, 'fpr': 0.2,
                                    'jaccard': 0.21, 'independent_prob': 0.59, 'lift_over_independent': 0.08
                                     , 'lift_over_majority': -0.05, 'precision_lift': 0.29
                                     , 'classifier_entropy': 0.78, 'concept_entropy': 0.92,'comment': None}
                                 , id='regular1')
     ])
def test_summrize(classifier
                         , concept
                         , count
                         , g_df
                          , expected):
    cm = ConfusionMatrix(classifier
                         , concept
                         , count
                         , g_df)
    actual = cm.summarize()
    assert expected == actual



@pytest.mark.parametrize(('classifier'
                          , 'concept'
                          , 'count'
                          , 'g_df'
                          , 'expected')
    , [
                             pytest.param(
                                 'classifier'
                                 , 'concept'
                                 , 'count'
                                 , pd.DataFrame(columns=['classifier', 'concept', 'count'])
                                 , 1
                                 , id='regular1')
                         ])
def test_independent_prob(classifier
                  , concept
                  , count
                  , g_df
                  , expected):
    cm = ConfusionMatrix(classifier
                         , concept
                         , count
                         , g_df)
    actual = cm.independent_prob()
    assert expected == actual

@pytest.mark.parametrize(('probability'
                          , 'expected')
    , [
         pytest.param(
             1
             , 0
             , id='regular1')
         , pytest.param(
             0
             , 0
             , id='regular2')
        , pytest.param(
            0.5
            , 1
            , id='regular3')
        , pytest.param(
            0.25
            , 0.8112781244591328
            , id='regular4')
        , pytest.param(
            0.75
            , 0.8112781244591328
            , id='regular4')

                         ])
def test_entropy(probability
                          , expected):
    actual = entropy(probability)

    assert expected == actual

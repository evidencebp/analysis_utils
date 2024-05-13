import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from analysis_utils.agreement_utils import compute_agreement, agreement_with_concepts
from analysis_utils.binning_utils import sides_binning, side_binning_by_direction, SIDES_SUFFIX
from analysis_utils.cochange_analysis import the_lower_the_better, the_higher_the_better

@pytest.mark.parametrize(('df'
                            , 'concepts'
                            , 'metrics'
                            , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [1, 0, 1, 0]
                , [1, 0, 1, 0]
                , [0, 1, 0, 1]
                , [0, 1, 0, 1]
            ], columns=['c1', 'c2', 'm1', 'm2'])
            , ['c1', 'c2']
            , ['m1', 'm2']
            , pd.DataFrame([
                ['m1', 1.0, 0.0]
                , ['m2', 0.0, 1.0]
    ], columns=['metric', 'c1', 'c2'])

, id='reg1')
                         ])
def test_compute_agreement(df: pd.DataFrame
                            , concepts
                            , metrics
                            , expected):

    actual = compute_agreement(df=df
                       , concepts=concepts
                       , metrics=metrics)

    assert_frame_equal(actual, expected)


@pytest.mark.parametrize(('df'
                            , 'concepts'
                            , 'metrics'
                            , 'expected')
    , [
pytest.param(
            pd.DataFrame([
                [1, 4, 1, 4]
                , [2, 3, 2, 3]
                , [3, 2, 3, 2]
                , [4, 1, 4, 1]
            ], columns=['c1', 'c2', 'm1', 'm2'])
            , {'c1' : the_lower_the_better
                    , 'c2' : the_lower_the_better}
            , {'c1' : the_lower_the_better
                    , 'c2' : the_lower_the_better
                    , 'm1' : the_lower_the_better
                    , 'm2' : the_lower_the_better}
            , pd.DataFrame([
                            ['c1_SIDES', 1.0, 0.5]
                            , ['c2_SIDES', 0.5, 1.0]
                            , ['m1_SIDES', 1.0, 0.5]
                            , ['m2_SIDES', 0.5, 1.0]
    ], columns=['metric', 'c1_SIDES', 'c2_SIDES'])

, id='reg1')
                         ])
def test_agreement_with_concepts(df: pd.DataFrame
                            , concepts
                            , metrics
                            , expected):

    actual = agreement_with_concepts(df
                          , concepts
                          , metrics)

    assert_frame_equal(actual, expected)

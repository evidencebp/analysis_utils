import pytest
from pandas.testing import assert_frame_equal
import pandas as pd

from ml_utils import df_to_sk_structuring

@pytest.mark.parametrize(('df'
                                , 'concept'
                                , 'test_size'
                                , 'random_state'
                          , 'expected')
    , [
pytest.param(
                pd.DataFrame([
                            [1, 10, 101]
                            , [2, 20, 102]
                            , [3, 30, 103]
                            , [4, 40, 104]
                ], columns=['a', 'b', 'c']) # df
                , 'c' # concept
                , 0.5 # test size
                , 1 # random_state
                , (pd.DataFrame([
                            [4, 40]
                            , [3, 30]
                ], columns=['a', 'b']) # X_test
                , pd.DataFrame([
                            [1, 10]
                            , [2, 20]
                ], columns=['a', 'b']) # X_train
                , pd.DataFrame([
                            [104]
                            , [103]
                ], columns=['c'])['c'].to_numpy() # y_test
                , pd.DataFrame([
                            [101]
                            , [102]
                ], columns=['c'])['c'].to_numpy() # y_train
) # expected
, id='regular_split')
, pytest.param(
                pd.DataFrame([
                            [1, 10, 101]
                            , [2, 20, 102]
                            , [3, 30, 103]
                            , [4, 40, 104]
                ], columns=['a', 'b', 'c']) # df
                , 'c' # concept
                , 0 # test size
                , 1 # random_state
                , (pd.DataFrame(None, columns=['a', 'b']) # X_test
                ,  pd.DataFrame([
                            [1, 10]
                            , [2, 20]
                            , [3, 30]
                            , [4, 40]
                ], columns=['a', 'b']) # X_train
                , pd.DataFrame(None, columns=['c'])['c'].to_numpy() # y_test
                , pd.DataFrame([
                                [101]
                                , [102]
                                , [103]
                                , [104]
            ], columns=['c'])['c'].to_numpy() # y_train
) # expected
, id='only_train')
])
def test_df_to_sk_structuring(df
                                , concept
                                , test_size
                                , random_state
                                , expected):

    actual = df_to_sk_structuring(df
                  , concept
                  , test_size
                  , random_state
                  )

    for i in range(2):
        assert_frame_equal(actual[i].reset_index(drop=True)
                       , expected[i].reset_index(drop=True))

    for i in [2, 3]:
        assert (actual[i] == expected[i]).all()

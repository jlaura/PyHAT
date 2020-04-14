import numpy as np
import pandas as pd
from libpyhat.examples import get_path
import libpyhat.utils.folds

def test_folds():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    result = libpyhat.utils.folds.stratified_folds(df,nfolds=3,sortby=('comp','SiO2'))
    expected = [3., 1., 1., 1., 3., 2., 2., 1., 1., 1.]
    np.testing.assert_array_almost_equal(expected, np.array(result[('meta','Folds')].iloc[0:10]))

    result = libpyhat.utils.folds.random(df,('comp','SiO2'),nfolds=3,seed=10)
    expected = [1, 2, 2, 2, 1, 2, 1, 2, 2, 2]
    np.testing.assert_array_almost_equal(expected, np.array(result[('meta','Folds')].iloc[0:10]))

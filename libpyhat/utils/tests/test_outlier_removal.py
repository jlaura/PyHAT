import numpy as np
import pandas as pd
from libpyhat.examples import get_path
import libpyhat.utils.outlier_removal

def test_LOF():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    params = {
                'n_neighbors': 10,
                'contamination': 'auto',
                'leaf_size': 10,
                'p': 2}
    result = libpyhat.utils.outlier_removal.outlier_removal(df, 'wvl', 'Local Outlier Factor', params)
    expected_scores = [-1.010267, -1.35764 , -1.383224, -1.620422, -1.036561]
    np.testing.assert_array_almost_equal(expected_scores, np.array(result[('meta', result['meta'].columns[-1])])[0:5])


def test_isolation_forest():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    params = {'n_estimators': 10,
              'contamination': 'auto',
              'random_state':1}
    result = libpyhat.utils.outlier_removal.outlier_removal(df, 'wvl','Isolation Forest',params)
    expected_scores = [0.07998454, 0.01812089, 0.06773168, 0.01483949, -0.04311234]
    np.testing.assert_array_almost_equal(expected_scores,np.array(result[('meta',result['meta'].columns[-2])])[0:5])



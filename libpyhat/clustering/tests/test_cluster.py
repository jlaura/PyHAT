import numpy as np
import pandas as pd
from libpyhat.examples import get_path
import libpyhat.clustering.cluster as cluster

def test_spectral():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    kws = {     'n_clusters': 3,
                'n_init': 2,
                'affinity': 'rbf',
                'gamma': 1.0,
                'n_neighbors': 5,
                'degree': 3,
                'coef0': 1,
                'random_state':1}
    result = cluster.cluster(df, 'wvl', 'Spectral', [], kws)
    expected = [2, 2, 1, 1, 2, 3, 2, 1, 1, 1]
    np.testing.assert_array_almost_equal(expected, np.squeeze(np.array(result['Spectral'].iloc[0:10])))


def test_kmeans():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    kws = {'n_clusters': 3,
              'n_init': 2,
              'max_iter': 100,
              'tol': 0.01,
              'random_state':1}
    result = cluster.cluster(df,'wvl','K-Means',[],kws)
    expected = [2, 1, 1, 1, 1, 2, 2, 3, 2, 1]
    np.testing.assert_array_almost_equal(expected,np.squeeze(np.array(result['K-Means'].iloc[0:10])))

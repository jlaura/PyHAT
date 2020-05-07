import numpy as np
import pandas as pd
from libpyhat.examples import get_path
import libpyhat.clustering.cluster as cluster
import libpyhat.transform.norm as norm
np.random.seed(1)
df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
df = norm.norm(df,[[585,600]])

def test_spectral():
    kws = {     'n_clusters': 3,
                'n_init': 10,
                'affinity': 'rbf',
                'gamma': 1.0,
                'n_neighbors': 5,
                'degree': 3,
                'coef0': 1,
                'n_jobs':1,
                'random_state':1}
    result = cluster.cluster(df, 'wvl', 'Spectral', [], kws)
    clusters = np.squeeze(np.array(result['Spectral']))
    cluster_count = [np.count_nonzero(clusters==1),np.count_nonzero(clusters==2),np.count_nonzero(clusters==3)]
    cluster_count.sort()
    assert cluster_count == [8,32,63]

def test_kmeans():
    kws = {'n_clusters': 3,
              'n_init': 10,
              'max_iter': 100,
              'tol': 0.01,
              'n_jobs':1,
           'random_state':1}
    result = cluster.cluster(df,'wvl','K-Means',[],kws)
    clusters = np.squeeze(np.array(result['K-Means']))
    cluster_count = [np.count_nonzero(clusters == 1), np.count_nonzero(clusters == 2), np.count_nonzero(clusters == 3)]
    cluster_count.sort()
    assert cluster_count == [10, 34, 59]

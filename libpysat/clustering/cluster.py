
from sklearn.cluster import KMeans, SpectralClustering

#This function runs clustering on a data frame full of spectra. Different algorithms can be chosen

def cluster(df, col, method, params, kws):
    if method == 'K-Means':
        do_cluster = KMeans(*params, **kws)
    if method == 'Spectral':
        do_cluster = SpectralClustering(*params, **kws)

    do_cluster.fit(df[col])
    df[(method, 'Cluster')] = do_cluster.labels_

    return df
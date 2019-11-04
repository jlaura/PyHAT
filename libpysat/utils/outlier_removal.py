import sklearn.ensemble as ensemble
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
import numpy as np

#This function flags outliers in a spectral data set. Different algorithms can be selected.

def outlier_removal(df, col, method, params):
    if method == 'Isolation Forest':
        do_outlier_removal = IsolationForest(**params)
    if method == 'Local Outlier Factor':
        do_outlier_removal = LocalOutlierFactor(**params)
    else:
        method == None
    do_outlier_removal.fit(np.array(df[col]))
    if method == 'Isolation Forest':
        outlier_scores = do_outlier_removal.decision_function(np.array(df[col]))
        df[('meta', 'Outlier Scores - ' + method + str(params))] = outlier_scores
        is_outlier = do_outlier_removal.predict(np.array(df[col]))
        df[('meta', 'Outliers - ' + method + str(params))] = is_outlier
    if method == 'Local Outlier Factor':
        is_outlier = do_outlier_removal.fit_predict(np.array(df[col]))
        df[('meta', 'Outliers - ' + method + str(params))] = is_outlier
        df[('meta', 'Outlier Factor - ' + method + str(params))] = do_outlier_removal.negative_outlier_factor_
    return df, do_outlier_removal
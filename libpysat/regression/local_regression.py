# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 11:31:46 2016

@author: rbanderson
"""
import copy
import traceback
import numpy as np
import sklearn.kernel_ridge as kernel_ridge
import sklearn.linear_model as linear
import sklearn.svm as svm
from sklearn.cross_decomposition.pls_ import PLSRegression
from sklearn.linear_model import LassoCV
from sklearn.decomposition import PCA, FastICA
from sklearn.gaussian_process import GaussianProcess
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import GroupKFold

class local_regression:
    def __init__(self, method, params, n_neighbors = 250,
                 i=0):  # TODO: yrange doesn't currently do anything. Remove or do something with it!
        self.algorithm_list = ['LASSO']
        self.method = method

        print(params)
        if self.method[i] == 'LASSO':
            self.model = LassoCV(**params[i])

        self.neighbors = NearestNeighbors(n_neighbors=n_neighbors)

    def fit_predict(self,x_train,y_train, x_predict):

        self.neighbors.fit(x_train)
        predictions = []
        coeffs = []
        intercepts = []
        for i in range(x_predict.shape[0]):
            print('Predicting spectrum ' + str(i + 1))
            x_temp = np.array(x_predict[i])
            foo, ind = self.neighbors.kneighbors([x_temp])
            x_train_local = np.squeeze(x_train[ind])
            y_train_local = np.squeeze(y_train[ind])

            cv = GroupKFold(n_splits=3)
            cv = cv.split(x_train_local, y_train_local,
                          groups=y_train_local)
            self.model.fit(x_train_local, y_train_local)
            predictions.append(self.model.predict([x_temp])[0])
            coeffs.append(self.model.coef_)
            intercepts.append(self.model.intercept_)
        return predictions, coeffs, intercepts


# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 11:31:46 2016

@author: rbanderson
"""
import numpy as np
import pysat.spectral.within_range as within_range
from sklearn.cross_decomposition.pls_ import PLSRegression
from sklearn.decomposition import PCA, FastICA
from sklearn.gaussian_process import GaussianProcess
from sklearn.linear_model import RANSACRegressor as RANSAC
from pysat.spectral.meancenter import meancenter
import scipy.optimize as opt
from pysat.plotting import plots 

class regression:
    def __init__(self,method,params,i=0,ransacparams=None):
        self.method=method 
        self.outliers=None
        self.inliers=None
        self.ransac=False
        
        if self.method is 'PLS':
           self.model=PLSRegression(**params[i])
        if self.method is 'GP':
            self.model=GaussianProcess(**params[i])
        if ransacparams is not None:
            self.model=RANSAC(self.model,**ransacparams[i])
            self.ransac=True
            
        
    def fit(self,x,y,figparams=None):
            
        self.model.fit(x,y)
        self.ypred=self.predict(x)
        self.rmsec=np.sqrt(np.mean((np.squeeze(self.ypred)-y)**2))
        
        if self.ransac:
            self.outliers=np.logical_not(self.model.inlier_mask_)
            self.rmsec_ransac=np.sqrt(np.mean((np.squeeze(self.ypred)[self.model.inlier_mask_]-y[self.model.inlier_mask_])**2))
            print(str(np.sum(self.outliers))+' outliers removed with RANSAC')
        if self.method is 'PLS' and self.ransac is False:
            self.calc_Qres_Lev(x)
            
        if figparams:
            plots.scatterplot(y,[self.ypred],figparams)
                
    def predict(self,x):
        return self.model.predict(x)
        
    def calc_Qres_Lev(self,x):
        #calculate spectral residuals
        E=x-np.dot(self.model.x_scores_,self.model.x_loadings_.transpose())
        Q_res=np.dot(E,E.transpose()).diagonal()
        #calculate leverage                
        T=self.model.x_scores_
        leverage=np.diag(T@np.linalg.inv(T.transpose()@T)@T.transpose())
        self.leverage=leverage
        self.Q_res=Q_res        

        
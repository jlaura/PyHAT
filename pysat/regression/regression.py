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
            #get the method for dimensionality reduction and the number of components
            self.reduce_dim=params[i]['reduce_dim']
            self.n_components=params[i]['n_components']
            #Then removed these from the parameters so params can be passed to Gaussian Process
            params[i].pop('reduce_dim')
            params[i].pop('n_components')
            self.model=GaussianProcess(**params[i])
        if ransacparams is not None:
            self.model=RANSAC(self.model,**ransacparams[i])
            self.ransac=True
            
        
    def fit(self,x,y,figparams=None):
        #if gaussian processes are being used, data dimensionality needs to be reduced before fitting        
        if self.method is 'GP':
            if self.reduce_dim is 'ICA':
                do_ica=FastICA(n_components=self.n_components)
                self.do_reduce_dim=do_ica.fit(x)
            if self.reduce_dim is 'PCA':
                do_pca=PCA(n_components=self.n_components)
                self.do_reduce_dim=do_pca.fit(x)
            x=self.do_reduce_dim.transform(x)
        try:
            self.model.fit(x,y)
        
            if self.ransac:
                self.outliers=np.logical_not(self.model.inlier_mask_)
                print(str(np.sum(self.outliers))+' outliers removed with RANSAC')
        
            if self.method is 'PLS' and self.ransac is False:
                self.calc_Qres_Lev(x)
            self.goodfit=True
        except:
            self.goodfit=False  #This can happen for GP when dimensionality is reduced too much. Use try/except to handle these cases.
            
                
    def predict(self,x):
        if self.method is 'GP':
            x=self.do_reduce_dim.transform(x)
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

        
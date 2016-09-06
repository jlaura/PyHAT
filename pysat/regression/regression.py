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
    def __init__(self,ycol,method,ransac=False,**kwargs):
        self.ycol=ycol
        self.method=method 
        self.ransac=ransac
        self.outliers=None
        self.inliers=None
        self.reduce_dim=False
        self.kwargs=kwargs  #pass kwargs to other functions
        try:
            self.i=kwargs['i']  #kwargs must include an entry 'i' to index into the other keywords. This lets regression work with submodels
        except:
            print('kwargs must include an entry "i" to index into the other keywords. This lets regression work with submodels')
        self.range=kwargs['range']
        if self.method is 'PLS':
           self.model=PLSRegression(n_components=kwargs['nc'][self.i],scale=False)
        if self.method is 'GP':
            self.model=GaussianProcess(theta0=kwargs['theta0'][self.i],thetaL=kwargs['thetaL'][self.i],
                                       thetaU=kwargs['thetaU'][self.i],random_start=kwargs['random_start'][self.i],
                                        regr=kwargs['regr'][self.i])
        if self.ransac:
            self.model=RANSAC(self.model,min_samples=self.ransac)
            #TO DO: enable changing other parameters of RANSAC
            
        
    def fit(self,x,y,figpath=None):
        #x_centered,x_mean_vect=meancenter(x) #mean center training data
        if self.reduce_dim is 'ICA':
            ica=FastICA(n_components=self.kwargs['nc'][self.i])
            self.do_ica=ica.fit(x)
            x_centered=self.do_ica.transform(x)
        if self.reduce_dim is 'PCA':
            pca=PCA(n_components=self.kwargs['nc'][self.i])
            self.do_pca=pca.fit(x)
            x_centered=self.do_pca.transform(x)
            
        self.model.fit(x,y)
        self.ypred=self.predict(x)
        self.rmsec=np.sqrt(np.mean((np.squeeze(self.ypred)-y)**2))
        
        if self.ransac:
            self.outliers=np.logical_not(self.model.inlier_mask_)
            self.rmsec=np.sqrt(np.mean((np.squeeze(self.ypred)[self.model.inlier_mask_]-y[self.model.inlier_mask_])**2))
            print(str(np.sum(self.outliers))+' outliers removed with RANSAC')
        if self.method is 'PLS' and self.ransac is False:
            self.calc_Qres_Lev(x)
            
        if figpath:
            ransac_str=''
            if self.ransac:
                ransac_str='_ransac'
            figname=self.ycol[-1]+'_'+self.method+'_'+str(self.range[0])+'-'+str(self.range[1])+ransac_str+'_train.png'
            lbl=['RMSEC = '+str(round(self.rmsec,2))]
        #Plot the training set predictions
            plots.scatterplot([y],[self.ypred],one_to_one=True,figpath=figpath,
                figname=figname,title=self.ycol[-1],lbls=lbl,annot_mask=[self.outliers])
                
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

        
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:16:11 2016
This function is used to run cross validation 
to help choose the optimal number of components. Folds are stratified 
according to a user-specified column

@author: rbanderson
"""
import numpy as np
from sklearn.cross_validation import LeaveOneLabelOut
from sklearn.grid_search import ParameterGrid
from pysat.regression.regression import regression
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

def RMSE(ypred,y):
    return np.sqrt(np.mean((np.squeeze(ypred)-np.squeeze(y))**2))

def cv(Train,params,xcols='wvl',ycol=('meta','SiO2'),method='PLS',ransac=False):
    paramgrid=list(ParameterGrid(params))  #create a grid of parameter permutations
    cv_iterator=LeaveOneLabelOut(Train[('meta','Folds')])  #create an iterator for cross validation based on the predefined folds

    rmsecv_folds=[]
    rmsec=[]
    rmsecv=[]
    
    #loop through the grid of parameters, do cross validation for each permutation
    for i in list(range(len(paramgrid))):
        print(paramgrid[i])
        
        #create the estimator object with the current parameters
        model=regression(method,[paramgrid[i]])
        rmsecv_folds_tmp=[]  #Create empty list to hold RMSECV for each fold
        for train,holdout in cv_iterator:  #Iterate through each of the folds in the training set
            resultcol=('meta',ycol[-1]+'_cv_'+method+'_param'+str(i))  #create the name of the column in which results will be stored
            cv_train=Train.iloc[train]   #extract the data to be used to create the model
            cv_holdout=Train.iloc[holdout]  #extract the data that will be held out of the model
            model.fit(cv_train[xcols],cv_train[ycol])
            if model.goodfit:            
                y_pred_holdout=model.predict(cv_holdout[xcols])
            else:
                y_pred_holdout=cv_holdout[ycol]*0
            Train.set_value(Train.index[holdout],resultcol,y_pred_holdout)
            rmsecv_folds_tmp.append(RMSE(y_pred_holdout,cv_holdout[ycol]))
        
        rmsecv_folds.append(rmsecv_folds_tmp)
        rmsecv.append(RMSE(Train[ycol],Train[resultcol]))
          
        model.fit(Train[xcols],Train[ycol])
        if model.goodfit:
            ypred_train=model.predict(Train[xcols])        
        else:
            ypred_train=Train[ycol]*0
        rmsec.append(RMSE(ypred_train,Train[ycol]))
    
    
    return rmsec,rmsecv,rmsecv_folds,pd.DataFrame(paramgrid)
           
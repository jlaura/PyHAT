# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:16:11 2016
This function is used to run cross validation 
to help choose the optimal number of components. Folds are stratified 
according to a user-specified column

@author: rbanderson
"""
import numpy as np
from sklearn.cross_decomposition.pls_ import PLSRegression
from sklearn.cross_validation import LeaveOneLabelOut
from pysat.spectral.meancenter import meancenter
from pysat.regression.regression import regression 
from pysat.plotting import plots 

def cv(Train,xcols='wvl',ycol=('meta','SiO2'),method='PLS',ransac=False,figpath='.',figname='rmsecv.png',**kwargs):
    #create empty arrays for the RMSE values    
    rmsecv=np.empty(kwargs['nc'])
    rmsec=np.empty(kwargs['nc'])
        

    #loop through each number of components
    for i in range(1,kwargs['nc']+1):
        print('nc='+str(i))
        Train[('meta',ycol[-1]+'_cv_'+method+'_nc'+str(i))]=0 #create a column to hold the cross validation results for this nc
        Train[('meta',ycol[-1]+'_'+method+'_nc'+str(i))]=0 #create a column to hold the training set results for this nc
        
        #Do the cross validation
        cv_iterator=LeaveOneLabelOut(Train[('meta','Folds')]) #create the iterator for cross validation within the training data
        
        #How can we modify regression such that we can use more built-in cross-validation tools from scikit?
        #Maybe bypass regression and just directly call the scikit routines for cv?
        
        for train,holdout in cv_iterator:  #Iterate through each of the folds in the training set
            cv_train=Train.iloc[train]
            cv_holdout=Train.iloc[holdout]
            
            #Do PLS for this number of components
            cv_train_centered,cv_train_mean_vect=meancenter(cv_train) #mean center training data
            cv_holdout_centered,cv_holdout_mean_vect=meancenter(cv_holdout,previous_mean=cv_train_mean_vect) #apply same mean centering to holdout data           
            kwargs_reg=kwargs
            kwargs_reg['i']=0
            kwargs_reg['nc']=[i]        
            reg=regression(ycol,method,ransac=ransac,**kwargs)            
            #pls=PLSRegression(n_components=i,scale=False)
            reg.fit(cv_train_centered[xcols],cv_train_centered[ycol])            
            
            y_pred_holdout=reg.predict(cv_holdout_centered[xcols])
            Train.set_value(Train.index[holdout],('meta',ycol[-1]+'_cv_'+method+'_nc'+str(i)),y_pred_holdout)
 
        rmsecv[i-1]=np.sqrt(np.mean(np.subtract(Train[ycol],Train[('meta',ycol[-1]+'_cv_'+method+'_nc'+str(i))])**2,axis=0))
       
        #Do train and test set PLS predictions for this number of components
        Train_centered,Train_mean_vect=meancenter(Train)
        pls=PLSRegression(n_components=i,scale=False)
        pls.fit(Train_centered['wvl'],Train_centered[ycol])
        
        y_pred=pls.predict(Train_centered['wvl'])
        Train.set_value(Train.index,('meta',ycol[-1]+'_PLS_nc'+str(i)),y_pred)    
        rmsec[i-1]=np.sqrt(np.mean(np.subtract(Train[ycol],Train[('meta',ycol[-1]+'_'+method+'_nc'+str(i))])**2,axis=0))

               
    if figpath and figname:
        x=np.array(range(1,kwargs['nc'][kwargs['i']]+1))
        x=[x,x]
        y=[rmsec,rmsecv]
        lbls=['RMSEC','RMSECV']
            
        plots.lineplot(x,y,xtitle='# of Componenets',ytitle='RMSE (wt.%)',title=None,
                lbls=lbls,figpath=figpath,figname=figname,dpi=1000)        
        
    rmses={'RMSEC':rmsec,'RMSECV':rmsecv}
    return rmses
    
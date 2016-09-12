# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 14:53:23 2015

@author: rbanderson
"""
import numpy as np
import pandas as pd
import scipy as sp
from sklearn import cross_validation
from pysat.spectral.baseline_code.als import ALS
from pysat.spectral.baseline_code.dietrich import Dietrich
from pysat.spectral.baseline_code.polyfit import PolyFit
from pysat.spectral.baseline_code.airpls import AirPLS
from pysat.spectral.baseline_code.fabc import FABC
from pysat.spectral.baseline_code.kajfosz_kwiatek import KajfoszKwiatek as KK
from pysat.spectral.baseline_code.mario import Mario
from pysat.spectral.baseline_code.median import MedianFilter
from pysat.spectral.baseline_code.rubberband import Rubberband


def norm_total(df):
    df=df.div(df.sum(axis=1),axis=0)
    return df

class spectral_data(object):
    def __init__(self,df):
        self.df=df

    
    def interp(self,xnew):
        xnew=np.array(xnew,dtype='float')

        metadata_cols=self.df.columns.levels[0]!='wvl'
        metadata=self.df[self.df.columns.levels[0][metadata_cols]]
        old_wvls=np.array(self.df['wvl'].columns,dtype='float')
        old_spectra=np.array(self.df['wvl'])
        new_spectra=np.empty([len(old_spectra[:,0]),len(xnew)])*np.nan
        interp_index=(xnew>min(old_wvls)) & (xnew<max(old_wvls))
        
        f=sp.interpolate.interp1d(old_wvls,old_spectra,axis=1)
        new_spectra[:,interp_index]=f(xnew[interp_index])

        xnew=list(xnew)
        for i,x in enumerate(xnew):    
            xnew[i]=('wvl',x)
            
        new_df=pd.DataFrame(new_spectra,columns=pd.MultiIndex.from_tuples(xnew),index=self.df.index)
        new_df=pd.concat([new_df,metadata],axis=1)
        
        self.df=new_df
        
    
    def mask(self,maskfile):
        df_spectra=self.df['wvl'] #extract just the spectra from the data frame
        metadata_cols=self.df.columns.levels[0]!='wvl'  #extract just the metadata
        metadata=self.df[self.df.columns.levels[0][metadata_cols]]
        
        mask = pd.read_csv(maskfile, sep=',')  #read the mask file
        tmp=[]
        for i in mask.index:
            tmp.append((np.array(self.df['wvl'].columns,dtype='float')>=mask.ix[i,'min_wvl'])&(np.array(self.df['wvl'].columns,dtype='float')<=mask.ix[i,'max_wvl']))
    
        #combine the indexes for each range in the mask file into a single masking vector and use that to mask the spectra
        masked=np.any(np.array(tmp),axis=0)
        spectcols=list(df_spectra.columns)  #get the list of columns in the spectra dataframe
        for i,j in enumerate(masked):  #change the first level of the tuple from 'wvl' to 'masked' where appropriate
            if j==True:
                spectcols[i]=('masked',spectcols[i])
            else:
                spectcols[i]=('wvl',spectcols[i])
        df_spectra.columns=pd.MultiIndex.from_tuples(spectcols) #assign the multiindex columns based on the new tuples
        self.df=pd.concat([df_spectra,metadata],axis=1) #merge the masked spectra back with the metadata

        
    def random_folds(self,nfolds=5,seed=10,groupby=None):
        self.df[('meta','Folds')]=np.nan #Create an entry in the data frame that holds the folds
        foldslist=np.array(self.df[('meta','Folds')])
        if groupby==None: #if no column name is listed to group on, just create random folds
            n=len(self.df.index)
            folds=cross_validation.KFold(n,nfolds,shuffle=True,random_state=seed)
            i=1        
            for train,test in folds:
                foldslist[test]=i
                i=i+1
        
        else: 
            #if a column name is provided, get all the unique values and define folds
            #so that all rows of a given value fall in the same fold 
            #(this is useful to ensure that training and test data are truly independent)
            unique_inds=np.unique(self.df[groupby]) 
            folds=cross_validation.KFold(len(unique_inds),nfolds,shuffle=True,random_state=seed)
            foldslist=np.array(self.df[('meta','Folds')])
            i=1        
            for train,test in folds:
                tmp=unique_inds[test]
                tmp_full_list=np.array(self.df[groupby])
                tmp_ind=np.in1d(tmp_full_list,tmp)
                foldslist[tmp_ind]=i
                i=i+1
        
        self.df[('meta','Folds')]=foldslist
       
        
    
    def stratified_folds(self,nfolds=5,sortby=None):
        self.df[('meta','Folds')]=np.NaN #Create an entry in the data frame that holds the folds
        self.df.sort(columns=sortby,inplace=True) #sort the data frame by the column of interest
        uniqvals=np.unique(self.df[sortby])   #get the unique values from the column of interest
        
        #assign folds by stepping through the unique values
        fold_num=1
        for i in uniqvals:
            ind=self.df[sortby]==i #find where the data frame matches the unique value
            self.df.set_value(self.df.index[ind],('meta','Folds'),fold_num)
            #Inrement the fold number, reset to 1 if it is greater than the desired number of folds        
            fold_num=fold_num+1
            if fold_num>nfolds:
                fold_num=1
                    
        #sort by index to return the df to its original order
        self.df.sort_index(inplace=True)
        
        
    def norm(self,ranges):
        df_spect=self.df['wvl']
        df_meta=self.df['meta']
        wvls=df_spect.columns.values
        df_sub_norm=[]
        allind=[]    
        for i in ranges:
            #Find the indices for the range
            ind=(np.array(wvls,dtype='float')>=i[0])&(np.array(wvls,dtype='float')<=i[1])
            #find the columns for the range
            cols=wvls[ind]
            #keep track of the indices used for all ranges
            allind.append(ind)
            #add the subset of the full df to a list of dfs to normalize
            df_sub_norm.append(norm_total(df_spect[cols]))
        
        #collapse the list of indices used to a single array
        allind=np.sum(allind,axis=0)
        #identify wavelengths that were not used by where the allind array is less than 1
        wvls_excluded=wvls[np.where(allind<1)]
        #create a separate data frame containing the un-normalized columns
        df_excluded=df_spect[wvls_excluded]
        
        #combine the normalized data frames into one
        df_norm=pd.concat(df_sub_norm,axis=1)
        
        #make the columns into multiindex
        df_excluded.columns=[['masked']*len(df_excluded.columns),df_excluded.columns]    
        df_norm.columns=[['wvl']*len(df_norm.columns),df_norm.columns.values] 
        df_meta.columns=[['meta']*len(df_meta.columns),df_meta.columns.values]
        
        #combine the normalized data frames, the excluded columns, and the metadata into a single data frame
        df_new=pd.concat([df_meta,df_norm,df_excluded],axis=1)
        self.df=df_new


        
    def remove_baseline(self,method='als',segment=True,params=None):
        wvls=np.array(self.df['wvl'].columns.values,dtype='float')
        spectra=np.array(self.df['wvl'],dtype='float')
        
       
        #set baseline removal object (br) to the specified method
        if method is 'als':
            br=ALS()
        if method is 'dietrich':
            br=Dietrich()
        if method is 'polyfit':
            br=PolyFit()
        if method is 'airpls':
            br=AirPLS()
        if method is 'fabc':
            br=FABC()
        if method is 'kk':
            br=KK()
        if method is 'mario':
            br=Mario()
        if method is 'median':
            br=MedianFilter()
        if method is 'rubberband':
            br=Rubberband()
        #if method is 'wavelet':
         #   br=Wavelet()
            
            
        #if parameters are provided, use them to set the parameters of br
        if params is not None:
            for i in br.__dict__.keys():
                try:
                    br[i]=params[i]
                except:
                    print('Required keys are:')
                    print(br.__dict__.keys())
        br.fit(wvls,spectra,segment=segment)
        self.df_baseline=self.df.copy()
        self.df_baseline['wvl']=br.baseline
        self.df['wvl']=br.fit_transform(wvls,spectra)
       
    

    def rows_match(self,column_name,isin_array,invert=False):
        if invert:
            new_df=self.df.loc[-self.df[column_name].isin(isin_array)]              
        else:
            new_df=self.df.loc[self.df[column_name].isin(isin_array)]              
        return spectral_data(new_df)
        
    def col_within_range(self,rangevals,col):
        mask=(self.df[('meta',col)]>rangevals[0])&(self.df[('meta',col)]<rangevals[1])
        return self.df.loc[mask]
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 13:07:07 2016

@author: rbanderson
"""

def meancenter(df,previous_mean=None):
    if previous_mean is not None:
        mean_vect=previous_mean
    else:
        mean_vect=df['wvl'].mean(axis=0)    
    df['wvl']=df['wvl'].sub(mean_vect,axis=1)
    
    return df,mean_vect
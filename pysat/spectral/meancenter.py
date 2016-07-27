# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 13:07:07 2016

@author: rbanderson
"""

import numpy as np
def meancenter(df,previous_mean=None):
    if previous_mean is not None:
        mean_vect=previous_mean
    else:
        mean_vect=df['wvl'].mean(axis=0)
        
    
    #check that the wavelength values match    
    if np.array_equal(mean_vect.index.values,df['wvl'].columns.values):
        df['wvl']=df['wvl'].sub(mean_vect.values,axis=1)
    else:
        print("Can't mean center! Wavelengths don't match!")    
    
    return df,mean_vect
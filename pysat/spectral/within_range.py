# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:11:37 2016

@author: rbanderson
"""
def within_range(data,rangevals,col):
    mask=(data[col]>rangevals[0])&(data[col]<rangevals[1])
    return data.loc[mask]
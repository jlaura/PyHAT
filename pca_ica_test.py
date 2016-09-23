# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:09:29 2016

@author: rbanderson
"""
import pandas as pd
from pysat.spectral.spectral_data import spectral_data
from pysat.plotting import plots
import numpy as np
import warnings

warnings.filterwarnings('ignore')

print('Read training database')
db=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Sample_Data\full_db_mars_corrected_dopedTiO2_pandas_format.csv"
data=pd.read_csv(db,header=[0,1])

data=spectral_data(data)


print('read unknown data from the combined csv file (much faster)')
unknowndatacsv=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\Lab Data\lab_data_averages_pandas_format.csv"
unknown_data=pd.read_csv(unknowndatacsv,header=[0,1])
unknown_data=spectral_data(unknown_data)

print('Interpolate unknown data onto the same exact wavelengths as the training data')
unknown_data.interp(data.df['wvl'].columns)

print('Mask out unwanted portions of the data')
maskfile=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Input\mask_minors_noise.csv"
data.mask(maskfile)
unknown_data.mask(maskfile)

print('Normalize spectra by specifying the wavelength ranges over which to normalize')
ranges3=[(0,350),(350,470),(470,1000)] #this is equivalent to "norm3"

print('Norm3 data')
data3=data
data3.norm(ranges3)
unknown_data3=unknown_data
unknown_data3.norm(ranges3)

data3.pca('wvl',nc=8)
unknown_data3.pca('wvl',load_fit=data3.do_pca)

x=data3.df['wvl'].columns.values
x=[x,x]
pcs=[data3.do_pca.components_[0,:],data3.do_pca.components_[1,:]]
plots.lineplot(x,pcs,figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",figname='PCA_loadings_test.png')

x=[data3.df[('PCA',1)],unknown_data3.df[('PCA',1)]]
y=[data3.df[('PCA',2)],unknown_data3.df[('PCA',2)]]
pc1_var=data3.do_pca.explained_variance_ratio_[0]*100
pc2_var=data3.do_pca.explained_variance_ratio_[1]*100

lbls=['Training','Unknown']
plots.scatterplot(x,y,xtitle='PC1 ('+str(round(pc1_var,1))+r'%)',ytitle='PC2 ('+str(round(pc2_var,1))+r'%)',figname='PCA_scores_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",lbls=lbls)

data3.ica('wvl',nc=8)
unknown_data3.ica('wvl',load_fit=data3.do_ica)


x=data3.df['wvl'].columns.values
x=[x,x]
ics=[data3.do_ica.components_[0,:],data3.do_ica.components_[1,:]]
plots.lineplot(x,ics,figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",figname='ICA_loadings_test.png')

x=[data3.df[('ICA',1)],unknown_data3.df[('ICA',1)]]
y=[data3.df[('ICA',2)],unknown_data3.df[('ICA',2)]]

lbls=['Training','Unknown']
plots.scatterplot(x,y,xtitle='IC1',ytitle='IC2',figname='ICA_scores_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",lbls=lbls)

data3.ica_jade('wvl',nc=8)
#unknown_data3.ica_jade('wvl',load_fit=data3.ica_jade_loadings)

x=data3.df['wvl'].columns.values
x=[x,x]
ics=[data3.ica_jade_loadings[0,:].T,data3.ica_jade_loadings[1,:].T]
plots.lineplot(x,ics,figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",figname='ICA_jade_sources_test.png')

x=[data3.df[('ICA_JADE',1)]]#,unknown_data3.df[('ICA_JADE',1)]]
y=[data3.df[('ICA_JADE',2)]]#,unknown_data3.df[('ICA_JADE',2)]]

lbls=['Training']
plots.scatterplot(x,y,xtitle='IC1',ytitle='IC2',figname='ICA_jade_scores_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",lbls=lbls)

pass
    






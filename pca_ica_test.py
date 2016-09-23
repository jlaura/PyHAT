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
import itertools
from matplotlib import pyplot as plot

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

x=np.array(data3.df[('PCA',1)])
y=np.array(data3.df[('PCA',2)])
pc1_var=data3.do_pca.explained_variance_ratio_[0]*100
pc2_var=data3.do_pca.explained_variance_ratio_[1]*100
colors=[]
SiO2_colors=[]
CaO_colors=[]
Na2O_colors=[]
MgO_colors=[]
FeOT_colors=[]
K2O_colors=[]

for i in list(range(len(data3.df.index))):
    print(i)
    SiO2=data3.df[('meta','SiO2')].iloc[i]
    CaO=data3.df[('meta','CaO')].iloc[i]
    Na2O=data3.df[('meta','Na2O')].iloc[i]
    MgO=data3.df[('meta','MgO')].iloc[i]
    FeOT=data3.df[('meta','FeOT')].iloc[i]
    K2O=data3.df[('meta','K2O')].iloc[i]
    
    
    SiO2_colors.append(SiO2)
    CaO_colors.append(CaO)
    Na2O_colors.append(Na2O)
    MgO_colors.append(MgO)     
    FeOT_colors.append(FeOT)     
    K2O_colors.append(K2O)     
    
       
    SiO2=SiO2/(SiO2+CaO+Na2O)    
    CaO=SiO2/(SiO2+CaO+Na2O)    
    Na2O=SiO2/(SiO2+CaO+Na2O)    
    colors.append((SiO2,CaO,Na2O))


plots.scatterplot(x,y,xtitle='PC1 ('+str(round(pc1_var,1))+r'%)',ytitle='PC2 ('+str(round(pc2_var,1))+r'%)',figname='PCA_scores_SiO2_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",colors=SiO2_colors,alpha=1,cmap='viridis',colortitle='SiO2')
plots.scatterplot(x,y,xtitle='PC1 ('+str(round(pc1_var,1))+r'%)',ytitle='PC2 ('+str(round(pc2_var,1))+r'%)',figname='PCA_scores_CaO_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",colors=CaO_colors,alpha=1,cmap='viridis',colortitle='CaO')
plots.scatterplot(x,y,xtitle='PC1 ('+str(round(pc1_var,1))+r'%)',ytitle='PC2 ('+str(round(pc2_var,1))+r'%)',figname='PCA_scores_Na2O_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",colors=Na2O_colors,alpha=1,cmap='viridis',colortitle='Na2O')
plots.scatterplot(x,y,xtitle='PC1 ('+str(round(pc1_var,1))+r'%)',ytitle='PC2 ('+str(round(pc2_var,1))+r'%)',figname='PCA_scores_MgO_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",colors=MgO_colors,alpha=1,cmap='viridis',colortitle='MgO')
plots.scatterplot(x,y,xtitle='PC1 ('+str(round(pc1_var,1))+r'%)',ytitle='PC2 ('+str(round(pc2_var,1))+r'%)',figname='PCA_scores_FeOT_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",colors=FeOT_colors,alpha=1,cmap='viridis',colortitle='FeOT')
plots.scatterplot(x,y,xtitle='PC1 ('+str(round(pc1_var,1))+r'%)',ytitle='PC2 ('+str(round(pc2_var,1))+r'%)',figname='PCA_scores_K2O_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",colors=K2O_colors,alpha=1,cmap='viridis',colortitle='K2O')


plots.scatterplot(x,y,xtitle='PC1 ('+str(round(pc1_var,1))+r'%)',ytitle='PC2 ('+str(round(pc2_var,1))+r'%)',figname='PCA_scores_gradient_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",colors=colors,alpha=1)


print('Do ICA using FastICA algorithm')
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

print('Do ICA using JADE algorithm')
data3.ica_jade('wvl',nc=8)
#unknown_data3.ica_jade('wvl',load_fit=data3.ica_jade_loadings)

x=data3.df['wvl'].columns.values
ics=[data3.ica_jade_loadings[0,:].T,data3.ica_jade_loadings[1,:].T]

f,ax=plot.subplots(8,sharex=True)

ax[0].plot(x,data3.ica_jade_loadings[0,:].T)
ax[1].plot(x,data3.ica_jade_loadings[1,:].T)
ax[2].plot(x,data3.ica_jade_loadings[2,:].T)
ax[3].plot(x,data3.ica_jade_loadings[3,:].T)
ax[4].plot(x,data3.ica_jade_loadings[4,:].T)
ax[5].plot(x,data3.ica_jade_loadings[5,:].T)
ax[6].plot(x,data3.ica_jade_loadings[6,:].T)
ax[7].plot(x,data3.ica_jade_loadings[7,:].T)
plot.savefig(r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output\ICA_loadings_JADE_test.png",dpi=1000)
plot.show()


#plots.lineplot(x,ics,figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",figname='ICA_jade_sources_test.png')

x=[data3.df[('ICA_JADE',1)]]#,unknown_data3.df[('ICA_JADE',1)]]
y=[data3.df[('ICA_JADE',2)]]#,unknown_data3.df[('ICA_JADE',2)]]

lbls=['Training']
plots.scatterplot(x,y,xtitle='IC1',ytitle='IC2',figname='ICA_jade_scores_test.png',figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output",lbls=lbls)

pass
    






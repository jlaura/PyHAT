# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 13:09:21 2016

@author: rbanderson
"""
from matplotlib import pyplot as plot
import numpy as np
import itertools
import pysat.plotting.colormaps as colormaps

def cmaps():
    plot.register_cmap(name='viridis',cmap=colormaps.viridis)
    plot.register_cmap(name='magma',cmap=colormaps.magma)
    plot.register_cmap(name='inferno',cmap=colormaps.inferno)
    plot.register_cmap(name='plasma',cmap=colormaps.plasma)
    

def scatterplot(x,y,figpath,figfile=None,xrange=None,yrange=None,xtitle='Reference (wt.%)',ytitle='Prediction (wt.%)',title=None,
                lbls=None,one_to_one=False,dpi=1000,
                colors=None,annot_mask=None,alpha=0.4,cmap=None,colortitle='',loadfig=None):
    if loadfig is not None:
        fig=loadfig
        axes=fig.gca()
    else:
        fig=plot.figure()
            
        axes=fig.gca()
        if title:
            fig.suptitle(title)        
        if xtitle:
            axes.set_xlabel(xtitle)
        if ytitle:
            axes.set_ylabel(ytitle)
        if xrange:
            axes.xlim(xrange)
    #    else:
    #        plot.xlim([0.9*np.min([0,np.min(x)]),1.1*np.max(x)])
    #        
        if yrange:
            axes.ylim(yrange)
#    else:
#        plot.ylim([0.9*np.min([0,np.min(y)]),np.min([100,1.1*np.max(y)])])
    
    if one_to_one:
        axes.plot([0, 100], [0, 100],color='k')
    
    if cmap is not None:
        axes.scatter(x,y,c=colors,edgecolors='k',linewidth=0.2,alpha=alpha,cmap=cmap)  
        axes.colorbar(label=colortitle)
    else:
        try:
            if colors is not None:
                axes.scatter(x,y,color=colors,edgecolors='k',linewidth=0.2,alpha=alpha,label=lbls)
                
        except:
            if colors==None:
                colors=itertools.cycle(['r','g','b','c','m','y',])
            
            if annot_mask==None:
                annot_mask=[None]*len(x)
            if lbls==None:
                lbls=['']*len(x)
        
            for i in np.arange(len(x)):
                axes.scatter(x[i],y[i],color=next(colors),label=lbls[i],edgecolors='k',linewidth=0.2,alpha=alpha)
                if annot_mask[i] is not None:
                    axes.scatter(x[i][annot_mask[i]],y[i][annot_mask[i]],facecolors='none',edgecolors='k',linewidth=1.0,label='RANSAC Outliers')
       
    
    axes.legend(loc='best',fontsize=8,scatterpoints=1)
    if figpath and figfile:
        fig.savefig(figpath+'/'+figfile,dpi=dpi)
    return fig
        
def lineplot(x,y,xrange=None,yrange=None,xtitle='',ytitle='',title=None,
                lbls=None,figpath=None,figfile=None,dpi=1000,
                colors=None,alphas=None,loadfig=None):
    if colors==None:
        colors=itertools.cycle(['r','g','b','c','m','y',])
    else:
        colors=itertools.cycle(colors)
        
    if alphas==None:
        alphas=itertools.cycle([1.0])
    else:
        alphas=itertools.cycle(alphas)
        
    if lbls==None:
        lbls=['']*len(x)
        
    if loadfig is not None:
        fig=loadfig
        axes=fig.gca()
    else:
        fig=plot.figure()
            
        axes=fig.gca()
        if title:
            axes.suptitle(title)
        if xtitle:
            axes.set_xlabel(xtitle)
        if ytitle:
            axes.set_ylabel(ytitle)
        if xrange:
            axes.xlim(xrange)
        if yrange:
            axes.ylim(yrange)

    for i in np.arange(len(x)):
        plot.plot(x[i],y[i],color=next(colors),label=lbls[i],linewidth=1,alpha=next(alphas))
    
    axes.legend(loc='best',fontsize=8)
    if figpath and figfile:
        fig.savefig(figpath+'/'+figfile,dpi=dpi)
    return fig
    
def pca_ica_plot(data,x_component,y_component,colorvar=None,cmap='viridis',method='PCA',figpath=None,figfile=None):
    cmaps()    
    

    x=[data.df[(method,x_component)]]
    y=[data.df[(method,y_component)]]
    if method=='PCA':
        x_loading=data.do_pca.components_[x_component,:]
        y_loading=data.do_pca.components_[y_component,:]
        
        x_variance=data.do_pca.explained_variance_ratio_[x_component]*100
        y_variance=data.do_pca.explained_variance_ratio_[y_component]*100
        x_label='PC '+str(x_component)+' ('+str(round(x_variance,1))+r'%)'       
        y_label='PC '+str(y_component)+' ('+str(round(y_variance,1))+r'%)'       
        
    if method=='ICA_JADE':
        x_loading=data.ica_jade_loadings[x_component,:].T
        y_loading=data.ica_jade_loadings[y_component,:].T
        x_label='Source '+str(x_component)  
        y_label='Source '+str(y_component)       
        
    #set up the subplots
    fig=plot.figure()
    fig.set_size_inches(10,4)
    ax1=fig.add_subplot(2,2,(1,3))
    ax2=fig.add_subplot(2,2,2)
    ax3=fig.add_subplot(2,2,4,xlabel='Wavelength (nm)')

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    
    if colorvar:
        mappable=ax1.scatter(x,y,c=data.df[colorvar],cmap=cmap,linewidth=0.2) 
        fig.colorbar(mappable,label=colorvar[1],ax=ax1)    
    else:
        mappable=ax1.scatter(x,y,linewidth=0.2) 
    
    #plot the loadings
    wvls=data.df['wvl'].columns.values
    ax2.plot(wvls,x_loading)
    ax3.plot(wvls,y_loading)
    
    ax2.set_yticklabels([])
    ax2.set_xticklabels([])
    ax2.set_ylabel(x_label)
    
    ax3.set_yticklabels([])
    ax3.set_ylabel(y_label)
    
    fig.subplots_adjust(hspace=0)
    
    if figpath and figfile:
        fig.savefig(figpath+'\\'+figfile,dpi=1000)    
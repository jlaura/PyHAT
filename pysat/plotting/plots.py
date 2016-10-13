# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 13:09:21 2016

@author: rbanderson
"""
from matplotlib import pyplot as plot
import numpy as np
import itertools
import colormaps

def scatterplot(x,y,xrange=None,yrange=None,xtitle='Reference (wt.%)',ytitle='Prediction (wt.%)',title=None,
                lbls=None,one_to_one=False,figpath=None,figname=None,dpi=1000,
                colors=None,annot_mask=None,alpha=0.4,cmap=None,colortitle=''):
    plot.figure()
    plot.register_cmap(name='viridis',cmap=colormaps.viridis)
    plot.register_cmap(name='magma',cmap=colormaps.magma)
    plot.register_cmap(name='inferno',cmap=colormaps.inferno)
    plot.register_cmap(name='plasma',cmap=colormaps.plasma)
    
    if title:
        plot.title(title)
    if xtitle:
        plot.xlabel(xtitle)
    if ytitle:
        plot.ylabel(ytitle)
    if xrange:
        plot.xlim(xrange)
#    else:
#        plot.xlim([0.9*np.min([0,np.min(x)]),1.1*np.max(x)])
#        
    if yrange:
        plot.ylim(yrange)
#    else:
#        plot.ylim([0.9*np.min([0,np.min(y)]),np.min([100,1.1*np.max(y)])])
    
    if one_to_one:
        plot.plot([0, 100], [0, 100],color='k')
    
    if cmap is not None:
        plot.scatter(x,y,c=colors,edgecolors='black',linewidth=0.2,alpha=alpha,cmap=cmap)  
        plot.colorbar(label=colortitle)
    else:
        try:
            if isinstance(colors[0],tuple):
                plot.scatter(x,y,color=colors,edgecolors='black',linewidth=0.2,alpha=alpha)  
        except:
            if colors==None:
                colors=itertools.cycle(['r','g','b','c','m','y',])
            
            if annot_mask==None:
                annot_mask=[None]*len(x)
            if lbls==None:
                lbls=['']*len(x)
        
            for i in np.arange(len(x)):
                plot.scatter(x[i],y[i],color=next(colors),label=lbls[i],edgecolors='black',linewidth=0.2,alpha=alpha)
                if annot_mask[i] is not None:
                    plot.scatter(x[i][annot_mask[i]],y[i][annot_mask[i]],facecolors='none',edgecolors='black',linewidth=1.0,label='RANSAC Outliers')
       
    
            plot.legend(loc='best',fontsize=8,scatterpoints=1)
    if figpath and figname:
        plot.savefig(figpath+'/'+figname,dpi=dpi)
        
def lineplot(x,y,xrange=None,yrange=None,xtitle='',ytitle='',title=None,
                lbls=None,figpath=None,figname=None,dpi=1000,
                colors=None,alphas=None):
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
        
    plot.figure()
    if title:
        plot.title(title)
    if xtitle:
        plot.xlabel(xtitle)
    if ytitle:
        plot.ylabel(ytitle)
    for i in np.arange(len(x)):
        plot.plot(x[i],y[i],color=next(colors),label=lbls[i],linewidth=1,alpha=next(alphas))
    if xrange:
        plot.xlim(xrange)
    if yrange:
        plot.ylim(yrange)
    else:
        pass#plot.ylim([0,np.max(y[-np.isnan(y)])])  --- This was causing issues, comment out for now
    
    plot.legend(loc='best',fontsize=8)
    if figpath and figname:
        plot.savefig(figpath+'/'+figname,dpi=dpi)
    
    
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 13:09:21 2016

@author: rbanderson
"""
from matplotlib import pyplot as plot
import numpy as np
import itertools

def scatterplot(x,y,xrange=None,yrange=None,xtitle=None,ytitle=None,title=None,
                lbls=None,one_to_one=False,figpath=None,figname=None,dpi=1000,
                colors=None,annot_mask=None):
    if colors==None:
        colors=itertools.cycle(['r','g','b','c','m','y',])

    
    plot.figure()
    if title:
        plot.title(title)
    if xtitle:
        plot.xlabel(xtitle)
    if ytitle:
        plot.ylabel(ytitle)
    if one_to_one:
        plot.plot([0, 100], [0, 100],color='k')
    for i in np.arange(len(x)):
        plot.scatter(x[i],y[i],color=next(colors),label=lbls[i],edgecolors='black',linewidth=0.2,alpha=0.6)

    if annot_mask is not None:
        print(len(annot_mask))
        plot.scatter(x[i][annot_mask[i]],y[i][annot_mask[i]],facecolors='none',edgecolors='black',linewidth=0.5)
    if xrange:
        plot.xlim(xrange)
    else:
        plot.xlim([0.9*np.min([0,np.min(x)]),1.1*np.max(x)])
        
    if yrange:
        plot.ylim(yrange)
    else:
        plot.ylim([0.9*np.min([0,np.min(y)]),1.1*np.max(y)])

    plot.legend(loc='best',fontsize=8,scatterpoints=1)
    if figpath and figname:
        plot.savefig(figpath+'/'+figname,dpi=dpi)
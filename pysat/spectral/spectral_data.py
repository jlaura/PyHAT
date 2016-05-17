from pysat.spectral.interp import interp_spect
from pysat.spectral.mask import mask
from pysat.utils.folds import random
from pysat.spectral.norm_total import norm_total

__authors__ = 'rbanderson'

class spectral_data(object):
    def __init__(self,df):
        self.df=df
    
    def interp(self,*args,**kwargs):
        return spectral_data(interp_spect(self.df,*args,**kwargs))
    
    def mask(self,*args,**kwargs):
        return spectral_data(mask(self.df,*args,**kwargs))
        
    def random_folds(self,*args,**kwargs):
        return spectral_data(random(self.df,*args,**kwargs))
        
    def norm(self,*args,**kwargs):
        return spectral_data(norm_total(self.df,*args,**kwargs))


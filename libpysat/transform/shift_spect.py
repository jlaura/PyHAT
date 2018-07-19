import pandas as pd
from libpysat.transform.interp import interp
import copy
import numpy as np
def shift_spect(df,shift):
    df_copy = copy.deepcopy(df)

    wvls = df['wvl'].columns.values #get the original wavelength values
    df_spect = df['wvl'] #extract just the spectra from the data frame
    df = df.drop('wvl',axis=1)
    newcols = [('wvl',i+shift) for i in df_spect.columns.values]
    df_spect.columns = pd.MultiIndex.from_tuples(newcols)
    df = pd.concat([df_spect, df], axis=1)
    df = interp(df,wvls)
    df[('meta','Shift')] = shift
    return df

#This function interpolates the spectra in one data frame onto a new set of wavelenths.
# Typically used to get data from different instruments onto the same set of weavelengths so they can be used together.
import numpy as np
import scipy as sp
import pandas as pd

def interp(df, xnew):
    xnew = np.array(xnew, dtype='float')

    metadata_cols = df.columns.levels[0] != 'wvl'
    metadata = df[df.columns.levels[0][metadata_cols]]
    old_wvls = np.array(df['wvl'].columns, dtype='float')
    old_spectra = np.array(df['wvl'])
    new_spectra = np.empty([len(old_spectra[:, 0]), len(xnew)]) * np.nan
    interp_index = (xnew > min(old_wvls)) & (xnew < max(old_wvls))

    f = sp.interpolate.interp1d(old_wvls, old_spectra, axis=1)
    new_spectra[:, interp_index] = f(xnew[interp_index])

    xnew = list(xnew)
    for i, x in enumerate(xnew):
        xnew[i] = ('wvl', x)

    new_df = pd.DataFrame(new_spectra, columns=pd.MultiIndex.from_tuples(xnew), index=df.index)
    new_df = pd.concat([new_df, metadata], axis=1)

    df = new_df
    return df
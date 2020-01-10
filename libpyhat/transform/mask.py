# This function masks out specified ranges of the data
import pandas as pd
import numpy as np

def mask(df, maskfile, maskvar='wvl'):
    df_spectra = df[maskvar]  # extract just the spectra from the data frame
    metadata_cols = df.columns.levels[0] != maskvar  # extract just the metadata
    metadata = df[df.columns.levels[0][metadata_cols]]

    mask = pd.read_csv(maskfile, sep=',')  # read the mask file
    tmp = []
    for i in mask.index:
        tmp.append((np.array(df[maskvar].columns, dtype='float') >= mask.ix[i, 'min_wvl']) & (
            np.array(df[maskvar].columns, dtype='float') <= mask.ix[i, 'max_wvl']))

    # combine the indexes for each range in the mask file into a single masking vector and use that to mask the spectra
    masked = np.any(np.array(tmp), axis=0)
    spectcols = list(df_spectra.columns)  # get the list of columns in the spectra dataframe
    for i, j in enumerate(masked):  # change the first level of the tuple from 'wvl' to 'masked' where appropriate
        if j == True:
            spectcols[i] = ('masked', spectcols[i])
        else:
            spectcols[i] = (maskvar, spectcols[i])
    df_spectra.columns = pd.MultiIndex.from_tuples(
        spectcols)  # assign the multiindex columns based on the new tuples
    df = pd.concat([df_spectra, metadata], axis=1)  # merge the masked spectra back with the metadata
    return df
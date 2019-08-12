import pandas as pd
import numpy as np
import os
import fnmatch
from plio.io import io_spectral_profiler

import libpyhat


def spectral_profiler(f, **kwargs):
        """
        Generate DataFrame from spectral profiler data.

        parameters
        ----------
        f : str
            file path to spectral profiler file

        tolerance : Real
                    Tolerance for floating point index
        """
        geo_data = io_spectral_profiler.Spectral_Profiler(f)
        meta = geo_data.ancillary_data
        meta.index.names = ['id']
        df = geo_data.spectra.transpose()
        df.index.names = ['id', 'minor']
        joined = df.join(meta, how='inner').transpose()

        return libpyhat.Spectra(joined, wavelengths=geo_data.wavelengths,
                                        metadata=meta.columns,
                                        index=joined.index,
                                        columns=joined.columns,
                                        **kwargs)


DRIVERS = [spectral_profiler]

def read_file(filename, **kwargs):
    #try:
    for d in DRIVERS:
        return d(filename, **kwargs)
    #except:
    #    return

"""
This function uses the pandas merge ability to look up metadata for an existing dataframe in a csv file
If lookupfile is a list, then each file will be read and concatenated together. Alternatively, a dataframe can be provided directly.
The default settings are for looking up ChemCam CCS csv data in the ChemCam master list files, matching on sclock value
"""

def lookup(df,lookupfile=None,lookupdf=None,sep=',',skiprows=1,left_on='sclock',right_on='Spacecraft Clock'):
    if lookupfile is not None:
        # this loop concatenates together multiple lookup files if provided
        for x in lookupfile:
            try:
                tmp = pd.read_csv(x, sep=sep, skiprows=skiprows, error_bad_lines=False)
                lookupdf = pd.concat([lookupdf, tmp])
            except:
                lookupdf = pd.read_csv(x, sep=sep, skiprows=skiprows, error_bad_lines=False)
    metadata = df['meta']

    metadata = metadata.merge(lookupdf, left_on=left_on, right_on=right_on, how='left')

    # remove metadata columns that already exist in the data frame to avoid non-unique columns
    meta_cols = set(metadata.columns.values)
    meta_cols_keep = list(meta_cols - set(df['meta'].columns.values))
    metadata = metadata[meta_cols_keep]

    # make metadata into a multiindex
    metadata.columns = [['meta'] * len(metadata.columns), metadata.columns.values]
    # give it the same indices as the df
    metadata.index = df.index
    # combine the df and the new metadata
    df = pd.concat([metadata, df], axis=1)
    return df

def file_search(searchdir, searchstring):
    # Recursively search for files in the specified directory
    filelist = []
    for root, dirnames, filenames in os.walk(searchdir):
        for filename in fnmatch.filter(filenames, searchstring):
            filelist.append(os.path.join(root, filename))
    filelist = np.array(filelist)
    return filelist
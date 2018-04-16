import pandas as pd
import numpy as np

from plio.io import io_spectral_profiler, io_moon_minerology_mapper

from . import hcube as hc
import libpysat


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

        meta = meta.transpose()
        meta.columns.names = ['id']
        df = geo_data.spectra.to_frame().unstack(level=1)
        df.columns.names = ['id', 'minor']
        
        joined = df.transpose().join(meta.transpose(), how='inner').transpose()
        
        return libpysat.Spectra(joined, wavelengths=df.index,
                                           metadata=meta.index,
                                           index=joined.index,
                                           columns=joined.columns,
                                           **kwargs)


def m3(f, tolerance = 2, waxis = 0):
    """
    Generate DataFrame from spectral profiler data.
    parameters
    ----------
    f : str
        file path to spectral profiler file
    tolerance : Real
                Tolerance for floating point index
    """

    wavelengths, _, ds = io_moon_minerology_mapper.openm3(f)
    m3_array = ds.ReadAsArray()

    return hc.HCube(m3_array, wavelengths, waxis = waxis, tolerance=tolerance)

DRIVERS = [spectral_profiler]

def read_file(filename, **kwargs):
    #try:
    for d in DRIVERS:
        return d(filename, **kwargs)
    #except:
    #    return
from pandas import DataFrame, Series, to_numeric
import random as rand

import numpy as np

from numbers import Real
from numbers import Number

from functools import reduce
from functools import singledispatch

from . import io
from .base import PySatBase
from libpysat.data import _index as _idx
from .spectrum import Spectrum
from ..transform import continuum
from ..utils import utils

import libpysat

class Spectra(PySatBase, DataFrame):
    """
    A pandas derived DataFrame used to store spectral and hyper-spectral observations.

    attributes
    ----------

    wavelengths : pandas.Float64Index
                  The wavelengths store as a pandas index

    get : PandasLocIndexer
          Indexing object, maps wavelengths to indices enabling access a tolerance for
          floating point labels.

    ----------
    """

    # attributes that carry over on operations
    _metadata = ['wavelengths', '_metadata_index', '_tolerance']


    def __init__(self, *args, **kwargs):
        wavelengths = kwargs.pop('wavelengths', None)
        metadata_index = kwargs.pop('metadata', None)
        tolerance = kwargs.pop('tolerance', 2)
        super(Spectra, self).__init__(*args, **kwargs)
        
        self.wavelengths = wavelengths
        self._metadata_index = metadata_index
        self.tolerance = tolerance
        self._reindex()

    @property
    def data(self):
        # Trying to support indices as either index or column
        wv = np.round(self.wavelengths, self.tolerance)
        try:
            return self[wv]
        except:
            return self.loc[wv]

    @property
    def _constructor_sliced(self):
        """
        Returns constructor used when dataframe dimension decreases (i.e. goes from a dataframe
        to a series).
        """
        return Spectrum

    @property
    def _constructor(self):
        return Spectra

    def __finalize__(self, other, method=None, **kwargs):
        """propagate metadata from other to self """
        # merge operation: using metadata of the left object
        if method == 'merge':
            for name in self._metadata:
                object.__setattr__(self, name, getattr(other.left, name, None))
        # concat operation: using metadata of the first object
        elif method == 'concat':
            for name in self._metadata:
                object.__setattr__(self, name, getattr(other.objs[0], name, None))
        else:
            for name in self._metadata:
                object.__setattr__(self, name, getattr(other, name, None))
        return self

    def __getitem__(self, key):
        """
        overrides ndarray's __getitem__ to use .get's floating point tolerance for
        floating point indexes.

        parameters
        ----------
        key : object
              the column labels to access on

        """
        result = super(Spectra, self).__getitem__(key)
        if isinstance(result, Series):
            result.__class__ = Spectrum
            result.wavelengths = self.wavelengths
            result.tolerance = self.tolerance
            result._metadata_index = self._metadata_index
            self._reindex()
        elif isinstance(result, DataFrame):
            result.__class__ = Spectra
            result.wavelengths = self.wavelengths
            result.tolerance = self.tolerance
            result._metadata_index = self._metadata_index
            self._reindex()
        return result
        #if isinstance(self.index, pd.MultiIndex):
        #    return self.get[:,:,key]
        #else:
        #     return self.get[:,key]


    @classmethod
    def from_file(cls, filename, **kwargs):

        return io.read_file(filename, **kwargs)

    '''@classmethod
    def from_spectral_profiler(cls, f, tolerance=1):
        """
        Generate DataFrame from spectral profiler data.

        parameters
        ----------
        f : str
            file path to spectral profiler file

        tolerance : Real
                    Tolerance for floating point index
        """
        return io.spectral_profiler(f, tolerance=tolerance)'''

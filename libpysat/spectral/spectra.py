import pandas as pd
import random as rand

import numpy as np

from numbers import Real
from numbers import Number

from functools import reduce

from _subindices import _get_subindices


class SpectrumLocIndexer(pd.core.indexing._LocIndexer):
    """
    """

    @property
    def tolerance(self):
        if not hasattr(self, '_tolerance'):
            self._tolerance = .5
        return self._tolerance


    @tolerance.setter
    def tolerance(self, val):
        self._tolerance = val


    def __getitem__(self, key):
        try:
            x,y,columns = None, None, self.obj.wavelengths

            if isinstance(self.obj.index, pd.MultiIndex):
                x,y = self.obj.index.levels
                indexes = x,y, self.obj.wavelengths
                subindices = _get_subindices(key, indexes, tolerance=self._tolerance)

                x = subindices[0:1] if subindices[0:1] else tuple([slice(None, None)])
                y = subindices[1:2] if subindices[1:2] else tuple([slice(None, None)])
                columns = subindices[2:3] if subindices[2:3] else tuple([slice(None, None)])

                columns = columns[0]
                if isinstance(columns, pd.Index):
                    columns = columns.union(self.obj.metadata)

                subindices = tuple([[x[0], y[0]], columns])

            else:
                x = self.obj.index
                indexes = x,columns
                subindices = _get_subindices(key, indexes, tolerance=self._tolerance)

                x = subindices[0:1] if subindices[0:1] else tuple([slice(None, None)])
                columns = subindices[1:2] if subindices[1:2] else tuple([slice(None, None)])

                columns = columns[0]
                if isinstance(columns, pd.Index):
                    columns = columns.union(self.obj.metadata)

                subindices = tuple([x[0], columns])


            subframe = super(SpectrumLocIndexer, self).__getitem__(subindices)

        except Exception as e:
            subframe = super(SpectrumLocIndexer, self).__getitem__(key)

        if isinstance(subframe, Spectrum):
            subframe.wavelengths = self.obj.wavelengths
            subframe.metadata = self.obj.metadata

        return subframe


class SpectrumiLocIndexer(pd.core.indexing._iLocIndexer):
    """
    """

    def __getitem__(self, key):
        subframe = super(SpectrumiLocIndexer, self).__getitem__(key)

        if isinstance(subframe, Spectrum):
            subframe.wavelengths = self.obj.wavelengths
            subframe.metadata = self.obj.metadata

        return subframe


class Spectrum(pd.Series):

    _metadata = ['_loc', 'wavelengths', 'metadata']

    def __init__(self, *args, **kwargs):
        wavelengths = kwargs.pop('wavelengths', None)
        metadata = kwargs.pop('metadata', None)
        _loc = kwargs.pop('loc', None)
        super(Spectrum, self).__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return Spectrum

    @property
    def _constructor_expanddim(self):
        return pd.DataFrame


class Spectra(object):
    """
    """

    def __init__(self, df = None, wavelengths={}, metadata={}, tolerance=.5):
        if df is not None:
            self._data = df
        else:
            self._data = pd.DataFrame()

        self.wavelengths = pd.Float64Index(wavelengths)
        self.metadata = metadata

        if isinstance(df, pd.DataFrame):
            self.metadata = df.columns.difference(self.wavelengths)
        else:
            self.metadata = df.index.difference(self.wavelengths)

        loc_name = self._data.loc.name
        iloc_name = self._data.iloc.name
        self._iloc = SpectrumiLocIndexer(name=iloc_name, obj=self)
        self._loc = SpectrumLocIndexer(name=loc_name, obj=self)
        self._loc.tolerance = tolerance

        self._get_axis = self._data._get_axis
        self._get_axis_name = self._data._get_axis_name
        self._slice = self._data._slice
        self._xs = self._data._xs
        self._ixs = self._data._ixs
        self._data._constructor_sliced = Spectrum
        self._take = self._data._take


    def __repr__(self):
        return self._data.__repr__()


    @property
    def loc(self):
        return self._loc


    @property
    def iloc(self):
        return self._iloc

    @property
    def take(self):
        return self._data.take


    def head(self, n=5):
        return self._data.head()


    @property
    def index(self):
        return self._data.index

    @property
    def columns(self):
        return self._data.columns

    @property
    def ndim(self):
        return self._data.ndim

    @property
    def sort_index(self):
        return self._data.sort_index

    @property
    def reindex(self):
        return self._data.reindex


    @property
    def axes(self):
        return self._data.axes


    @property
    def iterrows(self):
        return self._data.iterrows


    def apply(self, func, *args, **kwargs):
        return self._data.apply(func, *args, **kwargs)


    def apply_spectra(self, func, *args, **kwargs):
        self._data = self.apply(func, args, axis=1, **kwargs)


    @property
    def tolerance(self):
        if not hasattr(self._loc, '_tolerance'):
            self._loc._tolerance = .5
        return self._loc._tolerance


    @tolerance.setter
    def tolerance(self, val):
        self._loc._tolerance = val

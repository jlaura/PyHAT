import pandas as pd
import random as rand

import numpy as np

from numbers import Real
from numbers import Number

from functools import reduce

from libpysat.spectral._subindices import _get_subindices
from libpysat.utils.utils import linear_correction

from plio.io import io_spectral_profiler
from plio.io import io_moon_minerology_mapper

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

                subindices = tuple([tuple([x[0], y[0]]), columns])

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

        else:
            subframe = Spectra(subframe, self.obj.wavelengths, self.tolerance)

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


    @classmethod
    def from_spectral_profiler(cls, f, tolerance=.5):
        """
        """
        geo_data = io_spectral_profiler.Spectral_Profiler(f)
        meta = geo_data.ancillary_data

        df = geo_data.spectra.to_frame().unstack(level=1)
        df = df.transpose()
        df = df.swaplevel(0,1)

        df.index.names = ['minor', 'id']
        meta.index.name = 'id'

        wavelengths = df.columns

        df = df.reset_index().merge(meta.reset_index(), on='id')
        df = df.set_index(['minor', 'id'], drop=True)

        return cls(df, wavelengths, tolerance=tolerance)

    @classmethod
    def from_m3(cls, path_to_file):
        """
        """
        wavelengths, _, ds = io_moon_minerology_mapper.openm3(path_to_file)

        m3_array = ds.ReadAsArray().swapaxes(0, 2)
        m3_array = np.reshape(m3_array, (-1, m3_array.shape[-1]), order = "A")

        coords = [(i%ds.RasterXSize, i//ds.RasterXSize) for i in range(ds.RasterXSize * ds.RasterYSize)]
        index = pd.MultiIndex.from_tuples(coords, names = ['x', 'y'])
        m3_df = pd.DataFrame(data = m3_array, columns = wavelengths, index = index)

        meta = ds.GetMetadata_Dict()
        metadata = meta.keys()
        meta_df = pd.DataFrame(meta, index = index)

        spectra_df = m3_df.merge(meta_df, left_index = True, right_index = True)
        spectra_df.sort_index(inplace = True)
        return cls(spectra_df, wavelengths, metadata, 2)


    def __repr__(self):
        return self._data.__repr__()


    def linear_correction(self):
        """
        apply linear correction to all spectra
        """
        wavelengths = self.wavelengths.__array__()
        bands = tuple([0, len(wavelengths)-1])

        def lincorr(row):
            """
            Should be rewritten to be more apply friendly
            """
            corr, y = linear_correction(bands, row[wavelengths].__array__(), wavelengths)
            return Spectrum(corr, index=wavelengths)

        data = self._data.apply(lincorr, axis=1)
        return Spectra(data, self.wavelengths, tolerance = self.tolerance)


    def __getitem__(self, *args, **kwargs):
        df = self._data.__getitem__(*args,**kwargs)
        return Spectra(df, wavelengths=self.wavelengths, tolerance=self.tolerance)

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
        return self._data.head(n)


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

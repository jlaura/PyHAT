import pandas as pd
import random as rand

import numpy as np

from numbers import Real
from numbers import Number

from functools import reduce
from functools import singledispatch

from plio.io import io_spectral_profiler


from . import _index as _idx

from .continuum import lincorr

from libpysat.utils.utils import linear_correction
from libpysat.utils.utils import method_singledispatch



class Spectrum(pd.Series):

    _metadata = ['_loc', 'wavelengths', 'metadata', 'tolerance']

    def __init__(self, *args, wavelengths=[], metadata=[], tolerance=.5, **kwargs):
        super(Spectrum, self).__init__(*args, **kwargs)

        self._get = _idx.SpectrumLocIndexer(name='loc', obj=self)
        self._get._tolerance = tolerance

        self.wavelengths = wavelengths
        self.metadata = metadata


    @property
    def _constructor(self):
        return Spectrum


    @property
    def _constructor_expanddim(self):
        return pd.DataFrame


    def linear_correction(self):
        """
        apply linear correction to all spectra
        """
        return lincorr(self)


    @property
    def tolerance(self):
        if not hasattr(self._get, '_tolerance'):
            self._get._tolerance = .5
        return self._get._tolerance


    @tolerance.setter
    def tolerance(self, val):
        self._get._tolerance = val


    @property
    def get(self):
        return self._get


class Spectra(object):

    @method_singledispatch
    def __new__(self, data, *args, **kwargs):
        raise NotImplementedError('Not a supported datatype {}'.format(type(data)))


    @__new__.register(pd.DataFrame)
    def _(self, data, *args, **kwargs):
        return _Spectra_DataFrame(data, *args, **kwargs)


    @__new__.register(np.ndarray)
    def _(self, data, *args, **kwargs):
        return _SpectraArray(data, *args, **kwargs)


    @__new__.register(Real)
    def _(self, data, *args, **kwargs):
        return _SpectraArray([data], *args, **kwargs)


    @classmethod
    def from_spectral_profiler(cls, f, tolerance=1):
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

        return cls(df, wavelengths=wavelengths, tolerance=tolerance)


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



class _SpectraDataFrame(pd.DataFrame):
    """
    """

    # attributes that carry over on operations
    _metadata = ['_get', '_iget', 'wavelengths', 'metadata']


    def __init__(self, *args, wavelengths = [], metadata = [], tolerance=0, **kwargs):
        """
        """
        super(_Spectra_DataFrame, self).__init__(*args, **kwargs)

        get_name = self.loc.name
        iget_name = self.iloc.name
        self._iget = _idx.SpectrumiLocIndexer(name=iget_name, obj=self)
        self._get = _idx.SpectrumLocIndexer(name=get_name, obj=self)

        self._get._tolerance = tolerance
        self.wavelengths = pd.Float64Index(wavelengths)

        if metadata:
            self.metadata = pd.Index(metadata)
        else:
            self.metadata = self.columns.difference(self.wavelengths)


    @property
    def _constructor_sliced(self):
        return Spectrum


    @property
    def _constructor(self):
        return _Spectra_DataFrame


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

        data = self.apply(lincorr, axis=1)
        return Spectra(data, wavelengths=self.wavelengths, tolerance = self.tolerance)


    def __getitem__(self, key):
        if isinstance(self.index, pd.MultiIndex):
            return self.get[:,:,key]
        else:
             return self.get[:,key]


    @property
    def get(self):
        return self._get


    @property
    def iget(self):
        return self._iget


    @property
    def meta(self):
        return self[self.metadata]


    @property
    def spectra(self):
        return self[self.wavelengths]


    def plot_spectra(self, *args, **kwargs):
        return self.T.plot(*args, **kwargs)


    @property
    def tolerance(self):
        if not hasattr(self._get, '_tolerance'):
            self._get._tolerance = .5
        return self._get._tolerance


    @tolerance.setter
    def tolerance(self, val):
        self._get._tolerance = val


class _SpectraArray(np.ndarray):

    def __new__(cls, ndarray, wavelengths=[], waxis=None, tolerance=.5):
        obj = np.asarray(ndarray).view(cls)
        obj.wavelengths = pd.Float64Index(wavelengths)
        obj._get = _idx.ArrayLocIndexer(obj=obj, waxis=waxis, tolerance=tolerance)
        return obj


    def __getitem__(self, keys):
        if hasattr(keys, '__iter__'):
            if self._get.waxis <= len(keys):
                # wavelength is being sliced
                wavelengths=self.wavelengths[keys[self._get.waxis]]
                newarr = super(_SpectraArray, self).__getitem__(keys)
                return _SpectraArray(newarr, wavelengths, self._get.waxis, self._get.tolerance)
            else:
                newarr = super(_SpectraArray, self).__getitem__(keys)
                return _SpectraArray(newarr, self.wavelengths, self._get.waxis, self._get.tolerance)
        else:
            if self._get.waxis == 0:
                # wavelength is being sliced
                wavelengths=wavelengths[keys[self._get.waxis]]
                newarr = super(_SpectraArray, self).__getitem__(keys)
                return _SpectraArray(newarr, wavelengths, self._get.waxis, self._get.tolerance)
            else:
                newarr = super(_SpectraArray, self).__getitem__(keys)
                return _SpectraArray(newarr, self.wavelengths, self._get.waxis, self._get.tolerance)


    @property
    def get(self):
        return self._get

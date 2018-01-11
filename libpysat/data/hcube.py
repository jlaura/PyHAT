import numpy as np

from functools import reduce
from functools import singledispatch

from plio.io import io_moon_minerology_mapper

from . import _index as _idx


class HCube(np.ndarray):
    """
    A Numpy derived array used to store spectral and hyper-spectral images.

    attributes
    ----------

    wavelengths : pandas.Float64Index
                  The wavelengths store as a pandas index

    get : ArrayLocIndexer
          Indexing object, maps wavelengths to indices allowing for access using
          band labels

    ----------
    """
    def __new__(cls, ndarray, wavelengths=[], waxis=None, tolerance=.5):
        obj = np.asarray(ndarray).view(cls)
        obj.wavelengths = pd.Float64Index(wavelengths)
        obj._get = _idx.ArrayLocIndexer(obj=obj, waxis=waxis, tolerance=tolerance)
        return obj


    def __getitem__(self, keys):
        """
        Override numpy's __getitem__ to crop axis labels if slicing accross the labeled axis (e.g
        the axis representing labels)

        parameters
        ----------
        keys : object
               a key or set of keys to access on

        returns
        -------
        : _SpectraArray
          copy of the subset of the array

        """
        if hasattr(keys, '__iter__'):
            if self._get.waxis <= len(keys):
                # wavelength is being sliced
                wavelengths=self.wavelengths[keys[self._get.waxis]]
                newarr = super(_SpectraArray, self).__getitem__(keys)
                return _SpectraArray(newarr, wavelengths, self._get.waxis, self._get.tolerance)
            else:
                newarr = super(_SpectraArray, self).__getitem__(keys)
                if isinstance(keys, slice):
                    return _SpectraArray(newarr, self.wavelengths, self._get.waxis, self._get.tolerance)
                else:
                    return _SpectraArray(newarr, [self.wavelengths], self._get.waxis, self._get.tolerance)
        else:
            if self._get.waxis == 0:
                # wavelength is being sliced
                wavelengths=self.wavelengths[keys[self._get.waxis]]
                newarr = super(_SpectraArray, self).__getitem__(keys)
                return _SpectraArray(newarr, wavelengths, self._get.waxis, self._get.tolerance)
            else:
                newarr = super(_SpectraArray, self).__getitem__(keys)
                return _SpectraArray(newarr, self.wavelengths, self._get.waxis, self._get.tolerance)


    def __repr__(self):
        wavelengths = str(self.wavelengths)
        waxis = str(self.get.waxis)
        array = super(HCube, self).__repr__()
        return "\n".join([wavelengths, waxis, array])

    @property
    def get(self):
        """
        Access the array using labeled indices.

        see also
        --------
        _SpectraDataFrame.get : label-wise access to a spectral dataframe
        ArrayLocIndexer : Enable label-wise access to numpy arrays
        """
        return self._get


    @property
    def tolerance(self):
        if not hasattr(self._get, '_tolerance'):
            self._get._tolerance = .5
        return self._get._tolerance


    @tolerance.setter
    def tolerance(self, val):
        self._get._tolerance = val


    def band(self, n):
        return self.get[:,:,n]

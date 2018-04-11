import numpy as np
from pandas import Index, concat

from ..transform import smooth

import libpysat

def _spectral_unary_op(this, new, preserve_metadata=True):

    # Create the new class with the metadata obj, but the
    # data only index
    if isinstance(this, libpysat.Spectrum):
        new = libpysat.Spectrum(new, wavelengths=this.wavelengths,
                        metadata=None,
                        tolerance=this.tolerance,
                        index=this.data.index)
    else:
        new = libpysat.Spectra(new, wavelengths=this.wavelengths,
            metadata=None,
            tolerance=this.tolerance,
            index=this.data.index, 
            columns=this.data.columns)

    if preserve_metadata:
        new = concat((new, this.metadata))
        new.metadata = this.metadata
    return new

class PySatBase(object):

    def continuum_correct(self, func):
        print('CC')

    def smooth(self, func=libpysat.transform.smooth.boxcar, preserve_metadata='True', **kwargs):
        res = func(self.data.values, **kwargs)
        return _spectral_unary_op(self, res, preserve_metadata=preserve_metadata)

    @property
    def metadata(self):
        if self._metadata_index is not None:
            return self.loc[self._metadata_index]

    @metadata.setter
    def metadata(self, val):
        if hasattr(val, '__iter__') and not isinstance(val, (str, bytes)):
            self._metadata_index = val

    @property
    def tolerance(self):
        return self._tolerance
    
    @tolerance.setter
    def tolerance(self, val):
        if isinstance(val, int):
            self._tolerance = val
            self._reindex()
        else:
            raise TypeError

    def _reindex(self):
        if self.wavelengths is not None:
            wv = Index(np.round(self.wavelengths, decimals=self.tolerance))
            if self._metadata_index is not None:
                index = wv.append(Index(self._metadata_index))
            else:
                index = wv
            print(index)
            self.index = index
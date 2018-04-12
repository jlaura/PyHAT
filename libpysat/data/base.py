import numpy as np
from pandas import Index, concat

from ..transform import smooth

import libpysat

def _spectral_unary_op(this, new, preserve_metadata=True):
    """
    Wrapper for funcs that should return a spectral type

    Parameters
    ----------
    this : obj
           The parent or source Spectra/Spectrum that is operated on

    new : obj
          The return from the operation. Should be an ndarray, series,
          or dataframe
    
    preserve_metadata : bool
                        Whether or not the metadata should be added to 
                        the returned object if any metadata is present
                        on the parent (this) object. Default: True
    """

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

    def continuum_correct(self, nodes=[], correction_nodes=[],
                         func=libpysat.transform.continuum.linear, 
                         preserve_metadata=True,
                         **kwargs):
        if not nodes:
            nodes = [self.wavelengths[0], self.wavelengths[-1]]
        res, denom = libpysat.transform.continuum.continuum_correction(self.data.values,
                                                                       self.wavelengths,
                                                                       nodes=nodes,
                                                                       correction_nodes=correction_nodes,
                                                                       correction=func,
                                                                       **kwargs)
        res = _spectral_unary_op(self, res, preserve_metadata=preserve_metadata)
        return res, denom


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
            self.index = index
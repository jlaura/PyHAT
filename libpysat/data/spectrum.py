import pandas as pd

import numpy as np

from plio.io import io_spectral_profiler

from . import _index as _idx
from ..transform.continuum import lincorr


class Spectrum(pd.Series):
    """
    """
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

import numpy as np
from pandas import Index


class PySatBase(object):

    def continuum_correction(self):
        pass

    @property
    def metadata(self):
        if self._metadata_index:
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
        if self.wavelengths:
            wv = Index(np.round(self.wavelengths, decimals=self.tolerance))
            if self._metadata_index:
                index = wv.append(Index(self._metadata_index))
            else:
                index = wv
            self.index = index
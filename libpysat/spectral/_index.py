import pandas as pd
import random as rand

import numpy as np
from functools import singledispatch, update_wrapper

from multipledispatch import dispatch
from numbers import Real
from numbers import Number

from functools import reduce

from . import spectra as sp


@dispatch(Real, pd.Float64Index)
def _get_subindices(scalar, indices, tolerance=0):
    """
    Returns every index within the range [scalar +/- tolerance].

    >>> indices = pd.Float64Index([2.3, 3.55, 6.23, 9.99])
    >>> _get_subindices(10, indices, tolerance=.5)
    9.99

    Parameters
    ----------

    scalar : Number
             The scalar to access

    indices : pandas.Float64Index
              The index to access

    Returns
    -------

    : iterable
      the values that were inside the tolerance range for the scalar

    """

    start = scalar - tolerance
    stop = scalar + tolerance
    subindices = indices.where((indices >= start) & (indices <= stop)).dropna().astype(float)

    if subindices.size == 0:
        raise KeyError('{} is not in Index'.format(scalar))

    return subindices.__array__()


@dispatch((pd.Series, list, set, np.ndarray), pd.Float64Index)
def _get_subindices(iterable, indices, tolerance=0):
    """
    Returns every index within the range [scalar +/- tolerance] from a iterable of
    values.

    >>> l = [2, 9]
    >>> indices = pd.Float64Index([2.3, 3.55, 6.23, 9.99])
    >>> _get_subindices(l, indices, tolerance=.5)
    [2.3, 9.99]

    Parameters
    ----------

    iterable : iterable
               container of values

    indices : pandas.Float64Index
              The index to access

    Returns
    -------

    : list
      list of subindices within range

    """
    subindices = []
    for x in iterable:
        subindices.extend(_get_subindices(x, indices, tolerance=tolerance))
    return subindices


@dispatch(slice, pd.Float64Index)
def _get_subindices(s, indices, tolerance=0):
    """
    Returns every index within the range [scalar +/- tolerance] from a iterable of
    values.

    >>> l = [2, 9]
    >>> indices = pd.Float64Index([2.3, 3.55, 6.23, 9.99])
    >>> _get_subindices(l, indices, tolerance=.5)
    [2.3, 9.99]

    Parameters
    ----------

    iterable : iterable
               container of values

    indices : pandas.Float64Index
              The index to access

    Returns
    -------

    : list
      list of subindices within range

    """
    start = s.start
    stop = s.stop

    if start is None:
        start = -np.inf

    if stop is None:
        stop = np.inf

    subindices = indices.where((indices >= start) & (indices <= stop)).dropna().astype(float)

    if subindices.size == 0:
        raise KeyError('{} is not in range'.format(s))

    return subindices


@dispatch(object, pd.Index)
def _get_subindices(o, indices, tolerance=0):
    """
    Default function, returns the original input. This is just bookeeping
    for trying to use _get_subindices for indices that are not floating
    point indices.


    Parameters
    ----------

    o : object
               any python object

    indices : pandas.Index
              any pandas index

    Returns
    -------

    : object
      just returns o

    """
    return o


@dispatch((pd.Series, list, set, slice, np.ndarray, Real), tuple)
def _get_subindices(key, indexes, tolerance=0):
    """
    Returns


    Parameters
    ----------

    o : object
               any python object

    indices : pandas.Index
              any pandas index

    Returns
    -------

    : object
      just returns o

    """
    return _get_subindices(key, indexes[0], tolerance=tolerance)


@dispatch(tuple, tuple)
def _get_subindices(keys, indexes, tolerance=0):
    """
    Unpacks a tuple of keys and and tuple of indices. Matches the indices with
    keys and dispatches to the other _get_subindices.


    Parameters
    ----------

    keys : tuple
           a tuple of keys

    indices : tuple
              a tuple of indices

    Returns
    -------

    : tuple
      tuple of resulting indices

    """

    num_keys = len(keys)
    num_indexes = len(indexes)
    if num_keys > num_indexes:
        raise KeyError('{} keys for {}-dimensional keyspace'.format(num_keys, num_indexes))

    dim = max(num_keys, num_indexes)
    keys = keys[:dim]
    indexes = indexes[:dim]

    subindexes = tuple([_get_subindices(key, index, tolerance=tolerance) for key, index in zip(keys, indexes)])

    return subindexes


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
                # if isinstance(columns, pd.Index):
                #     columns = columns.union(self.obj.metadata)

                subindices = tuple([tuple([x[0], y[0]]), columns])

            else:
                x = self.obj.index
                indexes = x,columns
                subindices = _get_subindices(key, indexes, tolerance=self._tolerance)

                x = subindices[0:1] if subindices[0:1] else tuple([slice(None, None)])
                columns = subindices[1:2] if subindices[1:2] else tuple([slice(None, None)])

                columns = columns[0]
                # if isinstance(columns, pd.Index):
                #     columns = columns.union(self.obj.metadata)

                subindices = tuple([x[0], columns])


            subframe = super(SpectrumLocIndexer, self).__getitem__(subindices)

        except Exception as e:
            subframe = super(SpectrumLocIndexer, self).__getitem__(key)

        if isinstance(subframe, sp.Spectrum):
            subframe.wavelengths = self.obj.wavelengths
            subframe.metadata = self.obj.metadata
        else:
            subframe = sp.Spectra(subframe, wavelengths=self.obj.wavelengths, tolerance=self.tolerance)

        return subframe


class SpectrumiLocIndexer(pd.core.indexing._iLocIndexer):
    """
    """

    def __getitem__(self, key):
        subframe = super(SpectrumiLocIndexer, self).__getitem__(key)

        if isinstance(subframe, sp.Spectrum):
            subframe.wavelengths = self.obj.wavelengths
            subframe.metadata = self.obj.metadata
        else:
            subframe = sp.Spectra(subframe, wavelengths=self.obj.wavelengths, tolerance = self.obj._get.tolerance)
        return subframe

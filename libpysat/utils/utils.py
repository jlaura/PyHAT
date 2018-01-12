from functools import reduce
from functools import singledispatch
from functools import update_wrapper

import numpy as np
import pandas as pd
import scipy.stats as ss


def method_singledispatch(func):
    """
    New dispatch decorator that looks at the second argument to
    avoid self
    Parameters
    ----------
    func : Object
        Function object to be dispatched
    Returns
    wrapper : Object
        Wrapped function call chosen by the dispatcher
    ----------
    """
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, dispatcher)
    return wrapper


def crossform(a):
    """
    Return the cross form, e.g. a in the cross product of a b.
    Parameters
    ----------
    a : ndarray
        (3,) vector

    Returns
    -------
    a : ndarray
        (3,3)
    """
    return np.array([[0, -a[2], a[1]],
                     [a[2], 0, -a[0]],
                     [-a[1], a[0], 0]])


def normalize_vector(line):
    """
    Normalize a standard form line

    Parameters
    ----------
    line : ndarray
           Standard form of a line (Ax + By + C = 0)

    Returns
    -------
    line : ndarray
           The normalized line

    Examples
    --------
    >>> x = np.random.random((3,3))
    >>> normalize_vector(x)
    array([[ 0.88280225,  0.4697448 ,  0.11460811],
       [ 0.26090555,  0.96536433,  0.91648305],
       [ 0.58271501,  0.81267657,  0.30796395]])
    """
    if isinstance(line, pd.DataFrame):
        line = line.values
    try:
        n = np.sqrt(line[:, 0] ** 2 + line[:, 1] ** 2).reshape(-1, 1)
    except:
        n = np.sqrt(line[0] ** 2 + line[1] ** 2)
    line = line / n
    return line


def getnearest(iterable, value):
    """
    Given an iterable, get the index nearest to the input value

    Parameters
    ----------
    iterable : iterable
               An iterable to search

    value : int, float
            The value to search for

    Returns
    -------
        : int
          The index into the list
    """
    return min(enumerate(iterable), key=lambda i: abs(i[1] - value))


def checkbandnumbers(bands, checkbands):
    """
    Given a list of input bands, check that the passed
    tuple contains those bands.

    In case of THEMIS, we check for band 9 as band 9 is the temperature
    band required to derive thermal temperature.  We also check for band 10
    which is required for TES atmosphere calculations.

    Parameters
    ----------
    bands : tuple
            of bands in the input image
    checkbands : list
                 of bands to check against

    Returns
    -------
     : bool
       True if the bands are present, else False
    """
    for c in checkbands:
        if c not in bands:
            return False
    return True


def checkdeplaid(incidence):
    """
    Given an incidence angle, select the appropriate deplaid method.

    Parameters
    ----------
    incidence : float
                incidence angle extracted from the campt results.

    """
    if incidence >= 95 and incidence <= 180:
        return 'night'
    elif incidence >= 90 and incidence < 95:
        return 'night'
    elif incidence >= 85 and incidence < 90:
        return 'day'
    elif incidence >= 0 and incidence < 85:
        return 'day'
    else:
        return False


def checkmonotonic(iterable, piecewise=False):
    """
    Check if a given iterable is monotonically increasing.

    Parameters
    ----------
    iterable : iterable
                Any Python iterable object

    piecewise : boolean
                If false, return a boolean for the entire iterable,
                else return a list with elementwise monotinicy checks

    Returns
    -------
    monotonic : bool/list
                A boolean list of all True if monotonic, or including
                an inflection point
    """
    monotonic = [True] + [x < y for x, y in zip(iterable, iterable[1:])]
    if piecewise is True:
        return monotonic
    else:
        return all(monotonic)


def find_in_dict(obj, key):
    """
    Recursively find an entry in a dictionary

    Parameters
    ----------
    obj : dict
          The dictionary to search
    key : str
          The key to find in the dictionary

    Returns
    -------
    item : obj
           The value from the dictionary
    """
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = find_in_dict(v, key)
            if item is not None:
                return item


def find_nested_in_dict(data, key_list):
    """
    Traverse a list of keys into a dict.

    Parameters
    ----------
    data : dict
           The dictionary to be traversed
    key_list: list
              The list of keys to be travered.  Keys are
              traversed in the order they are entered in
              the list

    Returns
    -------
    value : object
            The value in the dict
    """
    return reduce(lambda d, k: d[k], key_list, data)


def make_homogeneous(points):
    """
    Convert a set of points (n x dim array) to
        homogeneous coordinates.

    Parameters
    ----------
    points : ndarray
             n x m array of points, where n is the number
             of points.

    Returns
    -------
     : ndarray
       n x m + 1 array of homogeneous points
    """
    return np.hstack((points, np.ones((points.shape[0], 1))))


def remove_field_name(a, name):
    """
    Given a numpy structured array, remove a column and return
    a copy of the remainder of the array

    Parameters
    ----------
    a : ndarray
        Numpy structured array

    name : str
           of the index (column) to be removed

    Returns
    -------
    b : ndarray
        Numpy structured array with the 'name' column removed
    """
    names = list(a.dtype.names)
    if name in names:
        names.remove(name)
    b = a[names]
    return b

def linear(data, wv_array, axis=0):
    """
    perform linear continuum correction on a ndarray

    parameters
    ----------

    data : ndarray
           The array to continuum correct

    wv_array : ndarray
               array of wavelengths parallel to the wavelengths axis

    axis : int
           The array axis along which the wavelengths exist
    """
    y1 = np.take(data, 0, axis=axis)
    y2 = np.take(data, -1, axis=axis)
    wv1 = wv_array[0]
    wv2 = wv_array[-1]
    m = (y2 - y1) / (wv2 - wv1)
    b = y1 - (m * wv1)

    new_wv_shape = [wv_array.size] + [s for s in m.shape]
    wv_array = np.repeat(wv_array, m.size).reshape(new_wv_shape)

    y = m * wv_array
    y += b

    # reshape the array back to normal
    # TODO: make this less ugly
    for i in range(data.ndim-1):
        y = np.swapaxes(y, i, i+1)
    return y

def regression(data, wv_array):
    m,b,_,_,_ =  ss.linregress(wv_array, data)
    regressed_continuum = m * wv_array + b
    return  data / regressed_continuum

def horgan(data, wv_array, points, window):
    #Define the search windows
    windows = np.empty(len(points), dtype=list)
    for i, point in enumerate(points):
        windows[i] = ((np.where((wv_array > point - window) & (wv_array < point + window))[0]))

    #Get the maximum within the window
    maxima = np.empty(len(points), dtype = int)
    for i, t_window in enumerate(windows):
        maxima[i] = data[t_window.argmax() + t_window[0]]

    x = np.asarray([wv_array[i-1] for i in maxima])
    y = np.asarray([data[i-1] for i in maxima])

    fit = np.polyfit(x,y,2)
    continuum = np.polyval(fit,wv_array)
    continuum_corrected =  data / continuum

    return continuum_corrected

def continuum_correction(data, wv, nodes, correction_nodes=np.array([]), correction=linear, axis=0, **kwargs):
    if not correction_nodes:
        correction_nodes = nodes

    correction_idx = []
    for start, stop in zip(correction_nodes, correction_nodes[1:]):
        start = np.where(np.isclose(wv, [start], atol=1))[0][0]
        stop = np.where(np.isclose(wv, [stop], atol=1))[0][0]+1 # +1 as slices are exclusive
        correction_idx.append((start, stop))

    # Make a copy of the input data that will house the corrected spectra
    corrected = np.copy(data)
    denom = np.zeros(data.shape)

    for i, (start, stop) in enumerate(zip(nodes, nodes[1:])):
        # Get the start and stop indices into the wavelength array. These define the correction nodes
        start_idx = np.where(np.isclose(wv, [start], atol=1))[0][0]
        stop_idx = np.where(np.isclose(wv, [stop], atol=1))[0][0]+1 # +1 as slices are exclusive
        # Grab the correction indices.  These define the length of the line to be corrected
        cor_idx = correction_idx[i]

        print(start_idx, stop_idx)

        nodeidx = [slice(None, None)]*len(data.shape)
        nodeidx[axis] = slice(start_idx,stop_idx)
        corridx = [slice(None, None)]*len(data.shape)
        corridx[axis] = slice(cor_idx[0],cor_idx[1])

        print(data[tuple(nodeidx)].shape)
        print(wv[cor_idx[0]:cor_idx[1]].shape)

        # Compute an arbitrary correction
        y = correction(data[tuple(nodeidx)], wv[cor_idx[0]:cor_idx[1]], axis=axis, **kwargs)

        # Apply the correction to a copy of the input data and then step to the next subset
        vals = data[tuple(corridx)] / y
        corrected[tuple(corridx)] = vals
        denom[tuple(corridx)] = y
    return corrected, denom

def generic_func(data, wv_array, wavelengths, func = None):
    """
    Using some form of data and a wavelength array. Get the bands associated
    wtih each wavelength in wavelengths, create a subset of bands based off
    of those wavelengths then hand the subset to the function.

    Parameters
    ----------
    data : ndarray
           (x, y, z) 3 dimensional numpy array of a spectra image

    wv_array : iterable
               A list of all possible wavelengths for a given spectral image

    wavelengths : iterable
                  List of wavelengths to use for the function

    Returns
    ----------
    : func
      Returns the result from the given function
    """
    bands = getbandnumbers(wv_array, wavelengths)
    subset = data.take(bands, axis = 0)
    return func(subset, wavelengths)

def getbandnumbers(wavelengths, wave_values):
    '''
    This parses the wavelenth list,finds the mean wavelength closest to the
    provided wavelength, and returns the index of that value.  One (1) is added
    to the index to grab the correct band.

    Parameters
    ----------
    wavelengths: A list of wavelengths, 0 based indexing
    *args: A variable number of input wavelengths to map to bands

    Returns
    -------
    bands: A variable length list of bands.  These are in the same order they are
    provided in.  Beware that altering the order will cause unexpected results.

    '''
    bands = []
    for x in wave_values:
        bands.append(min(range(len(wavelengths)), key=lambda i: abs(wavelengths[i]-x)))
    return bands

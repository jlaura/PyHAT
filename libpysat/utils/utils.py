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


def linear_correction(bands, ref_array, wv_array):
    """
    Perform a linear continuum correction.

    Parameters
    ----------
        bands     : tuple(int)
            Index of bands used to perform the continuum correction.

        ref_array : array(float)
            The reference array on which we will perform the continuum
            correction.

        wv_array  : array(float):
            The array of wavelengths used to calculate the continuum correction.

    Returns
    -------
        corrected : array(float)
            The continuum corrected ref array.

        y         : int
            Continuum slope  @@TODO Check with J to make sure this is the correct description
    """
    try:
        y1 = ref_array[bands[0]]
        y2 = ref_array[bands[1]]
        wv1 = wv_array[bands[0]]
        wv2 = wv_array[bands[1]]

        m = (y2-y1) / (wv2 - wv1)
        b = y1 - (m * wv1)
        y = (m * wv_array) + b
        corrected = ref_array / y
    except ZeroDivisionError:
        return 0,0


    return corrected, y

def horgan_correction(reflectance, wavelength, a, b, c, window):
    #Define the search windows
    lowerwindow = np.where((wavelength > a - window) & (wavelength < a + window))[0]
    middlewindow = np.where((wavelength > b - window) & (wavelength < b + window))[0]
    upperwindow = np.where((wavelength > c - window) & (wavelength < c + window))[0]
    #Get the maximum within the window
    maxa = reflectance[lowerwindow].argmax() + lowerwindow[0]
    maxb = reflectance[middlewindow].argmax() + middlewindow[0]
    maxc = reflectance[upperwindow].argmax() + upperwindow[0]
    itercounter = 0
    iterating = True
    # @@TODO ask about this code.  Why loop if there's an unconditional
    #  flag that breaks the loop after the first iteration?
    while iterating:
        x = np.asarray([wavelength[maxa],wavelength[maxb], wavelength[maxc]])
        y = np.asarray([reflectance[maxa],reflectance[maxb], reflectance[maxc]])
        fit = np.polyfit(x,y,2)
        continuum = np.polyval(fit, wavelength)
        continuum_corrected = reflectance / continuum
        iterating = False
        if itercounter == 9:
            print('Unable to converge')
            break
        itercounter += 1

    return continuum_corrected, continuum

def regression_correction(wavelengths,reflectance):
    m,b,_,_,_ =  ss.linregress(wavelengths, reflectance)
    regressed_continuum = m * wavelengths + b
    return reflectance / regressed_continuum, regressed_continuum


def linear_correct_all(self, bands):
    """
    Convenience function used to perform continuum correction on all
    observations in Spectrum or HCube objects.

    Parameters
    ----------
        bands : tuple(int)
            Index of bands used to perform the continuum correction.

    Returns
    -------
        self.data : numpy array(float)
            A numpy array containing continuum corrected values.

        y : array(int)
            An array containing continuum slopes.

    Note
    ----
        Use with caution - this function mutates the object's "data" field.

    """
    y = np.empty(self.data.shape)
    for obs_id in range(len(self.data)):
        self.data[obs_id], y[obs_id] = linear_correction(bands,
                                                         self.data[obs_id],
                                                         self.wavelengths)
    return self.data, y


def horgan_correct_all(self, a,b,c, window):
    """
    Convenience function used to perform continuum correction on all
    observations in Spectrum or HCube objects.

    Parameters
    ----------
        bands : tuple(int)
            Index of bands used to perform the continuum correction.

    Returns
    -------
        self.data : numpy array(float)
            A numpy array containing continuum corrected values.

        y : array(int)
            An array containing continuum slopes.

    Note
    ----
        Use with caution - this function mutates the object's "data" field.

    """
    y = np.empty(self.data.shape)
    for obs_id in range(len(self.data)):
        self.data[obs_id], y[obs_id] = horgan_correction(self.data[obs_id],
                                                         self.wavelengths,
                                                         a,
                                                         b,
                                                         c,
                                                         window)
    return self.data, y


def regression_correct_all(self):
    """
    Convenience function used to perform continuum correction on all
    observations in Spectrum or HCube objects.

    Parameters
    ----------
        bands : tuple(int)
            Index of bands used to perform the continuum correction.

    Returns
    -------
        self.data : numpy array(float)
            A numpy array containing continuum corrected values.

        y : array(int)
            An array containing continuum slopes.

    Note
    ----
        Use with caution - this function mutates the object's "data" field.

    """
    y = np.empty(self.data.shape)
    for obs_id in range(len(self.data)):
        self.data[obs_id], y[obs_id] = regression_correction(self.data[obs_id],
                                                             self.wavelengths)
    return self.data, y

def generic(data, wv_array, wavelengths, func = None):
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
    subset = [data[:, :, i] for i in bands]
    return func(subset)

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

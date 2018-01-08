from libpysat.utils.utils import generic, getbandnumbers
from libpysat.m3 import supplemental_funcs as sp_funcs

def curvature(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [730, 749, 909, 1109, 1129]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.curv_func)

def fe_est(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [730, 749, 949, 970]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.fe_est_func)

def fe_mare_est(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [730, 749, 949, 970]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.fe_mare_est_func)

def luceyc_amat(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [730, 749, 949, 970]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.luceyc_amat_func)

def luceyc_omat(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [730, 749, 949, 970]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.luceyc_omat_func)

def mare_omat(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [730, 749, 949, 970]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.mare_omat_func)

def tilt(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [909, 930, 1009, 1029]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.tilt_func)

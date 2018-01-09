from libpysat.utils.utils import generic, getbandnumbers
from libpysat.derived.m3 import supplemental_funcs as sp_funcs

#TODO: The continuum in these funcs should default to linear

def curvature(data, wv_array, continuum = None, continuum_args = ()):
    '''
    Name: Curvature
    Parameter:1 um Band Curvature
    Formulation: (R749 + R1109) / (2* R909)
    Rationale: Tompkins and Pieters
    Bands: 749, R909, R1109

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    continuum : callable
                to perform a continuum correction

    continuum_args : tuple
                     of arguments to be passed to the continuum callable

    Returns
    -------
     : ndarray
       the processed ndarray
    '''
    wavelengths = [730, 749, 909, 1109, 1129]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.curv_func)

def fe_est(data, wv_array, continuum = None, continuum_args = ()):
    '''
    Name: FE_est
    Parameter:Iron Estimate
    Formulation:
        y0 = 1.19
        x0 = 0.08
        FE_est = (17.427*(-1*(math.atan(((R949/R749)-y0)/(R749 - x0))))) - 7.565
    Rationale: Iron estimate based on Lucey's Work
    Bands: R749, R949

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    continuum : callable
                to perform a continuum correction

    continuum_args : tuple
                     of arguments to be passed to the continuum callable

    Returns
    -------
     : ndarray
       the processed ndarray
    '''
    wavelengths = [730, 749, 949, 970]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.fe_est_func)

def fe_mare_est(data, wv_array, continuum = None, continuum_args = ()):
    '''
    Name: FE_est_mare
    Parameter:Iron Estimate Mare
    Formulation: -137.97 * ((R749 * 0.9834)+((R949 / R749)*0.1813)) + 57.46
    Rationale: Wilcox et al. JGR (2005), Clementine based
    Bands: R749, R949

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    continuum : callable
                to perform a continuum correction

    continuum_args : tuple
                     of arguments to be passed to the continuum callable

    Returns
    -------
     : ndarray
       the processed ndarray
    '''
    wavelengths = [730, 749, 949, 970]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.fe_mare_est_func)

def luceyc_amat(data, wv_array, continuum = None, continuum_args = ()):
    '''
    Name: Lucey_OMAT
    Parameter:Optimal Maturity - clementine Legacy; Using Adams Constants
    Formulation: (((R749-0.01)**2)+((R949/R749)-1.26)**2)**(1/2)
    Rationale: Based on Lucey et al., JGR (2000)
    Bands: R749, R949

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    continuum : callable
                to perform a continuum correction

    continuum_args : tuple
                     of arguments to be passed to the continuum callable

    Returns
    -------
     : ndarray
       the processed ndarray
    '''
    wavelengths = [730, 749, 949, 970]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.luceyc_amat_func)

def luceyc_omat(data, wv_array, continuum = None, continuum_args = ()):
    '''
    Name: Lucey_OMAT
    Parameter:Optimal Maturity - clementine Legacy; Using Clementine Constants
    Formulation: (((R749-0.08)**2)+((R949/R749)-1.19)**2)**(1/2)
    Rationale: Based on Lucey et al., JGR (2000)
    Bands: R749, R949

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    continuum : callable
                to perform a continuum correction

    continuum_args : tuple
                     of arguments to be passed to the continuum callable

    Returns
    -------
     : ndarray
       the processed ndarray
    '''
    wavelengths = [730, 749, 949, 970]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.luceyc_omat_func)

def mare_omat(data, wv_array, continuum = None, continuum_args = ()):
    '''
    Name: Mare_OMAT
    Parameter:Optical maturity Highlands
    Formulation: (R749 * 0.1813) - ((R949/R749)*0.9834)
    Rationale: Based on Wilcox et al. 2005 - untested
    Bands: R749, R949

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    continuum : callable
                to perform a continuum correction

    continuum_args : tuple
                     of arguments to be passed to the continuum callable

    Returns
    -------
     : ndarray
       the processed ndarray
    '''
    wavelengths = [730, 749, 949, 970]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.mare_omat_func)

def tilt(data, wv_array, continuum = None, continuum_args = ()):
    '''
    Name: Tilt
    Parameter: 1um tilt
    Formulation: R909 - R1009
    Rationale: Tompkins and Pieters

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    continuum : callable
                to perform a continuum correction

    continuum_args : tuple
                     of arguments to be passed to the continuum callable

    Returns
    -------
     : ndarray
       the processed ndarray
    '''
    wavelengths = [909, 930, 1009, 1029]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic(data, wv_array, wavelengths, func = sp_funcs.tilt_func)

from libpysat.derived.m3 import development_funcs as dv_funcs
from libpysat.utils.utils import generic_func

def bd1umratio(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [660 ,699, 929, 989, 1579, 1618]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic_func(data, wv_array, wavelengths, func = dv_funcs.bd1umratio_func)

def h2o2(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [1329, 1348, 1408, 1428, 1448, 1578, 1618]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic_func(data, wv_array, wavelengths, func = dv_funcs.h2o2_func)

def h2o3(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [1408, 1428, 1448, 1488, 1508, 1528, 1548]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic_func(data, wv_array, wavelengths, func = dv_funcs.h2o3_func)

def h2o4(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [2177, 2218, 2258, 2378, 2418, 2298, 2338, 2377]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic_func(data, wv_array, wavelengths, func = dv_funcs.h2o4_func)

def h2o5(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [2537, 2578, 2618, 2658, 2698, 2738, 2776]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic_func(data, wv_array, wavelengths, func = dv_funcs.h2o5_func)

def ice(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [2497, 2538, 2578, 2618, 2817, 2857, 2897, 2936]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic_func(data, wv_array, wavelengths, func = dv_funcs.ice_func)

def bd2umratio(data, wv_array, continuum = None, continuum_args = ()):
    wavelengths = [1548, 1578, 1898, 2298, 2578, 2616]
    if continuum:
        continuum(data, wavelengths, continuum, continuum_args)
    return generic_func(data, wv_array, wavelengths, func = dv_funcs.bd2umratio_func)

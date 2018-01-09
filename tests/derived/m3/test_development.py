import pytest
import numpy as np

from libpysat.derived.m3 import development as dev

@pytest.fixture
def test_params(wavelengths):
    return (np.array(wavelengths), None, 1)

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([730, 749, 909, 1109, 1129])])

def test_bd1umratio(six_dim, wv_array, continuum, expected):
    res = dev.bd1umratio(six_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([1329, 1348, 1408, 1428, 1448, 1578, 1618])])

def test_h2o2(seven_dim, wv_array, continuum, expected):
    res = dev.h2o2(seven_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [(np.array([1408, 1428, 1448, 1488, 1508, 1528, 1548]), None, 0)])

def test_h2o3(seven_dim, wv_array, continuum, expected):
    res = dev.h2o3(seven_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([2177, 2218, 2258, 2378, 2418, 2298, 2338, 2377])])

def test_h2o4(eight_dim, wv_array, continuum, expected):
    res = dev.h2o4(eight_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([2537, 2578, 2618, 2658, 2698, 2738, 2776])])

def test_h2o5(seven_dim, wv_array, continuum, expected):
    res = dev.h2o5(seven_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([2497, 2538, 2578, 2618, 2817, 2857, 2897, 2936])])

def test_ice(eight_dim, wv_array, continuum, expected):
    res = dev.ice(eight_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([1548, 1578, 1898, 2298, 2578, 2616])])

def test_bd2umratio(six_dim, wv_array, continuum, expected):
    res = dev.bd2umratio(six_dim, wv_array, continuum)
    assert res.all() == expected

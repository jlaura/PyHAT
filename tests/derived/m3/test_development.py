import pytest
import numpy as np

from libpysat.derived.m3 import development as dev

# TODO: Change the default of continuum to linear
@pytest.fixture
def test_params(wavelengths, continuum = None):
    return (np.array(wavelengths), continuum, 1)

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([699, 929, 989, 1579])])

def test_bd1umratio(four_dim, wv_array, continuum, expected):
    res = dev.bd1umratio(four_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([1348, 1408, 1428, 1448, 1578])])

def test_h2o2(five_dim, wv_array, continuum, expected):
    res = dev.h2o2(five_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [(np.array([1428, 1448, 1488, 1508, 1528]), None, 0)])

def test_h2o3(five_dim, wv_array, continuum, expected):
    res = dev.h2o3(five_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([2218, 2258, 2378, 2418, 2298, 2338])])

def test_h2o4(six_dim, wv_array, continuum, expected):
    res = dev.h2o4(six_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([2578, 2618, 2658, 2698, 2738])])

def test_h2o5(five_dim, wv_array, continuum, expected):
    res = dev.h2o5(five_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([2538, 2578, 2618, 2817, 2857, 2897])])

def test_ice(six_dim, wv_array, continuum, expected):
    res = dev.ice(six_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([1578, 1898, 2298, 2578])])

def test_bd2umratio(four_dim, wv_array, continuum, expected):
    res = dev.bd2umratio(four_dim, wv_array, continuum)
    assert res.all() == expected

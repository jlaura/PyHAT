import pytest
import numpy as np

from libpysat.derived.m3 import supplemental as sup

# TODO: Change the default of continuum to linear
@pytest.fixture
def test_params(wavelengths, continuum = None):
    return (np.array(wavelengths), continuum, 1)

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([749, 909, 1109])])

def test_curvature(three_dim, wv_array, continuum, expected):
    res = sup.curvature(three_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([749, 949])])

def test_fe_est(two_dim, wv_array, continuum, expected):
    res = sup.fe_est(two_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([749, 949])])

def test_fe_mare_est(two_dim, wv_array, continuum, expected):
    res = sup.fe_mare_est(two_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([749, 949])])

def test_luceyc_amat(two_dim, wv_array, continuum, expected):
    res = sup.luceyc_amat(two_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([749, 949])])

def test_luceyc_omat(two_dim, wv_array, continuum, expected):
    res = sup.luceyc_omat(two_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([749, 949])])

def test_mare_omat(two_dim, wv_array, continuum, expected):
    res = sup.mare_omat(two_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([930, 1009])])

def test_tilt(two_dim, wv_array, continuum, expected):
    res = sup.tilt(two_dim, wv_array, continuum)
    assert res.all() == expected

import pytest
import numpy as np

from libpysat.derived.m3 import supplemental as sup

@pytest.fixture
def test_params(wavelengths):
    return (np.array(wavelengths), None, 1)

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([730, 749, 909, 1109, 1129])])

def test_curvature(five_dim, wv_array, continuum, expected):
    res = sup.curvature(five_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([730, 749, 949, 970])])

def test_fe_est(four_dim, wv_array, continuum, expected):
    res = sup.fe_est(four_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([730, 749, 949, 970])])

def test_fe_mare_est(four_dim, wv_array, continuum, expected):
    res = sup.fe_mare_est(four_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([730, 749, 949, 970])])

def test_luceyc_amat(four_dim, wv_array, continuum, expected):
    res = sup.luceyc_amat(four_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([730, 749, 949, 970])])

def test_luceyc_omat(four_dim, wv_array, continuum, expected):
    res = sup.luceyc_omat(four_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([730, 749, 949, 970])])

def test_mare_omat(four_dim, wv_array, continuum, expected):
    res = sup.mare_omat(four_dim, wv_array, continuum)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, continuum, expected',
                          [test_params([909, 930, 1009, 1029])])

def test_tilt(four_dim, wv_array, continuum, expected):
    res = sup.tilt(four_dim, wv_array, continuum)
    assert res.all() == expected

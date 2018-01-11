import pytest
import numpy as np

from libpysat.derived.m3 import supplemental as sup
from libpysat.spectral.spectra import Spectra

# TODO: Change the default of continuum to linear
@pytest.fixture
def test_params(wavelengths):
    return (np.array(wavelengths), 1)

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 909, 1109])])

def test_curvature(three_dim, wv_array, expected):
    res = sup.curvature(Spectra(three_dim, wv_array, waxis = 0), wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 949])])

def test_fe_est(two_dim, wv_array, expected):
    res = sup.fe_est(Spectra(two_dim, wv_array, waxis = 0), wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 949])])

def test_fe_mare_est(two_dim, wv_array, expected):
    res = sup.fe_mare_est(Spectra(two_dim, wv_array, waxis = 0), wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 949])])

def test_luceyc_amat(two_dim, wv_array, expected):
    res = sup.luceyc_amat(Spectra(two_dim, wv_array, waxis = 0), wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 949])])

def test_luceyc_omat(two_dim, wv_array, expected):
    res = sup.luceyc_omat(Spectra(two_dim, wv_array, waxis = 0), wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([749, 949])])

def test_mare_omat(two_dim, wv_array, expected):
    res = sup.mare_omat(Spectra(two_dim, wv_array, waxis = 0), wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                          [test_params([930, 1009])])

def test_tilt(two_dim, wv_array, expected):
    res = sup.tilt(Spectra(two_dim, wv_array, waxis = 0), wv_array)
    assert res.all() == expected

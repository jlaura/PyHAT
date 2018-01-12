import pytest
import numpy as np

from libpysat.derived.crism import crism
from libpysat.spectral.spectra import Spectra

@pytest.fixture
def test_params(wavelengths):
    return(np.array(wavelengths, 1))

@pytest.mark.parametrize('wv_array, expected',
                         [test_params([770])])

def test_rockdust1(one_dim, wv_array, expected):
    data = Spectra(one_dim, wv_array, waxis = 0)
    res = crism.rockdust1(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array, expected',
                         [test_params([440,770])])

def test_rockdust2(two_dim, wv_array, expected):
    data = Spectra(two_dim, wv_array, waxis = 0)
    res = crism.rockdust2(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                         [test_params([440,530,709])])

def test_bd530(three_dim, wv_array, expected):
    data = Spectra(three_dim, wv_array, waxis = 0)
    res = crism.bd530(data, wv_array)
    assert res.all() == expected

@pytest.mark.parametrize('wv_array, expected',
                         [test_params([533,600,710])])

def test_sh600(three_dim, wv_array, expected):
    data = Spectra(three_dim, wv_array, waxis = 0)
    res = crism.sh600(data, wv_array)
    assert res.all() == expected


@pytest.mark.parametrize('wv_array, expected',
                         [test_params([600,648,709])])

def test_bd640(three_dim, wv_array, expected):
    data = Spectra(three_dim, wv_array, waxis = 0)
    res = crism.bd640(data, wv_array)
    assert res.all() == expected

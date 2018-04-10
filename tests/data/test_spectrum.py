import numpy as np
from pandas import Index
import pytest

from libpysat import Spectrum

@pytest.fixture
def basic_spectrum():
    return Spectrum([1,2,3,4],
                    index=[2.2, 3.3, 4.4, 5.5],
                    wavelengths=[2.2, 3.3, 4.4, 5.5])

@pytest.fixture
def metadata_spectrum():
    return Spectrum([1,2,3,4, 'a', 'b', 'c'],
                    index=[2.2, 3.3, 4.4, 5.5, 'foo', 'bar', 'bat'],
                    wavelengths=[2.2, 3.3, 4.4, 5.5],
                    metadata=['foo', 'bar', 'bat'])

@pytest.fixture
def floatwv_spectrum():
    return Spectrum([1,2,3], 
                    index=[1.10001, 2.222222, 3.33300015],
                    wavelengths=[1.10001, 2.222222, 3.33300015])

@pytest.fixture
def floatwv_metadata_spectrum():
    return Spectrum([1,2,3, 'a', 'b', 'c'], 
                    index=[1.10001, 2.222222, 3.33300015, 'foo', 'bar', 'bat'],
                    wavelengths=[1.10001, 2.222222, 3.33300015],
                    metadata=['foo', 'bar', 'bat'])

def test_slice_return_spectrum(basic_spectrum):
    assert isinstance(basic_spectrum[1:2], Spectrum)

def test_get_data_type(metadata_spectrum):
    assert isinstance(metadata_spectrum.data, Spectrum)

def test_get_data(metadata_spectrum, basic_spectrum):
    assert metadata_spectrum.data.equals(basic_spectrum)
    
def test_get_metadata_type(metadata_spectrum):
    assert isinstance(metadata_spectrum, Spectrum)

def test_get_metadata(metadata_spectrum):
    assert metadata_spectrum.metadata.equals(Spectrum(['a', 'b', 'c'],
                                                   index=['foo', 'bar', 'bat']))

def test_get_metadata_slice(metadata_spectrum):
    assert metadata_spectrum[1:].metadata.equals(Spectrum(['a', 'b', 'c'],
                                                   index=['foo', 'bar', 'bat']))

def test_get_metadata_slice_type(metadata_spectrum):
    assert isinstance(metadata_spectrum[1:].metadata, Spectrum)

def test_unary_operation(basic_spectrum):
    basic_spectrum[2.2] += 1
    assert isinstance(basic_spectrum, Spectrum)
    assert basic_spectrum[2.2] == 2
    
    basic_spectrum[2.2] -= 1
    basic_spectrum += 1
    assert isinstance(basic_spectrum, Spectrum)
    assert basic_spectrum.equals(Spectrum([2, 3,4,5],
                    index=[2.2, 3.3, 4.4, 5.5],
                    wavelengths=[2.2, 3.3, 4.4, 5.5]))

def test_approximate_indexer(basic_spectrum):
    assert basic_spectrum.iloc[basic_spectrum.index.get_loc(2.1, tolerance=0.11, method='nearest')] == 1

@pytest.mark.parametrize("spectrum, tolerance, expected",
                        [(floatwv_spectrum(), 5, Index([1.10001, 2.22222, 3.33300])),
                         (floatwv_spectrum(), 1, Index([1.1, 2.2, 3.3])),
                         (floatwv_metadata_spectrum(), 5, Index([1.10001, 2.22222, 3.33300, 'foo', 'bar', 'bat'])),
                         (floatwv_metadata_spectrum(), 1, Index([1.1, 2.2, 3.3, 'foo', 'bar', 'bat']))])
def test_set_tolerance(spectrum, tolerance, expected):
    spectrum.tolerance = tolerance
    assert isinstance(spectrum, Spectrum)
    np.testing.assert_array_equal(spectrum.index, expected)

def test_generic_return(basic_spectrum):
    m = basic_spectrum.take([2, 3])
    assert isinstance(m, Spectrum)
    assert m.equals(Spectrum([3, 4], index=[4.4, 5.5]))

    m = basic_spectrum.sort_index()
    assert isinstance(m, Spectrum)

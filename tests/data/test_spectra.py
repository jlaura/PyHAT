import numpy as np
from pandas import Index, MultiIndex, DataFrame, concat
import pytest

from libpysat import Spectra, Spectrum

@pytest.fixture
def spectra():
    return Spectra(np.arange(16).reshape(4,4),
                   index=[2.22221, 3.33331, 4.400001, 5.500001],
                   wavelengths=[2.22221, 3.33331, 4.400001, 5.500001], 
                   columns=['a', 'b', 'c', 'd'])

@pytest.fixture
def spectra_multiindex():
    multi = [(0, 'a'), (0, 'b'), (1, 'a'), (1, 'b')]
    cols = MultiIndex.from_tuples(multi, names=['observationid', 'wv'])
    return Spectra(np.arange(20).reshape(5,4),
                   index=[2.22221, 3.33331, 4.400001, 5.500001, 6.6],
                   wavelengths=[2.22221, 3.33331, 4.400001, 5.500001, 6.6], 
                   columns=cols)

#@pytest.fixture
#def spectra_multiindex_metadata():

@pytest.fixture
def spectra_metadata():
        return Spectra([[1,2,3,4],
                        [1,2,3,4],
                        [1,2,3,4],
                        [1,2,4,4],
                        ['a', 'a', 'a', 'a'],
                        ['b', 'b', 'b', 'b'],
                        ['c', 'c', 'c', 'c']],
                   index=[2.22221, 3.33331, 4.400001, 5.500001, 'foo', 'bar', 'bat'],
                   wavelengths=[2.22221, 3.33331, 4.400001, 5.500001],
                   metadata=['foo', 'bar', 'bat'] ,
                   columns=['a', 'b', 'c', 'd'])

def test_slicing_types(spectra):
    # As the spectra is sliced, are the proper subclasses returned?
    assert isinstance(spectra['a'], Spectrum)
    assert isinstance(spectra[['a', 'c']], Spectra)
    assert isinstance(spectra.loc[[2.22, 3.33, 5.5]], Spectra)
    assert isinstance(spectra.loc[4.4], Spectrum)

def test_false(spectra_multiindex):
    assert isinstance(spectra_multiindex, Spectra)
    assert isinstance(spectra_multiindex[0], Spectra)
    assert isinstance(spectra_multiindex[(0,'a')], Spectrum)
    
    s = spectra_multiindex.transpose()
    assert isinstance(s, Spectra)
    assert isinstance(s.loc[0], Spectra)
    assert isinstance(s.loc[(0, 'a')], Spectrum)

@pytest.mark.parametrize("spectra",
                         [(spectra_metadata()),
                           (spectra_multiindex())])
def test_get_data_type(spectra):
    assert isinstance(spectra.data, Spectra)
    
@pytest.mark.parametrize("spectra, col",
                         [(spectra_metadata(), 'a'),
                          (spectra_multiindex(), (0,'a'))])
def test_get_data(spectra, col):
    assert 'foo' not in spectra.data.columns
    assert col in spectra.data.columns

     
@pytest.mark.parametrize("spectra, clstype",
                         [(spectra_metadata(), Spectra),
                          (spectra_metadata().metadata.iloc[1:], Spectra),
                          (spectra_metadata().metadata.iloc[0], Spectrum),
                          (spectra_metadata().metadata.loc['foo'], Spectrum)])
def test_get_metadata_type(spectra, clstype):
    assert isinstance(spectra, clstype)

def test_get_metadata(spectra_metadata):
    assert spectra_metadata.metadata.equals(Spectra([['a', 'a', 'a', 'a'],
                                                     ['b', 'b', 'b', 'b'],
                                                     ['c', 'c', 'c', 'c']],
                                                     index=['foo', 'bar', 'bat'],
                                                     columns=['a', 'b', 'c', 'd']))

def test_get_metadata_slice(spectra_metadata):
    assert spectra_metadata.iloc[1:].metadata.equals(Spectra([['a', 'a', 'a', 'a'],
                                                     ['b', 'b', 'b', 'b'],
                                                     ['c', 'c', 'c', 'c']],
                                                     index=['foo', 'bar', 'bat'],
                                                     columns=['a', 'b', 'c', 'd']))
    
    assert spectra_metadata.metadata.iloc[1:].equals(Spectra([['b', 'b', 'b', 'b'],
                                                     ['c', 'c', 'c', 'c']],
                                                     index=['bar', 'bat'],
                                                     columns=['a', 'b', 'c', 'd']))


@pytest.mark.parametrize("spectra, tolerance, expected",
                        [(spectra(), 5, Index([2.22221, 3.33331, 4.4, 5.5])),
                         (spectra(), 1, Index([2.2, 3.3, 4.4, 5.5])),
                         (spectra_multiindex(), 5, Index([2.22221, 3.33331, 4.4, 5.5, 6.6])),
                         (spectra_multiindex(), 1, Index([2.2,  3.3,  4.4,  5.5,  6.6])),
                         (spectra_metadata(), 5, Index([2.22221, 3.33331, 4.4, 5.5, 'foo', 'bar', 'bat'])),
                         (spectra_metadata(), 1, Index([2.2, 3.3, 4.4, 5.5, 'foo', 'bar', 'bat']))])
def test_set_tolerance(spectra, tolerance, expected):
    spectra.tolerance = tolerance
    assert isinstance(spectra, Spectra)
    np.testing.assert_array_equal(spectra.index, expected)
    
def test_merge(spectra):
    s = spectra.merge(spectra)
    assert isinstance(s, Spectra)

def test_concat(spectra):
    s = concat([spectra, spectra])
    assert isinstance(s, Spectra)
    
    s = concat([spectra, DataFrame([['a', 'a', 'a', 'a'],
                                    ['b', 'b', 'b', 'b']], 
                                    index=['foo', 'bar'],
                                    columns=['a', 'b', 'c', 'd'])])
    assert isinstance(s, Spectra)

    # Test that the merge is a left merge - the df first should result in a df
    s = concat([DataFrame([['a', 'a', 'a', 'a'],
                          ['b', 'b', 'b', 'b']], 
                          index=['foo', 'bar'],
                          columns=['a', 'b', 'c', 'd']), spectra])

    assert isinstance(s, DataFrame)

    
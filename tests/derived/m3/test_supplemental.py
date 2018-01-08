import pytest
import numpy as np

from libpysat.derived.m3 import supplemental as sup



@pytest.mark.parametrize('wv_array, continuum, expected',
                          [(np.array([730, 749, 909, 1109, 1129]), None, 1)
                          ])
def test_curvature(five_dim, wv_array, continuum, expected):
    res = sup.curvature(five_dim, wv_array, continuum)
    assert res.all() == expected

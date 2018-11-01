import pytest

import numpy as np
from numpy.testing import assert_array_equal

from libpyhat.analytics import analytics

@pytest.fixture
def setUp():
    np.random.seed(seed=12345)
    return np.random.random(25)

def test_band_minima(setUp):
    minidx, minvalue = analytics.band_minima(setUp)
    print(setUp)
    assert minidx == 12
    assert minvalue == pytest.approx(0.008388297)

@pytest.mark.parametrize("lower_bound, upper_bound, expected_idx, expected_val", [
                                            (0, 7, 2, 0.18391881),
                                            pytest.param(6, 1, 0, 0, marks=pytest.mark.xfail)]
)
def test_band_minima_bounds(lower_bound, upper_bound, expected_idx, expected_val, setUp):
    minidx, minvalue = analytics.band_minima(setUp, lower_bound, upper_bound)
    assert minidx == expected_idx
    assert minvalue == pytest.approx(expected_val)

@pytest.mark.parametrize("spectrum, expected_zero_idx, expected_neg_one_idx, expected_center", [
                                            (setUp(), 0.56293697, 0.42828491, [12]),
                                            (np.ones(24), 1, 1, np.array(range(24)))]
)
def test_band_center(spectrum, expected_zero_idx, expected_neg_one_idx, expected_center):
    center, center_fit = analytics.band_center(spectrum)
    assert center_fit[0] == pytest.approx(expected_zero_idx)
    assert center_fit[-1] == pytest.approx(expected_neg_one_idx)
    assert_array_equal(center[0], expected_center)

def test_band_area():
    x = np.arange(-2, 2, 0.1)
    y = x ** 2
    parabola = y
    area = analytics.band_area(parabola)
    assert area == [370.5]

@pytest.mark.parametrize("spectrum, expected_val", [
                                            (setUp(), 0),
                                            (np.ones(24), 0)]
)
def test_band_asymmetry(spectrum, expected_val):
    assymetry = analytics.band_asymmetry(spectrum)
    assert assymetry == pytest.approx(expected_val)

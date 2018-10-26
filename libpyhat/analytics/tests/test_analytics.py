import unittest

import numpy as np

from libpyhat.analytics import analytics


class Test_Analytics(unittest.TestCase):
    np.random.seed(12345)

    def setUp(self):
        self.arg = np.random.rand(25)

    def test_band_minima(self):
        minidx, minvalue = analytics.band_minima(self.arg)
        self.assertEqual(minidx, 24)
        self.assertAlmostEqual(minvalue, 0.042715304)

        minidx, minvalue = analytics.band_minima(self.arg, 0, 7)
        self.assertEqual(minidx, 0)
        self.assertAlmostEqual(minvalue, 0.225637606)

        with self.assertRaises(ValueError):
            minidx, minvalue = analytics.band_minima(self.arg, 6, 1)

    def test_band_center(self):
        center, center_fit = analytics.band_center(self.arg)
        self.assertEqual(center[0], 6)
        self.assertAlmostEqual(center[1], 0.506357004)
        self.assertAlmostEqual(center_fit[0], 0.5674192848)
        self.assertAlmostEqual(center_fit[12], 0.549810311)
        self.assertAlmostEqual(center_fit[23], 0.598239935)
        self.assertAlmostEqual(center_fit.mean(), 0.55942233)
        self.assertAlmostEqual(np.median(center_fit), 0.56080959)
        self.assertAlmostEqual(center_fit.std(), 0.03824290)

    def test_band_area(self):
        x = np.arange(-2, 2, 0.1)
        y = x ** 2
        parabola = y
        area = analytics.band_area(parabola)
        self.assertEqual(area, [370.5])

    def test_band_asymmetry(self):
        assymetry = analytics.band_asymmetry(self.arg)
        self.assertEqual(assymetry, 1)

        assymetry = analytics.band_asymmetry(self.arg, 0, 10)
        self.assertEqual(assymetry, 0.6)

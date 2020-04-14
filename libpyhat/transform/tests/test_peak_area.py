from libpyhat.transform import peak_area as pa
import numpy as np
import pandas as pd
from libpyhat.examples import get_path
np.random.seed(1)

df = pd.read_csv(get_path('test_data.csv'),header=[0,1])
df = df[df[('meta','LIBS ID')]=='LIB00041']


def test_peak_area():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    df = df[df[('meta', 'LIBS ID')] == 'LIB00041']

    expected_peaks = np.array([586.723, 588.746, 589.42, 590.767, 591.216, 592.114, 592.787, 593.46, 593.909, 594.357])
    expected_mins = np.array(
        [585.374, 587.173, 589.195, 590.543, 590.992, 591.89, 592.338, 593.236, 593.685, 594.133, 594.582])
    expected_areas = np.array(
        [7248.48, 43986.54, 25421.36, 1843.12, 3593.24, 1661.12, 3316.24, 1679.12, 1690.12, 1739.12])
    pa_df = pd.DataFrame(expected_areas).T
    pa_df.columns = pd.MultiIndex.from_tuples([('peak_area', i) for i in expected_peaks])
    df_result, peaks_result, mins_result = pa.peak_area(df, peaks_mins_file=None)
    np.testing.assert_array_almost_equal(np.array(peaks_result,dtype=float), expected_peaks)
    np.testing.assert_array_almost_equal(np.array(mins_result,dtype=float), expected_mins)
    np.testing.assert_array_almost_equal(np.squeeze(np.array(df_result['peak_area'])), expected_areas)

def test_peak_area_from_file():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    df = df[df[('meta', 'LIBS ID')] == 'LIB00041']
    peaks_mins_file = get_path('peaks_mins.csv')
    df_result, peaks_result, mins_result = pa.peak_area(df, peaks_mins_file=peaks_mins_file)
    expected_peaks = [588.072, 592.338]
    expected_mins = [586.273, 589.195, 594.133]
    expected_areas = [47938.78, 39204.32]
    np.testing.assert_array_almost_equal(expected_peaks,peaks_result)
    np.testing.assert_array_almost_equal(expected_mins,mins_result)
    np.testing.assert_array_almost_equal(expected_areas, np.array(df_result['peak_area'])[0,:])

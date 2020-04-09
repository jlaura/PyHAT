import numpy as np
import pandas as pd
from libpyhat.examples import get_path
from libpyhat.transform.remove_baseline import remove_baseline
from libpyhat.transform.baseline_code import airpls, als, dietrich,polyfit, kajfosz_kwiatek, median, fabc, rubberband

def test_min_interp():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'window':10,'kind':'cubic'}

    result, result_baseline = remove_baseline(df,'Min + Interpolate',params=methodParameters)

    expected = [0.00000000e+00, 1.04801898e+03, 1.60660800e+03, 7.45393017e+02, 3.41060513e-13]
    expected_baseline = [1210.06, 504.04102404, 259.45200478, 417.66698313, 920.06]
    np.testing.assert_array_almost_equal(expected,np.array(result['wvl'].iloc[5,0:5]),decimal=4)
    np.testing.assert_array_almost_equal(expected_baseline,np.array(result_baseline['wvl'].iloc[5,0:5]),decimal=4)

    methodParameters = {'window': 1000, 'kind': 'cubic'}

    result, result_baseline = remove_baseline(df, 'Min + Interpolate', params=methodParameters)

    expected = [0.00000000e+00, 1.04801898e+03, 1.60660800e+03, 7.45393017e+02, 3.41060513e-13]
    expected_baseline = [0, 0, 0, 0, 0]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]), decimal=4)
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]), decimal=4)

def test_wavelet_spline():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'level': 6, 'levelmin': 2}

    result, result_baseline = remove_baseline(df, 'Wavelet a Trous + Spline', params=methodParameters)

    expected = [0., 463.585425, 863.017414, 214.440695, 0.]
    expected_baseline = [1210.06, 1088.474575, 1003.042586, 948.619305, 920.06]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))


def test_Rubberband():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'num_iters': 8, 'num_ranges': 4}

    result, result_baseline = remove_baseline(df, 'Rubberband', params=methodParameters)

    expected = [0., 299.089331, 620.12025, -25.907243, -161.993146]
    expected_baseline = [1210.06, 1252.970669, 1245.93975, 1188.967243, 1082.053146]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))

    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'num_iters': 0, 'num_ranges': 4}

    result, result_baseline = remove_baseline(df, 'Rubberband', params=methodParameters)

    expected = [0., 414.5, 801., 170.5, 0.]
    expected_baseline = [1210.06, 1137.56, 1065.06, 992.56, 920.06]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))

    expected_ranges = {'num_ranges_': (1, 100, 'integer'),
                       'num_iters_': (0, 36, 'integer')}
    br_obj = rubberband.Rubberband()
    assert br_obj.param_ranges() == expected_ranges

def test_median():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'window_size': 30}

    result, result_baseline = remove_baseline(df, 'Median', params=methodParameters)

    expected = [290., 567., 848., 134., -171.]
    expected_baseline = [920.06, 985.06, 1018.06, 1029.06, 1091.06]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))

    expected_ranges = {'window_': (201, 901, 'integer')}
    br_obj = median.MedianFilter()
    assert br_obj.param_ranges() == expected_ranges

def test_KK():
    #test case where bottom width is too small
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'top_width': 10, 'bottom_width': 0, 'exponent': 2, 'tangent': False}
    result, result_baseline = remove_baseline(df, 'KK', params=methodParameters)
    assert np.isnan(result['wvl'].iloc[0, 0])

    #test case using top and bottom widths and tangent
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'top_width': 10, 'bottom_width': 50, 'exponent': 2, 'tangent': True}

    result, result_baseline = remove_baseline(df, 'KK', params=methodParameters)
    expected = [-14256.0221, -13917.137851, -13606.003676, -14311.619575, -14556.985549]
    expected_baseline = [15466.0821, 15469.197851, 15472.063676, 15474.679575, 15477.045549]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))

    #test using just bottom width
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'top_width': 0, 'bottom_width': 50, 'exponent': 2, 'tangent': False}

    result, result_baseline = remove_baseline(df, 'KK', params=methodParameters)
    expected = [289.0003, 630.8753, 945.0003, 242.3752, 0.]
    expected_baseline = [921.059702, 921.184664, 921.059702, 920.684814, 920.06]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]),decimal=4)
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))

    expected_ranges = {'top_width_': (0, 100, 'integer'),
                       'bottom_width_': (0, 100, 'integer')}
    br_obj = kajfosz_kwiatek.KajfoszKwiatek()
    assert br_obj.param_ranges() == expected_ranges

def test_FABC():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'dilation_param': 50, 'smoothness_param': 1e3}

    result, result_baseline = remove_baseline(df, 'FABC', params=methodParameters)
    expected = [-1549.471938, -1209.02141, -897.779904, -1604.436177, -1852.696886]
    expected_baseline = [2759.531938, 2761.08141, 2763.839904, 2767.496177, 2772.756886]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))

    expected_ranges = {'dilation_': (1, 100, 'integer'),
                       'smoothness_': (1, 1e6, 'log')}
    br_obj = fabc.FABC()
    assert br_obj.param_ranges() == expected_ranges

def test_Polyfit():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'poly_order': 5, 'num_stdv': 3.}

    result, result_baseline = remove_baseline(df, 'Polyfit', params=methodParameters)
    expected = [-2968.315, 1.06, 1927.81, 2016.185, 1920.06]
    expected_baseline = [4178.375, 1551., -61.75, -853.125, -1000.]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))

    expected_ranges = {'poly_order_': (1, 12, 'integer'),
                       'stdv_': (1, 5, 'linear')}
    br_obj = polyfit.PolyFit()
    assert br_obj.param_ranges() == expected_ranges


def test_Dietrich():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'half_window': 10,
                        'num_erosions': 2}

    result, result_baseline = remove_baseline(df, 'Dietrich', params=methodParameters)
    expected = [0., 355.294155, 682.58831, -7.117535, -236.82338 ]
    expected_baseline = [1210.06, 1196.765845, 1183.47169, 1170.177535, 1156.88338 ]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))

    expected_ranges = {'half_window_': (1, 100, 'integer'),
                       'num_erosions_': (1, 20, 'integer')}
    br_obj = dietrich.Dietrich()
    assert br_obj.param_ranges() == expected_ranges

def test_AirPLS():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'smoothness_param': 100,
                        'conv_thresh': 0.01,
                        'max_iters': 5,
                        'verbose':True}

    result, result_baseline = remove_baseline(df, 'AirPLS', params=methodParameters)
    expected = [168.813415, 512.518371, 828.223327, 126.928282, -113.037659]
    expected_baseline = [1041.246585, 1039.541629, 1037.836673, 1036.131718, 1033.097659]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))

    expected_ranges = {'smoothness_': (1, 1e4, 'log')}

    br_obj=airpls.AirPLS()
    assert br_obj.param_ranges()==expected_ranges

def test_ALS():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'asymmetry_param': 0.05,
                        'smoothness_param': 1e6,
                        'max_iters': 10,
                        'conv_thresh': 1e-5,
                        'verbose':True}

    result, result_baseline = remove_baseline(df, 'ALS', params=methodParameters)
    expected = [-151.880266, 200.842386, 525.565183, -166.711742, -398.988281]
    expected_baseline = [1361.940266, 1351.217614, 1340.494817, 1329.771742, 1319.048281]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[5, 0:5]))
    np.testing.assert_array_almost_equal(expected_baseline, np.array(result_baseline['wvl'].iloc[5, 0:5]))

    expected_ranges = {'asymmetry_': (1e-3, 1e-1, 'log'),
            'smoothness_': (1e2, 1e8, 'log')}
    br_obj = als.ALS()
    assert br_obj.param_ranges() == expected_ranges

test_KK()
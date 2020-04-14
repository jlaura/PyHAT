import numpy as np
import pandas as pd
from libpyhat.examples import get_path
from libpyhat.transform.norm import norm
from libpyhat.transform.remove_baseline import remove_baseline
from libpyhat.transform.baseline_code import airpls, als, dietrich,polyfit, kajfosz_kwiatek, median, fabc, rubberband, common
np.random.seed(1)

def br_caller(df, method, params, expected, expected_baseline):
    df = norm(df,[[580,600]])
    result, result_baseline = remove_baseline(df, method, params=params)
    np.testing.assert_array_almost_equal(expected,np.array(result['wvl'].iloc[5,0:5]))
    np.testing.assert_array_almost_equal(expected_baseline,np.array(result_baseline['wvl'].iloc[5,0:5]))

def test_min_interp():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'window':10,'kind':'cubic'}
    expected = [0.000000e+00, 8.816021e-03, 1.351492e-02, 6.270307e-03, -2.602085e-18]
    expected_baseline = [0.010179, 0.00424 , 0.002183, 0.003513, 0.00774 ]
    br_caller(df, 'Min + Interpolate', methodParameters, expected, expected_baseline)

    #test case where the window is too big
    methodParameters = {'window': 1000, 'kind': 'cubic'}
    expected = [0.010179, 0.013056, 0.015697, 0.009784, 0.00774 ]
    expected_baseline = [0, 0, 0, 0, 0]
    br_caller(df, 'Min + Interpolate', methodParameters, expected, expected_baseline)


def test_wavelet_spline():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])

    #test case where levelmin is too big
    methodParameters = {'level': 6, 'levelmin': 5}
    expected = [0.010179, 0.013056, 0.015697, 0.009784, 0.00774]
    expected_baseline = [0., 0., 0., 0., 0.]
    br_caller(df,'Wavelet a Trous + Spline',methodParameters,expected, expected_baseline)

    methodParameters = {'level': 6, 'levelmin': 2}
    expected = [0., 0.0039, 0.00726, 0.001804, 0.]
    expected_baseline = [0.010179, 0.009156, 0.008438, 0.00798, 0.00774]
    br_caller(df, 'Wavelet a Trous + Spline', methodParameters, expected, expected_baseline)

def test_Rubberband():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'num_iters': 8, 'num_ranges': 4}
    expected = [0.,  0.002516,  0.005217, -0.000218, -0.001363]
    expected_baseline = [0.010179, 0.01054 , 0.010481, 0.010002, 0.009102]
    br_caller(df,'Rubberband',methodParameters,expected,expected_baseline)

    #test no iterations
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'num_iters': 0, 'num_ranges': 4}
    expected = [0., 0.003487, 0.006738, 0.001434, 0.]
    expected_baseline = [0.010179, 0.009569, 0.008959, 0.008349, 0.00774]
    br_caller(df, 'Rubberband', methodParameters, expected, expected_baseline)

    # test ranges
    expected_ranges = {'num_ranges': (1, 100, 'integer'),
                       'num_iters': (0, 36, 'integer')}
    br_obj = rubberband.Rubberband()
    assert br_obj.param_ranges() == expected_ranges

def test_median():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'window_size': 30}
    expected = [ 0.00244 ,  0.00477 ,  0.007133,  0.001127, -0.001438]
    expected_baseline = [0.00774 , 0.008286, 0.008564, 0.008657, 0.009178]
    br_caller(df,'Median',methodParameters,expected,expected_baseline)

    # test ranges
    expected_ranges = {'window_size': (201, 901, 'integer')}
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
    expected = [-0.119923, -0.117072, -0.114455, -0.120391, -0.122455]
    expected_baseline = [0.130102, 0.130128, 0.130152, 0.130174, 0.130194]
    br_caller(df,'KK',methodParameters,expected,expected_baseline)

    #test using just bottom width
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'top_width': 0, 'bottom_width': 50, 'exponent': 2, 'tangent': False}
    expected = [0.002431, 0.005307, 0.007949, 0.002039, 0.]
    expected_baseline = [0.007748, 0.007749, 0.007748, 0.007745, 0.00774 ]
    br_caller(df,'KK',methodParameters,expected,expected_baseline)

    # test ranges
    expected_ranges = {'top_width': (0, 100, 'integer'),
                       'bottom_width': (0, 100, 'integer')}
    br_obj = kajfosz_kwiatek.KajfoszKwiatek()
    assert br_obj.param_ranges() == expected_ranges


def test_FABC():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'dilation_param': 50, 'smoothness_param': 1e3}
    expected = [-0.013034, -0.01017 , -0.007552, -0.013497, -0.015585]
    expected_baseline = [0.023213, 0.023226, 0.02325 , 0.02328 , 0.023325]
    br_caller(df,'FABC',methodParameters,expected,expected_baseline)

    # test ranges
    expected_ranges = {'dilation_param': (1, 100, 'integer'),
                       'smoothness_param': (1, 1e6, 'log')}
    br_obj = fabc.FABC()
    assert br_obj.param_ranges() == expected_ranges

def test_Polyfit():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'poly_order': 5, 'num_stdv': 3.}
    expected = [-2.500340e-02, -3.468003e-06,  1.620876e-02,  1.696360e-02, 1.616043e-02]
    expected_baseline = [ 0.035183,  0.01306 , -0.000511, -0.00718 , -0.008421]
    br_caller(df,'Polyfit',methodParameters,expected,expected_baseline)

    # test ranges
    expected_ranges = {'poly_order': (1, 12, 'integer'),
                       'num_stdv': (1, 5, 'linear')}
    br_obj = polyfit.PolyFit()
    assert br_obj.param_ranges() == expected_ranges

def test_Dietrich():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'half_window': 10,
                        'num_erosions': 2}
    expected = [ 0.000000e+00,  2.988763e-03,  5.741989e-03, -5.987328e-05,
       -1.992178e-03]
    expected_baseline = [0.010179, 0.010067, 0.009955, 0.009844, 0.009732]
    br_caller(df,'Dietrich',methodParameters,expected,expected_baseline)

    #test ranges
    expected_ranges = {'half_window': (1, 100, 'integer'),
                       'num_erosions': (1, 20, 'integer')}
    br_obj = dietrich.Dietrich()
    assert br_obj.param_ranges() == expected_ranges

def test_AirPLS():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'smoothness_param': 100,
                        'conv_thresh': 0.01,
                        'max_iters': 5,
                        'verbose':True}
    expected = [ 0.00142 ,  0.004311,  0.006967,  0.001068, -0.000951]
    expected_baseline = [0.008759, 0.008745, 0.00873 , 0.008716, 0.008691]
    br_caller(df,'AirPLS',methodParameters,expected,expected_baseline)

    # test ranges
    expected_ranges = {'smoothness_param': (1, 1e4, 'log')}

    br_obj=airpls.AirPLS()
    assert br_obj.param_ranges()==expected_ranges

def test_ALS():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    methodParameters = {'asymmetry_param': 0.05,
                        'smoothness_param': 1e6,
                        'max_iters': 10,
                        'conv_thresh': 1e-5,
                        'verbose':True}
    expected = [-0.001278,  0.00169 ,  0.004421, -0.001402, -0.003356]
    expected_baseline = [0.011457, 0.011367, 0.011276, 0.011186, 0.011096]
    br_caller(df,'ALS',methodParameters,expected,expected_baseline)

    #test ranges
    expected_ranges = {'asymmetry_param': (1e-3, 1e-1, 'log'),
                       'smoothness_param': (1e2, 1e8, 'log')}
    br_obj = als.ALS()
    assert br_obj.param_ranges() == expected_ranges

def test_not_recognized():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    result = remove_baseline(df, 'foo', params=None)
    assert result == 0

def test_common():
    #this test hits parts of the common baseline code not covered above
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    wvls = np.array(df['wvl'].columns.values, dtype='float')
    spectra = np.array(df['wvl'], dtype='float')

    #test fit_transform
    br_obj = als.ALS()
    result = br_obj.fit_transform(wvls,spectra)
    expected = [-151.88026557, 200.84238645, 525.56518276, -166.71174241, -398.98828107]
    np.testing.assert_array_almost_equal(expected,result[5,0:5])

    #test fit on single spectrum
    result = br_obj.fit(wvls, spectra[0,:])
    expected = [1063.366517, 1059.53780945, 1055.70887361, 1051.87920998, 1048.0481028 ]
    np.testing.assert_array_almost_equal(expected, result.baseline[0:5])

    #test segmenting
    wvls = np.array(df['wvl'].columns.values,dtype=float)
    wvls[20:]= wvls[20:]+10

    result = [i for i in common._segment(wvls, np.array(df['wvl']))]
    assert result[0][0][0] == 585.149
    assert result[1][0][0] == 599.644




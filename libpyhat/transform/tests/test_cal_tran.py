import numpy as np
import pandas as pd
from libpyhat.examples import get_path
from libpyhat.transform import cal_tran, norm
from libpyhat.transform.caltran_utils import prepare_data
np.random.seed(1)

data1 = pd.read_csv(get_path('caltran_test1.csv'),header=[0,1])
data2 = pd.read_csv(get_path('caltran_test2.csv'),header=[0,1])
data1, data2 = prepare_data(data1,data2,'Target','Target')

#normalize the data for numerical stability
data1 = norm.norm(data1,[[240,250]])
data2 = norm.norm(data2,[[240,250]])


def cal_tran_helper(data1,data2,params, expected, single_spect = False):
    ct = cal_tran.cal_tran(params)
    ct.derive_transform(data1['wvl'], data2['wvl'])
    if single_spect:
        result = ct.apply_transform(data1['wvl'].iloc[0,:])
    else:
        result = ct.apply_transform(data1['wvl'])
    if len(result.shape)>1:
        np.testing.assert_array_almost_equal(np.array(result,dtype=float)[:, 4], expected)
    else:
        np.testing.assert_array_almost_equal(np.array(result,dtype=float)[4], expected)

def test_no_transform():
    params = {'method':'None'}
    ct = cal_tran.cal_tran(params)
    ct.derive_transform(data1['wvl'], data2['wvl'])
    result = ct.apply_transform(data1['wvl'])
    pd.testing.assert_frame_equal(data1['wvl'], result)

def test_undefined():
    params = {'method':'foo'}
    ct = cal_tran.cal_tran(params)
    assert ct.ct_obj == None

    params = {'method': 'LASSO DS','reg':'foo'}
    ct = cal_tran.cal_tran(params)
    ct.derive_transform(data1['wvl'],data2['wvl'])
    assert ct.ct_obj.proj_to_B == None

def test_ratio():
    params = {'method':'Ratio'}
    expected = [ 0.318841,  0.02854 ,  0.065888,  0.028543, -0.036599,  0.028683,  0.076133]
    cal_tran_helper(data1, data2, params, expected)

def test_piecewise_ds():
    params = {'method': 'PDS - Piecewise DS', 'win_size':5,'pls':False}
    expected = [0.178173, 0.022496, 0.053328, 0.055634, 0.078359, 0.042854, 0.080929]
    cal_tran_helper(data1, data2, params, expected)

def test_piecewise_ds_pls():
    params = {'method':  'PDS-PLS - PDS using Partial Least Squares', 'win_size': 5, 'pls': True}
    expected = [0.892316, 0.717635, 0.759557, 0.776147, 0.785993, 0.783869, 0.790914]
    cal_tran_helper(data1, data2, params, expected)

def test_ds():
    params = {'method': 'DS - Direct Standardization', 'fit_intercept':False}
    expected = [0.178577, 0.001241, 0.051551, 0.063651, 0.072738, 0.069143,  0.073129]
    cal_tran_helper(data1, data2, params, expected)

    #test fit intercept
    params = {'method': 'DS - Direct Standardization', 'fit_intercept': True}
    expected = [0.178577, 0.001241, 0.051551, 0.063651, 0.072738, 0.069143, 0.073129]
    cal_tran_helper(data1, data2, params, expected)

    #test single spectrum
    params = {'method': 'DS - Direct Standardization','fit_intercept':False}
    expected = 0.178577
    cal_tran_helper(data1, data2, params, expected, single_spect=True)

def test_lasso():
    params = {'method': 'LASSO DS', 'reg':'lasso'}
    expected = [0.054903, 0.06442 , 0.057151, 0.064025, 0.084927, 0.06608, 0.056687]
    cal_tran_helper(data1, data2, params, expected)

    params = {'method': 'LASSO DS', 'reg': 'lasso'}
    expected = 0.054903
    cal_tran_helper(data1, data2, params, expected, single_spect=True)

def test_fused():
    ct = cal_tran.admm_ds(reg='fused')
    ct.derive_transform(data1['wvl'], data2['wvl'])
    result = ct.apply_transform(data1['wvl'])
    expected = [0.131446, 0.075009, 0.077237, 0.076254, 0.079208, 0.076004,  0.080078]
    np.testing.assert_array_almost_equal(np.array(result,dtype=float)[:, 4], expected)

def test_rank():
    ct = cal_tran.admm_ds(reg='rank')
    ct.derive_transform(data1['wvl'], data2['wvl'])
    result = ct.apply_transform(data1['wvl'])
    expected = [0.137651, 0.069806, 0.071676, 0.071139, 0.076506, 0.071349, 0.074898]
    np.testing.assert_array_almost_equal(np.array(result,dtype=float)[:, 4], expected)

def test_ridge():
    params = {'method': 'Ridge DS', 'reg': 'ridge'}
    expected = [0.080705, 0.058048, 0.057408, 0.058376, 0.064338, 0.05882, 0.058512]
    cal_tran_helper(data1, data2, params, expected)

def test_sp_lr():
    params = {'method': 'Sparse Low Rank DS', 'reg': 'sp_lr'}
    expected = [0.086601, 0.068787, 0.065989, 0.068998, 0.080721, 0.070023, 0.066837]
    cal_tran_helper(data1, data2, params, expected)

def test_cca():
    params = {'method': 'CCA - Canonical Correlation Analysis'}
    expected = [0.173499, 0.035199, 0.065695, 0.045576, 0.063046, 0.057604,  0.069411]
    cal_tran_helper(data1, data2, params, expected)

    params = {'method': 'CCA - Canonical Correlation Analysis'}
    expected = [0.173499]
    cal_tran_helper(data1, data2, params, expected, single_spect=True)

def test_cca_new():
    params = {'method': 'New CCA', 'ccatype':'new'}
    expected = [0.102786, -0.047663, -0.014488, -0.036374, -0.01737, -0.02329 , -0.010446]
    cal_tran_helper(data1, data2, params, expected)

def test_ipd_ds():
    params = {'method':'Incremental Proximal Descent DS'}
    expected = [0.136078,  0.012181,  0.02812,  0.012182, -0.01562, 0.012242,  0.032493]
    cal_tran_helper(data1, data2, params, expected)

def test_forward_backward_ds():
    params = {'method': 'Forward Backward DS'}
    expected = [0.00015 , 0.00019 , 0.000174, 0.000188, 0.000235, 0.000193,  0.000172]
    cal_tran_helper(data1, data2, params, expected)

def test_prepare_data_no_repeats():
    a,b = prepare_data(data1, data2, 'Target', 'Target')
    pd.testing.assert_frame_equal(a,data1)
    pd.testing.assert_frame_equal(b, data2)

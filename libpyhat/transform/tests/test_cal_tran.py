import numpy as np
import pandas as pd
from libpyhat.examples import get_path
from libpyhat.transform import cal_tran
from libpyhat.transform.caltran_utils import prepare_data

data1 = pd.read_csv(get_path('caltran_test1.csv'),header=[0,1])
data2 = pd.read_csv(get_path('caltran_test2.csv'),header=[0,1])
data1, data2 = prepare_data(data1,data2,'Target','Target')

def cal_tran_helper(data1,data2,params, expected, single_spect = False):
    ct = cal_tran.cal_tran(params)
    ct.derive_transform(data1['wvl'], data2['wvl'])
    if single_spect:
        result = ct.apply_transform(data1['wvl'].iloc[0,:])
    else:
        result = ct.apply_transform(data1['wvl'])
    if len(result.shape)>1:
        np.testing.assert_array_almost_equal(np.array(result)[:, 4], expected)
    else:
        np.testing.assert_array_almost_equal(np.array(result)[4], expected)

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
    expected = [36534916958.477615, 126211263696.69794, 259194764038.6235, 95005798500.24937, -25195900571.396236,
                74384983186.39635, 177294858496.4514]
    cal_tran_helper(data1, data2, params, expected)

def test_piecewise_ds():
    params = {'method': 'PDS - Piecewise DS', 'win_size':5,'pls':False}
    expected = [2518296750.7669373, 22939818289.340088, 133837284646.25781, 143969630699.28076, 131001824154.48917,
                141823720448.1682, 165079532503.75415]
    cal_tran_helper(data1, data2, params, expected)

def test_piecewise_ds_pls():
    params = {'method':  'PDS-PLS - PDS using Partial Least Squares', 'win_size': 5, 'pls': True}
    expected = [-267781865648.5343, -247623829267.95703, -123176082646.5293, -124548787498.16602, -125447616089.96704,
                -139565106866.63477, -116198982744.31836]
    cal_tran_helper(data1, data2, params, expected)

def test_ds():
    params = {'method': 'DS - Direct Standardization', 'fit_intercept':False}
    expected = [14390389678.999939, 3040294626.501465, 159500000000.00146, 155500000000.0, 129000000000.00037,
                154500000000.00098, 127500000000.00073]
    cal_tran_helper(data1, data2, params, expected)

    #test fit intercept
    params = {'method': 'DS - Direct Standardization', 'fit_intercept': True}
    expected = [14390389679.000206, 3040294626.5009766, 159500000000.00122,
       155500000000.00122, 129000000000.00043, 154500000000.0022,
       127500000000.00098]
    cal_tran_helper(data1, data2, params, expected)

    #test single spectrum
    params = {'method': 'DS - Direct Standardization','fit_intercept':False}
    expected = 14390389678.999939
    cal_tran_helper(data1, data2, params, expected, single_spect=True)

def test_lasso():
    params = {'method': 'LASSO DS', 'reg':'lasso'}
    expected = [1190077827.480402, 53889464287.102356, 42529733431.96185, 40313198120.17833, 11059787150.482561,
                32416798086.29209, 24971837215.286034]
    cal_tran_helper(data1, data2, params, expected)

    params = {'method': 'LASSO DS', 'reg': 'lasso'}
    expected = 1190077827.480402
    cal_tran_helper(data1, data2, params, expected, single_spect=True)

def test_fused():
    ct = cal_tran.admm_ds(reg='fused')
    ct.derive_transform(data1['wvl'], data2['wvl'])
    result = ct.apply_transform(data1['wvl'])
    expected = [2849243131.0724015, 62747825214.21766, 57476877313.03153, 48012638532.69881, 10315037639.60446,
                37285141026.96995, 35276208169.25773]
    np.testing.assert_array_almost_equal(np.array(result)[:, 4], expected)

def test_rank():
    ct = cal_tran.admm_ds(reg='rank')
    ct.derive_transform(data1['wvl'], data2['wvl'])
    result = ct.apply_transform(data1['wvl'])
    expected = [2983729459.6655235, 58395418330.43097, 53338740816.48527, 44792462932.167305, 9963178402.018112,
                35001553532.792885, 32994432752.733253]
    np.testing.assert_array_almost_equal(np.array(result)[:, 4], expected)

def test_ridge():
    params = {'method': 'Ridge DS', 'reg': 'ridge'}
    expected = [1749378667.735192, 48558975799.3131, 42721051828.34153, 36755957102.83551, 8378554736.596158,
                28855256282.60194, 25775733813.46185]
    cal_tran_helper(data1, data2, params, expected)

def test_sp_lr():
    params = {'method': 'Sparse Low Rank DS', 'reg': 'sp_lr'}
    expected = [1877170886.930834, 57542919512.710205, 49106458502.41265, 43444221540.97199, 10512067271.173079,
                34351170567.167973, 29443294204.300148]
    cal_tran_helper(data1, data2, params, expected)

def test_cca():
    params = {'method': 'CCA - Canonical Correlation Analysis'}
    expected = [92044557972.7028, 105920435813.84615, 114193459070.33023, 108757580896.19865, 109998305126.70969, 108690052718.79832, 103826292706.91415]
    cal_tran_helper(data1, data2, params, expected)

    params = {'method': 'CCA - Canonical Correlation Analysis'}
    expected = [92044557972.7028]
    cal_tran_helper(data1, data2, params, expected, single_spect=True)

def test_cca_new():
    params = {'method': 'New CCA', 'ccatype':'new'}
    expected = [-79330279537.80644, 9324121672.360352, 62181312503.680176, 27450931471.487793, 35378045343.64673,
                27019487046.79834, -4055572594.114502]
    cal_tran_helper(data1, data2, params, expected)

def test_ipd_ds():
    params = {'method':'Incremental Proximal Descent DS'}
    expected = [2949631085.173894, 10189613052.137402, 20925979768.656185, 7670253003.355394, -2034180387.7316878,
                6005440190.984758, 14313825496.222805]
    cal_tran_helper(data1, data2, params, expected)

def test_forward_backward_ds():
    params = {'method': 'Forward Backward DS'}
    expected = [3249297.3595255464, 159194775.40413117, 129173821.12988204, 118581703.09505463, 30645501.99455126,
                94605059.37954581, 75735758.32418025]
    cal_tran_helper(data1, data2, params, expected)
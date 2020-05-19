import numpy as np
import pandas as pd
from libpyhat.examples import get_path
import libpyhat.transform.deriv as deriv
import libpyhat.transform.dim_red as dim_red
import libpyhat.transform.interp as interp
import libpyhat.transform.mask as mask
import libpyhat.transform.meancenter as meancenter
import libpyhat.transform.multiply_vector as multiply_vector
import libpyhat.transform.norm as norm
import libpyhat.transform.shift_spect as shift_spect
import libpyhat.clustering.cluster as cluster
np.random.seed(1)


def test_shift_spect():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    result = shift_spect.shift_spect(df,-1.0)
    expected = [898.64928571, 973.62444444, 1034.46444444, 1004.54, 939.16222222]
    np.testing.assert_array_almost_equal(expected,np.array(result['wvl'].iloc[0,0:5]))
    assert result[('meta','Shift')].shape == (103,)

def test_norm():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    result = norm.norm(df,[[580,590],[590,600]],col_var='wvl')
    np.testing.assert_almost_equal(result['wvl'].iloc[0,:].sum(), 2.0)

def test_multiply_vector():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    result = multiply_vector.multiply_vector(df, get_path('vector.csv'))
    expected = [1646.12, 1548.12, 1656.12, 1656.12, 1732.12]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[0,0:5]))

    result = multiply_vector.multiply_vector(df, get_path('bad_vector.csv'))
    assert result == 0

def test_meancenter():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    result_df, mean_vect = meancenter.meancenter(df,'wvl')
    expected = [-168.05398058, 579.71601942, 309.16601942, 709.21601942, -341.00398058]
    expected_mv = [ 991.11398058, 1160.24990291, 1287.87126214, 931.56058252, 838.89067961]
    np.testing.assert_array_almost_equal(expected, np.array(result_df['wvl'].iloc[0:5,0]))
    np.testing.assert_array_almost_equal(expected_mv, np.array(mean_vect)[0:5])

    #test providing the mean vector
    mean_vect.iloc[:] = 1
    result_df2, mean_vect2 = meancenter.meancenter(df,'wvl',previous_mean=mean_vect)
    expected2 = np.array(expected) - 1.0
    expected_mv2 = [1., 1., 1., 1., 1.]
    np.testing.assert_array_almost_equal(expected2, np.array(result_df2['wvl'].iloc[0:5,0]))
    np.testing.assert_array_almost_equal(expected_mv2, np.array(mean_vect2)[0:5])

    #test mismatched wvls
    mean_vect.index = np.array(mean_vect.index,dtype=float) + 1.0
    result = meancenter.meancenter(df, 'wvl', previous_mean=mean_vect)
    assert result == 0


def test_mask():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    result = mask.mask(df,get_path('mask.csv'))
    assert result['wvl'].columns[0] == 586.049
    assert result['wvl'].columns[-1] == 589.869
    assert result['wvl'].shape == (103,18)
    assert result['masked'].shape == (103,26)

def test_interp():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    result = interp.interp(df,[588, 590, 592, 594])
    expected = [1637.58, 1104.47964286, 830.53321429, 857.77875]
    assert result['wvl'].shape == (103,4)
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[0,:]))

def test_deriv():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    result = deriv.deriv(df)
    expected = [-0.08370717, 1.08648488, 0.83536337, 1.59556113, 0.13666476]
    np.testing.assert_array_almost_equal(expected, np.array(result['wvl'].iloc[0:5,0]))

def test_dimred_JADE():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])

    params = {'n_components': 3}

    df, dimred_obj = dim_red.dim_red(df, 'wvl', 'JADE-ICA', [], params)
    expected_loadings = [0.56247385, 0.19292341, 3.42289881]
    expected_scores = [174708.34499912, 125682.55985134, 145155.40758151]

    assert df['JADE-ICA'].shape == (103, 3)
    np.testing.assert_almost_equal(expected_loadings, np.squeeze(np.array(dimred_obj.ica_jade_loadings[:,0])))
    np.testing.assert_array_almost_equal(expected_scores, np.array(df['JADE-ICA'].iloc[0,:]))

def test_dimred_LLE():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])

    params = {'n_components': 3,
              'n_neighbors': 10,
              'reg': 1e-3}
    df, dimred_obj = dim_red.dim_red(df, 'wvl', 'LLE', [], params)
    expected_err = 2.0687806439705738e-05
    expected_scores = [0.11088153, 0.01215013, -0.03551393]

    assert df['LLE'].shape == (103, 3)
    np.testing.assert_almost_equal(expected_err, dimred_obj.reconstruction_error_)
    np.testing.assert_array_almost_equal(np.abs(expected_scores), np.abs(np.array(df['LLE'].iloc[0, :])),decimal=4)

def test_dimred_tSNE():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])

    params = {
        'n_components': 2,
        'learning_rate': 200.0,
        'n_iter': 1000,
        'n_iter_without_progress': 300,
        'perplexity': 30,
        'init': 'pca'}
    df, dimred_obj = dim_red.dim_red(df, 'wvl', 't-SNE', [], params)
    expected_div = 0.38829776644706726
    expected_scores = [9938.469727, -802.161682]

    assert df['t-SNE'].shape == (103, 2)
    np.testing.assert_almost_equal(expected_div, dimred_obj.kl_divergence_)
    np.testing.assert_array_almost_equal(expected_scores, np.array(df['t-SNE'].iloc[0, :]))

def test_dimred_FastICA():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])

    params = {'n_components': 3, 'random_state':1}
    df, dimred_obj = dim_red.dim_red(df, 'wvl', 'FastICA', [], params)
    expected_comps = [-2.190278e-05,  1.498101e-06,  9.082887e-07]
    expected_scores = [0.03252833, -0.03749623, -0.11434307]

    assert df['FastICA'].shape == (103, 3)
    np.testing.assert_array_almost_equal(expected_comps, dimred_obj.components_[:, 0])
    np.testing.assert_array_almost_equal(expected_scores, np.array(df['FastICA'].iloc[0, :]))

def test_dimred_PCA():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])

    params = {'n_components': 3}
    df, dimred_obj = dim_red.dim_red(df, 'wvl', 'PCA', [], params)
    expected_expl_var = [0.96051211, 0.01683739, 0.01471955]
    expected_scores = [10092.96265442, -628.16699776, -359.06894452]
    assert df['PCA'].shape == (103,3)
    np.testing.assert_array_almost_equal(expected_expl_var, dimred_obj.explained_variance_ratio_)
    np.testing.assert_array_almost_equal(expected_scores,np.array(df['PCA'].iloc[0,:]))

def test_dimred_NMF():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    df['wvl'] = df['wvl'] - 1000 #make some values negative to test adding a constant
    dim_red.check_positive(df['wvl'])
    params = {'n_components': 3,
        'random_state': 0,
        'add_constant': True}
    df, dimred_obj = dim_red.dim_red(df, 'wvl', 'NMF', [], params)
    expected_comps = [10.27191532, 34.62489686, 3.06822373]
    expected_scores = [49.42458628, 3.9910722, 27.03100371]
    assert df['NMF'].shape == (103,3)
    np.testing.assert_array_almost_equal(expected_comps, dimred_obj.components_[:,0])
    np.testing.assert_array_almost_equal(expected_scores,np.array(df['NMF'].iloc[0,:]))

def test_dimred_LDA():

    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    kws = {'n_clusters': 5,
           'n_init': 10,
           'max_iter': 100,
           'tol': 0.01,
           'n_jobs': 1,
           'random_state': 1}
    cluster.cluster(df, 'wvl', 'K-Means', [], kws)
    params = {'n_components': 3}
    df, dimred_obj = dim_red.dim_red(df, 'wvl', 'LDA', [], params, ycol='K-Means')
    expected_coefs = [-0.02209121, -0.0016516, -0.01139357, -0.06448139, 0.07085655]
    expected_scores = [-11.89340048, 0.41598425, 0.22964169]
    assert df['LDA'].shape == (103, 3)
    np.testing.assert_array_almost_equal(expected_coefs, dimred_obj.coef_[:, 0])
    np.testing.assert_array_almost_equal(expected_scores, np.array(df['LDA'].iloc[0, :]))

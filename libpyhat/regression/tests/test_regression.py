import numpy as np
import pandas as pd
from libpyhat.examples import get_path
from libpyhat.regression.regression import regression

df = pd.read_csv(get_path('test_data.csv'),header=[0,1])
x = df['wvl']
y = df[('comp','SiO2')]

def test_PLS():
    regress = regression(method=['PLS'],
                         params=[{'n_components': 3, 'scale': False}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 13.801824573081946
    np.testing.assert_almost_equal(rmse, expected)

    regress.calc_Qres_Lev(x)
    Qres_expected = [2.35103099e+08, 2.36647676e+08, 2.35449237e+08, 2.36345327e+08, 2.33488060e+08, 2.36975197e+08,
                     2.35345188e+08, 2.35190537e+08, 2.35189934e+08, 2.32935818e+08]
    np.testing.assert_array_almost_equal(regress.Q_res[0:10], Qres_expected, decimal=0)
    leverage_expected = [0.01854551, 0.04063431, 0.02558205, 0.10486388, 0.03121949, 0.0393575, 0.0084857, 0.01386892,
                         0.01066457, 0.06845841]
    np.testing.assert_array_almost_equal(regress.leverage[0:10], leverage_expected)


def test_badfit():
    regress = regression(method=['PLS'],
                         params=[{'n_components': 300, 'scale': False}])
    regress.fit(x, y)
    assert regress.goodfit == False

def test_OLS():
    regress = regression(method=['OLS'],
                         params=[{'fit_intercept': True}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 6.935420148428834
    np.testing.assert_almost_equal(rmse, expected)


def test_OMP():
    regress = regression(method=['OMP'], params=[{'fit_intercept': True}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 10.560905826959745
    np.testing.assert_almost_equal(rmse, expected)

def test_LASSO():
    regress = regression(method=['LASSO'],
                         params=[{'alpha': 1.0,
                                  'fit_intercept': True,
                                  'positive': False}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 7.027314035067699
    np.testing.assert_almost_equal(rmse, expected)


def test_Elastic_Net():
    regress = regression(method=['Elastic Net'],
                         params=[{'alpha': 1.0,
                                  'l1_ratio': 0.5,
                                  'fit_intercept': True,
                                  'positive': False}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 7.019810621596676
    np.testing.assert_almost_equal(rmse, expected)



def test_Ridge():
    regress = regression(method=['Ridge'],
                         params=[{'alpha': 1.0,
                                  'fit_intercept': True}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 6.935420151711957
    np.testing.assert_almost_equal(rmse, expected)

def test_Bayesian_Ridge():
    regress = regression(method=['BRR'],
                         params=[{'n_iter': 300,
                                  'tol': 0.001,
                                  'alpha_1': 0.001,
                                  'alpha_2': 1e-06,
                                  'lambda_1': 1e-06,
                                  'lambda_2': 1e-06,
                                  'compute_score': False,
                                  'fit_intercept': True,
                                  'normalize': False}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 7.843189715819001
    np.testing.assert_almost_equal(rmse, expected)


def test_ARD():
    regress = regression(method=['ARD'],
                         params=[{'n_iter': 300,
                                  'tol': 0.001,
                                  'alpha_1': 0.001,
                                  'alpha_2': 1e-06,
                                  'lambda_1': 1e-06,
                                  'lambda_2': 1e-06,
                                  'compute_score': False,
                                  'threshold_lambda': 100000,
                                  'fit_intercept': True,
                                  'normalize': False,
                                  'copy_X': True,
                                  'verbose': False}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 7.981886512289962
    np.testing.assert_almost_equal(rmse, expected)


def test_LARS():
    regress = regression(method=['LARS'],
                         params=[{'n_nonzero_coefs': 5,
                                  'fit_intercept': True,
                                  'normalize': False,
                                  'precompute': True,
                                  'copy_X': True,
                                  'eps': 2.220445,
                                  'fit_path': True}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 15.605082215087926
    np.testing.assert_almost_equal(rmse, expected)


def test_SVR():
    regress = regression(method=['SVR'], params=[{'C': 1.0, 'epsilon': 0.1,
                                                   'kernel': 'rbf',
                                                   'degree': 0,
                                                   'gamma': 'auto',
                                                   'coef0': 0.0,
                                                   'shrinking': False,
                                                   'tol': 0.001,
                                                   'cache_size': 200,
                                                   'verbose': False,
                                                   'max_iter': -1}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 23.05563865877408
    np.testing.assert_almost_equal(rmse, expected)


def test_KRR():
    regress = regression(method=['KRR'],
                         params=[{'alpha': 0,
                                  'kernel': 'linear',
                                  'gamma': 'None',
                                  'degree': 3.0,
                                  'coef0': 1.0,
                                  'kernel_params': 'None'}])
    regress.fit(x, y)
    prediction = np.squeeze(regress.predict(x))
    rmse = np.sqrt(np.average((prediction - y) ** 2))
    expected = 10.085128628153841
    np.testing.assert_almost_equal(rmse, expected)



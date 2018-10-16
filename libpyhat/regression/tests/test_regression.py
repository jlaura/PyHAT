from libpyhat.regression.regression import regression


def test_PLS():
    regress = regression(method=['PLS'], yrange=[0.0, 100.0],
                         params=[{'n_components': 0,'scale': False}])


'''
def test_GP():
    regress = regression(method=['GP'], yrange=[0.0, 100.0],
                         params=[{'reduce_dim': 'PCA',
                                  'n_components': 0,
                                  'random_start': 1,
                                  'theta0': 1.0,
                                  'thetaL': 0.1,
                                  'thetaU': 100.0}])
'''


def test_OLS():
    regress = regression(method=['OLS'], yrange=[0.0, 100.0],
                         params=[{'fit_intercept': True}])


def test_OMP_CV_true():
    regress = regression(method=['OMP'], yrange=[0.0, 100.0], params=[{'fit_intercept': True,
                                                                       'CV': True,
                                                                       'precompute': True}])

def test_OMP_CV_false():
    regress = regression(method=['OMP'], yrange=[0.0, 100.0], params=[{'fit_intercept': True,
                                                                       'CV': False}])


def test_LASSO_CV_true():
    regress = regression(method=['LASSO'], yrange=[0.0, 100.0],
                         params=[{'alpha': 1.0,
                                  'fit_intercept': True,
                                  'max_iter': 1000,
                                  'tol': 0.0001,
                                  'positive': False,
                                  'selection': 'random',
                                  'CV': True}])

def test_LASSO_CV_none():
    regress = regression(method=['LASSO'], yrange=[0.0, 100.0],
                         params=[{'alpha': 1.0,
                                  'fit_intercept': True,
                                  'max_iter': 1000,
                                  'tol': 0.0001,
                                  'positive': False,
                                  'selection': 'random'}])


def test_Elastic_Net_CV_none():
    regress = regression(method=['Elastic Net'], yrange=[0.0, 100.0],
                         params=[{'alpha': 1.0,
                                  'l1_ratio': 0.5,
                                  'fit_intercept': True,
                                  'normalize': False,
                                  'precompute': 'False',
                                  'max_iter': 1000,
                                  'copy_X': True,
                                  'tol': 0.0001,
                                  'warm_start': False,
                                  'positive': False,
                                  'selection': 'cyclic',
                                  'random_state': 'None'}])

def test_Elastic_Net_CV_true():
    regress = regression(method=['Elastic Net'], yrange=[0.0, 100.0],
                         params=[{'l1_ratio': 0.5,
                                  'fit_intercept': True,
                                  'normalize': False,
                                  'precompute': 'False',
                                  'max_iter': 1000,
                                  'copy_X': True,
                                  'tol': 0.0001,
                                  'positive': False,
                                  'selection': 'cyclic',
                                  'random_state': 'None',
                                  'CV': True}])


def test_Ridge_CV_none():
    regress = regression(method=['Ridge'], yrange=[0.0, 100.0],
                         params=[{'alpha': 1.0,
                                  'copy_X': True,
                                  'fit_intercept': True,
                                  'max_iter': 'None',
                                  'normalize': False,
                                  'solver': 'auto',
                                  'tol': 0.0,
                                  'random_state': ''}])

def test_Ridge_CV_true():
    regress = regression(method=['Ridge'], yrange=[0.0, 100.0],
                         params=[{'fit_intercept': True,
                                  'normalize': False,
                                  'CV': True}])

def test_Bayesian_Ridge():
    regress = regression(method=['Bayesian Ridge'], yrange=[0.0, 100.0],
                         params=[{'n_iter': 300,
                                  'tol': 0.001,
                                  'alpha_1': 0.001,
                                  'alpha_2': 1e-06,
                                  'lambda_1': 1e-06,
                                  'lambda_2': 1e-06,
                                  'compute_score': False,
                                  'fit_intercept': True,
                                  'normalize': False,
                                  'copy_X': True,
                                  'verbose': False}])


def test_ARD():
    regress = regression(method=['ARD'], yrange=[0.0, 100.0],
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


def test_LARS_CV_none():
    regress = regression(method=['LARS'], yrange=[0.0, 100.0],
                         params=[{'n_nonzero_coefs': 500,
                                  'fit_intercept': True,
                                  'positive': False,
                                  'verbose': False,
                                  'normalize': False,
                                  'precompute': True,
                                  'copy_X': True,
                                  'eps': 2.220445,
                                  'fit_path': True}])

def test_LARS2_CV_true():
    regress = regression(method=['LARS'], yrange=[0.0, 100.0],
                         params=[{'fit_intercept': True,
                                  'positive': False,
                                  'verbose': False,
                                  'normalize': False,
                                  'precompute': True,
                                  'copy_X': True,
                                  'eps': 2.220445,
                                  'CV': True}])

def test_Lasso_LARS_model_0():
    regress = regression(method=['Lasso LARS'], yrange=[0.0, 100.0],
                         params=[{'alpha': 0.0,
                                  'fit_intercept': True,
                                  'positive': False,
                                  'verbose': False,
                                  'normalize': True,
                                  'copy_X': True,
                                  'precompute': 'Auto',
                                  'max_iter': 500,
                                  'model': 0,
                                  'eps': 2.220446,
                                  'fit_path': True}])

def test_Lasso_LARS_model_1():
    regress = regression(method=['Lasso LARS'], yrange=[0.0, 100.0],
                         params=[{'fit_intercept': True,
                                  'positive': False,
                                  'verbose': False,
                                  'normalize': True,
                                  'copy_X': True,
                                  'precompute': 'Auto',
                                  'max_iter': 500,
                                  'model': 1,
                                  'eps': 2.220446}])

def test_Lasso_LARS_model_2():
    regress = regression(method=['Lasso LARS'], yrange=[0.0, 100.0],
                         params=[{'fit_intercept': True,
                                  'positive': False,
                                  'verbose': False,
                                  'normalize': True,
                                  'copy_X': True,
                                  'precompute': 'Auto',
                                  'max_iter': 500,
                                  'model': 2,
                                  'eps': 2.220446}])

def test_Lasso_LARS_model_none():
    regress = regression(method=['Lasso LARS'], yrange=[0.0, 100.0],
                         params=[{'fit_intercept': True,
                                  'positive': False,
                                  'verbose': False,
                                  'normalize': True,
                                  'copy_X': True,
                                  'precompute': 'Auto',
                                  'max_iter': 500,
                                  'model': None,
                                  'eps': 2.220446}])

def test_SVR():
    regress = regression(method=['SVR'], yrange=[0.0, 100.0], params=[{'C': 1.0,
                                                                       'epsilon': 0.1,
                                                                       'kernel': 'rbf',
                                                                       'degree': 0,
                                                                       'gamma': 'auto',
                                                                       'coef0': 0.0,
                                                                       'shrinking': False,
                                                                       'tol': 0.001,
                                                                       'cache_size': 200,
                                                                       'verbose': False,
                                                                       'max_iter': -1}])


def test_KRR():
    regress = regression(method=['KRR'], yrange=[0.0, 100.0],
                         params=[{'alpha': 0,
                                  'kernel': 'linear',
                                  'gamma': 'None',
                                  'degree': 3.0,
                                  'coef0': 1.0,
                                  'kernel_params': 'None'}])

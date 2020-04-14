import numpy as np
import pandas as pd
from libpyhat.examples import get_path
import libpyhat.regression.cv as cv
from libpyhat.utils.folds import stratified_folds
from sklearn.model_selection import ParameterGrid
np.random.seed(1)



def test_cv_nofolds():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    params = {'n_components': [1, 2, 3],
              'scale': [False]}
    paramgrid = list(ParameterGrid(params))

    cv_obj = cv.cv(paramgrid)
    results = cv_obj.do_cv(df, xcols='wvl', ycol=[('comp', 'SiO2')],
                                                                  method='PLS', yrange=[0, 100], calc_path=False,
                                                                  alphas=None)
    print(results)
    assert results == 0


def test_cv():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    df = stratified_folds(df, nfolds=3, sortby=('comp', 'SiO2'))

    params = {'n_components': [1,2,3],
                      'scale': [False]}
    paramgrid = list(ParameterGrid(params))


    cv_obj = cv.cv(paramgrid)
    df_out, output, models, modelkeys, predictkeys = cv_obj.do_cv(df,xcols='wvl',ycol=[('comp','SiO2')],method='PLS',yrange=[0,100],calc_path=False,alphas=None)

    expected_predicts = [56.55707481, 57.93716105, 59.34785052, 60.59708391, 55.83934129, 56.7456989 ]
    expected_output_rmsec = [18.6509206, 14.64015186, 13.80182457]

    np.testing.assert_array_almost_equal(expected_predicts,np.array(df_out['predict'].iloc[0,:]))
    np.testing.assert_array_almost_equal(expected_output_rmsec,np.array(output[('cv','RMSEC')]))
    assert output.shape==(3,8)
    assert len(models)==3
    assert len(modelkeys)==3
    assert modelkeys[0]=='PLS - SiO2 - (0, 100) {\'n_components\': 1, \'scale\': False}'
    assert len(predictkeys)==6
    assert predictkeys[0]=='"PLS- CV -{\'n_components\': 1, \'scale\': False}"'

def test_cv_calc_path():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    df = stratified_folds(df, nfolds=3, sortby=('comp', 'SiO2'))

    params = {
        'fit_intercept': [True, False],
        'max_iter': [1000],
        'tol': [1e-3],
        'precompute': [True],
        'copy_X': [True],
        'positive': [True, False],
        'selection': ['random'],
        'random_state': [1]}
    alphas = np.logspace(np.log10(0.0000001), np.log10(0.01),
                         num=10)
    paramgrid = list(ParameterGrid(params))

    cv_obj = cv.cv(paramgrid)
    df_out, output, models, modelkeys, predictkeys = cv_obj.do_cv(df, xcols='wvl', ycol=[('comp', 'SiO2')],
                                                                  method='LASSO',
                                                                  yrange=[0, 100], calc_path=True, alphas=alphas)

    expected_predicts = [57.87064 , 57.868983, 57.868983, 57.868983, 57.868983, 59.315111, 59.315113, 59.315114, 59.315114, 59.315114]
    expected_output_rmsec = [18.490365, 18.490365, 18.490365, 18.490365, 18.490365,  7.042796, 6.986007,  6.967643,  6.959045,  6.953588]

    np.testing.assert_array_almost_equal(expected_predicts, np.array(df_out['predict'].iloc[0, 5:15]))
    np.testing.assert_array_almost_equal(expected_output_rmsec, np.array(output[('cv', 'RMSEC')].iloc[5:15]))

    assert output.shape == (40, 15)
    assert len(models) == 40
    assert len(modelkeys) == 40
    assert modelkeys[
               0] == 'LASSO - SiO2 - (0, 100) Alpha: 0.01, {\'copy_X\': True, \'fit_intercept\': True, \'max_iter\': 1000, \'positive\': True, \'precompute\': True, \'random_state\': 1, \'selection\': \'random\', \'tol\': 0.001}'
    assert len(predictkeys) == 80
    assert predictkeys[
               0] == '"LASSO - SiO2 - CV - Alpha:0.01 - {\'copy_X\': True, \'fit_intercept\': True, \'max_iter\': 1000, \'positive\': True, \'precompute\': True, \'random_state\': 1, \'selection\': \'random\', \'tol\': 0.001}"'

def test_cv_local_regression():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    df = df.iloc[0:20,:]  #make data set smaller so this test runs faster
    df = stratified_folds(df, nfolds=3, sortby=('comp', 'SiO2'))

    params = {'n_neighbors': [5, 6],
              'fit_intercept': [True],
              'positive': [False],
              'random_state': [1],
              'tol': [1e-2]
              }
    paramgrid = list(ParameterGrid(params))

    cv_obj = cv.cv(paramgrid)
    df_out, output, models, modelkeys, predictkeys = cv_obj.do_cv(df, xcols='wvl', ycol=[('comp', 'SiO2')],
                                                                  method='Local Regression', yrange=[0, 100],
                                                                  calc_path=False, alphas=None)

    expected_predicts = [51.30212, 54.25293063, 48.54834655, 54.18676067]
    expected_output_rmsec = [10.32151211, 10.89018268]

    np.testing.assert_array_almost_equal(expected_predicts, np.array(df_out['predict'].iloc[5, :]))
    np.testing.assert_array_almost_equal(expected_output_rmsec, np.array(output[('cv', 'RMSEC')]))
    assert output.shape == (2, 11)
    assert len(models) == 2
    assert len(modelkeys) == 2
    assert modelkeys[
               0] == 'Local Regression - SiO2 - (0, 100) {\'fit_intercept\': True, \'positive\': False, \'random_state\': 1, \'tol\': 0.01} n_neighbors: 5'
    assert len(predictkeys) == 4
    assert predictkeys[0] == '"Local Regression- CV -{\'fit_intercept\': True, \'positive\': False, \'random_state\': 1, \'tol\': 0.01} n_neighbors: 5"'


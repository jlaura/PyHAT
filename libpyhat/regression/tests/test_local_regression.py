import numpy as np
import pandas as pd
from libpyhat.examples import get_path
import libpyhat.regression.local_regression as local_regression
np.random.seed(1)


df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
def test_local_regression():
    params = {'fit_intercept': True,
              'positive': False,
              'random_state': 1,
              'tol': 1e-2,
              'max_iter': 2000,
              'selection': 'random'
              }
    model = local_regression.LocalRegression(params, n_neighbors=10)
    predictions, coeffs, intercepts = model.fit_predict(df['wvl'],df[('comp','SiO2')],df['wvl'])
    expected_rmse = 3.68281553418475
    expected_coefs = [ 0.06575656, 0.08675752, 0.04731151, 0.02209511, -0.00427306]
    expected_intercepts = [91.82150159555815, 20.29345787935364, 22.16812754981876, 47.349919072649534, 70.71488259124698]

    rmse = np.sqrt(np.average((predictions - df[('comp','SiO2')])**2))
    np.testing.assert_almost_equal(rmse,expected_rmse)
    assert np.array(coeffs).shape == (103,44)
    np.testing.assert_array_almost_equal(expected_coefs, np.array(coeffs)[10,5:10])
    assert np.array(intercepts).shape[0] == 103
    np.testing.assert_array_almost_equal(intercepts[0:5], expected_intercepts)



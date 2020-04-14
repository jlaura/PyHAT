import numpy as np
import libpyhat.transform.lra as lra
np.random.seed(1)


def test_lra():
    xresult, yresult = lra.demo()
    x_expected = [ 0.052998, -0.14058 ]
    y_expected = [ 0.053552, -0.140474]
    np.testing.assert_array_almost_equal(x_expected,xresult[0,:])
    np.testing.assert_array_almost_equal(y_expected,yresult[0,:])

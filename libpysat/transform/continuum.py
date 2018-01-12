import numpy as np
import pandas as pd
import scipy.stats as ss

from libpysat.utils.utils import continuum_correction


def regression(nx, ny):
    """
    Parameters
    ==========
    specturm : pd.series
               Pandas Series object

    nodes : list
            of nodes to be used for the continuum

    Returns
    =======
    corrected : array
                Continuum corrected array

    continuum : array
                The continuum used to correct the data

    x : array
        The potentially truncated x values
    """

    m, b, r_value, p_value, stderr = ss.linregress(nx, ny)
    c = m * nx + b
    return c


def cubic(spectrum, nodes):
    raise (NotImplemented)


correction_methods = {'linear': linear,
                      'regression': regression,
                      'cubic': cubic}

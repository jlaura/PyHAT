from . import ip_funcs

def lscc_maturity(data, **kwargs):
    """
    Name: LSCC_Maturity
    Parameter: Optical Maturity revised for hyperspectral data
    Formulation:
    Wk = weighting coefficent from table
    Sum from 1 to 46: Wk * (Rk / Rk_+1) * 10 + C
    Rationale: Based on all Lunar Soil Consortium data
    Bands: R300 - R2600

    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    raise NotImplementedError()

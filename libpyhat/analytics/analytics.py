import numpy as np

def band_minima(spectrum, low_endmember=None, high_endmember=None):
    """
    Given two end members, find the minimum observed value inclusively
    between them.

    Parameters
    ==========
    spectrum : nd.Array

    low_endmember : int
                    The low wavelength

    high_endmember : int
                    The high wavelength

    Returns
    =======
    minidx : int
             The wavelength of the minimum value

    minvalue : float
               The observed minimal value
    """

    if not low_endmember:
        low_endmember = 0
    if not high_endmember:
        high_endmember = spectrum.size
    else:
        high_endmember += 1

    slice = spectrum[low_endmember:high_endmember]
    minvalue = np.amin(slice)
    minidx = np.where(slice == minvalue)[0]

    return minidx, minvalue


def band_center(spectrum, low_endmember=None, high_endmember=None, degree=3):

    if not low_endmember:
        low_endmember = 0
    if not high_endmember:
        high_endmember = spectrum.size
    else:
        high_endmember += 1

    slice = spectrum[low_endmember:high_endmember]
    slice_indices = np.indices(slice.shape)[0]

    fit = np.polyfit(slice_indices, slice, degree)

    center_fit = np.polyval(fit, slice_indices)
    center = band_minima(center_fit)

    return center, center_fit


def band_area(spectrum, low_endmember=None, high_endmember=None):
    """
    Compute the area under the curve between two endpoints where the
    y-value <= 1.
    """
    if not low_endmember:
        low_endmember = 0
    if not high_endmember:
        high_endmember = spectrum.size
    else:
        high_endmember += 1

    slice = spectrum[low_endmember:high_endmember]
    return np.trapz(np.where(slice <= 1.0))


def band_asymmetry(spectrum, low_endmember=None, high_endmember=None):
    """
    Compute the asymmetry of an absorption feature as
    (left_area - right_area) / total_area

    Parameters
    ----------
    specturm : object

    low_endmember : int
        Bottom end of wavelengths to be obversed

    high_endmember : int
        Top end of wavelengths to be obversed

    Returns
    -------
    asymmetry : ndarray
        Array of percentage values of how asymmetrical the two halves of the spectrum are
        Where 100% is completely asymmetrical and 0 is completely symmetrical
    """

    if not low_endmember:
        low_endmember = 0
    if not high_endmember:
        high_endmember = spectrum.size
    else:
        high_endmember += 1

    slice = spectrum[low_endmember:high_endmember]

    center, _ = band_center(slice, low_endmember, high_endmember)
    area_left = band_area(slice[:center[0][0]], low_endmember, high_endmember)
    area_right = band_area(slice[center[0][0]:], low_endmember, high_endmember)
    asymmetry = abs((area_left - area_right) / (area_left + area_right))
    return asymmetry[0]

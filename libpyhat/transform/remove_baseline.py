from libpyhat.transform.baseline_code.airpls import AirPLS
from libpyhat.transform.baseline_code.als import ALS
from libpyhat.transform.baseline_code.dietrich import Dietrich
from libpyhat.transform.baseline_code.fabc import FABC
from libpyhat.transform.baseline_code.kajfosz_kwiatek import KajfoszKwiatek as KK
from libpyhat.transform.baseline_code.median import MedianFilter
from libpyhat.transform.baseline_code.polyfit import PolyFit
from libpyhat.transform.baseline_code.rubberband import Rubberband
from libpyhat.transform.baseline_code.wavelet_spline import wavelet_spline
from libpyhat.transform.baseline_code.min_spline import minimum_interp
import numpy as np

# This function applies baseline removal to the data
def remove_baseline(df, method='ALS', segment=True, params=None):
    wvls = np.array(df['wvl'].columns.values, dtype='float')
    spectra = np.array(df['wvl'], dtype='float')

    # set baseline removal object (br) to the specified method
    if method == 'ALS':
        br = ALS(**params)
    elif method == 'Dietrich':
        br = Dietrich(**params)
    elif method == 'Polyfit':
        br = PolyFit(**params)
    elif method == 'AirPLS':
        br = AirPLS(**params)
    elif method == 'FABC':
        br = FABC(**params)
    elif method == 'KK':
        br = KK(**params)
    elif method == 'Median':
        br = MedianFilter(**params)
    elif method == 'Rubberband':
        br = Rubberband(**params)
    elif method == 'Wavelet a Trous + Spline':
        br = wavelet_spline(**params)
    elif method == 'Min + Interpolate':
        br = minimum_interp(**params)
    else:
        print(f'{method} is not recognized!')
        return 0


    br.fit(wvls, spectra, segment=segment)
    df_baseline = df.copy()
    df_baseline['wvl'] = br.baseline
    df['wvl'] = df['wvl']-df_baseline['wvl']

    return df, df_baseline

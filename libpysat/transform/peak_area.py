#this function is used to bin a spectrum based on the intervals between local minima, effectively summing major peaks into individual values.
# Can be useful for spectra with many narrow peaks, such as LIBS spectra.
import scipy as sp
import numpy as np
import pandas as pd

def peak_area(df, peaks_mins_file=None):
    wvls = df['wvl'].columns.values  # get the wavelengths

    if peaks_mins_file is not None:
        peaks_mins = pd.read_csv(peaks_mins_file, sep=',')
        peaks = peaks_mins['peaks']
        mins = peaks_mins['mins']
        pass
    else:
        ave_spect = np.average(np.array(df['wvl']), axis=0)  # find the average of the spectra in the data frame
        peaks = wvls[
            sp.signal.argrelextrema(ave_spect, np.greater_equal)[0]]  # find the maxima in the average spectrum
        mins = wvls[sp.signal.argrelextrema(ave_spect, np.less_equal)[0]]  # find the maxima in the average spectrum

    wvls = df['wvl'].columns.values  # get the wavelengths

    spectra = np.array(df['wvl'])
    for i in range(len(peaks)):

        # get the wavelengths between two minima
        try:
            low = mins[np.where(mins < peaks[i])[0][-1]]
        except:
            low = mins[0]

        try:
            high = mins[np.where(mins > peaks[i])[0][0]]
        except:
            high = mins[-1]

        peak_indices = np.all((wvls > low, wvls < high), axis=0)
        # plot.plot(wvls,ave_spect)
        # plot.plot(wvls[peak_indices],ave_spect[peak_indices])
        # plot.show()
        df[('peak_area', peaks[i])] = spectra[:, peak_indices].sum(axis=1)

    return df, peaks, mins
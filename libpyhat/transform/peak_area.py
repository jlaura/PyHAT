#this function is used to bin a spectrum based on the intervals between local minima, effectively summing major peaks into individual values.
# Can be useful for spectra with many narrow peaks, such as LIBS spectra.
import scipy as sp
import numpy as np
import pandas as pd

def peak_area(df, peaks_mins_file=None):
    wvls = np.array(df['wvl'].columns.values,dtype=float)  # get the wavelengths

    if peaks_mins_file is not None:
        peaks_mins = pd.read_csv(peaks_mins_file, sep=',')
        peaks = np.array(peaks_mins[peaks_mins['type']=='peak']['wvl'],dtype='float')
        mins = np.array(peaks_mins[peaks_mins['type']=='min']['wvl'],dtype='float')
        #keep only peaks that have mins on both sides
        badpeaks = np.sum([peaks < np.min(mins), peaks > np.max(mins)], axis=0)

        if np.sum(badpeaks==1)>0:
            print('Removing unbounded peaks: '+str(peaks[badpeaks == 1]))
            peaks = peaks[badpeaks == 0]

    else:
        ave_spect = np.average(np.array(df['wvl']), axis=0)  # find the average of the spectra in the data frame
        peaks = wvls[
            sp.signal.argrelextrema(ave_spect, np.greater)[0]]  # find the maxima in the average spectrum
        mins = wvls[sp.signal.argrelextrema(ave_spect, np.less)[0]]  # find the maxima in the average spectrum

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

        peak_indices = np.all((wvls >= low, wvls < high), axis=0)

        df[('peak_area', peaks[i])] = spectra[:, peak_indices].sum(axis=1)

    return df, peaks, mins
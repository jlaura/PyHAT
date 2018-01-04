import pandas as pd
import numpy as np

from libpysat.spectral.spectra import Spectra
from libpysat.spectral.spectra import Spectrum

class m3():

    def __init__(self, path_to_img):
        self.spectra = Spectra.from_m3(path_to_file=path_to_img)

    def curvature(self):
        '''

        Returns
        ----------
        : Dataframe
          Dataframe of calculated curvature values
        '''
        wavelengths = [730, 749, 909, 1109, 1129]
        subset = self.spectra.loc[:, :, wavelengths]
        subset.wavelengths = subset.columns
        subset = subset.linear_correction()

        derived_data = (subset.iloc[:, 1] + subset.iloc[:, 2]) / (2 * subset.iloc[:, 3])
        return pd.DataFrame(index = self.spectra.index, data = derived_data).merge(self.spectra[self.spectra.metadata]._data,
                                                                                left_index = True, right_index = True)

    def fe_est(self, return_type = 'rad'):
        '''

        Parameters
        ----------
        return_type : str
                      Value for return type either in deg (Degrees) or
                      rad (Radians)

        Returns
        ----------
        : Dataframe
          Dataframe of calculated fe_est values
        '''
        wavelengths = [730, 749, 949, 970]
        subset = self.spectra.loc[:, :, wavelengths]
        subset.wavelengths = subset.columns
        subset = subset.linear_correction()

        y0 = 1.19
        x0 = 0.08

        derived_data = (17.427*(-1*(np.arctan(((subset.iloc[:, 2]/subset.iloc[:, 1])-y0)/(subset.iloc[:, 1] - x0))))) - 7.565
        if return_type == 'rad':
            return pd.DataFrame(index = self.spectra.index, data = derived_data).merge(self.spectra[self.spectra.metadata]._data,
                                                                                    left_index = True, right_index = True)
        else:
            return pd.DataFrame(index = self.spectra.index, data = derived_data * (180/np.pi)).merge(self.spectra[self.spectra.metadata]._data,
                                                                                                  left_index = True, right_index = True)
    def fe_mare_est(self):
        '''

        Returns
        ----------
        : Dataframe
          Dataframe of calculated fe mare est values
        '''
        wavelengths = [730, 749, 949, 970]
        subset = self.spectra.loc[:, :, wavelengths]
        subset.wavelengths = subset.columns
        subset = subset.linear_correction()

        derived_data = -137.97 * ((subset.iloc[:, 1] * 0.9834)+((subset.iloc[:, 2] / subset.iloc[:, 1])*0.1813)) + 57.46
        return pd.DataFrame(index = self.spectra.index, data = derived_data).merge(self.spectra[self.spectra.metadata]._data,
                                                                                left_index = True, right_index = True)

    def luceyc_amat(self):
        '''

        Returns
        ----------
        : Dataframe
          Dataframe of calculated luceyc amat values
        '''
        wavelengths = [730, 749, 949, 970]
        subset = self.spectra.loc[:, :, wavelengths]
        subset.wavelengths = subset.columns
        subset = subset.linear_correction()

        derived_data = (((subset.iloc[:, 1]-0.01)**2)+((subset.iloc[:, 2]/subset.iloc[:, 1])-1.26)**2)**(1/2)
        return pd.DataFrame(index = self.spectra.index, data = derived_data).merge(self.spectra[self.spectra.metadata]._data,
                                                                                left_index = True, right_index = True)
    # Add self to call
    def luceyc_omat(self):
        '''

        Returns
        ----------
        : Dataframe
          Dataframe of calculated luceyc omat values
        '''
        wavelengths = [730, 749, 949, 970]
        subset = self.spectra.loc[:, :, wavelengths]
        subset.wavelengths = subset.columns
        subset = subset.linear_correction()

        derived_data = (((subset.iloc[:, 1]-0.08)**2)+((subset.iloc[:, 2]/subset.iloc[:, 1])-1.19)**2)**(1/2)
        return pd.DataFrame(index = self.spectra.index, data = derived_data).merge(self.spectra[self.spectra.metadata]._data,
                                                                                left_index = True, right_index = True)

    def mare_omat(self):
        '''

        Returns
        ----------
        : Dataframe
          Dataframe of calculated mare omat values
        '''
        wavelengths = [730, 749, 949, 970]
        subset = self.spectra.loc[:, :, wavelengths]
        subset.wavelengths = subset.columns
        subset = subset.linear_correction()

        derived_data = (subset.iloc[:, 1] * 0.1813) - ((subset.iloc[:, 2]/subset.iloc[:, 1])*0.9834)
        return pd.DataFrame(index = self.spectra.index, data = derived_data).merge(self.spectra[self.spectra.metadata]._data,
                                                                                left_index = True, right_index = True)

    def tilt(self):
        '''

        Returns
        ----------
        : Dataframe
          Dataframe of calculated tilt values
        '''
        wavelengths = [890, 909, 1009, 1029]
        subset = self.spectra.loc[:, :, wavelengths]
        subset.wavelengths = subset.columns
        subset = subset.linear_correction()

        derived_data = subset.iloc[:, 1] - subset.iloc[:, 2]
        return pd.DataFrame(index = self.spectra.index, data = derived_data).merge(self.spectra[self.spectra.metadata]._data,
                                                                                left_index = True, right_index = True)

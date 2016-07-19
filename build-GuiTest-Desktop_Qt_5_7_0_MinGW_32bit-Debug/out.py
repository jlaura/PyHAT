from pysat.spectral.spectral_data import spectral_data
from pysat.regression.pls_sm import pls_sm
import pandas as pd
maskfile = "C:/Users/nicholas/Desktop/mask_minors_noise.csv"
unknowndatacsv = "C:/Users/nicholas/Desktop/lab_data_averages_pandas_format.csv"
db = "C:/Users/nicholas/Desktop/full_db_mars_corrected_dopedTiO2_pandas_format.csv"
outpath = "C:/Users/nicholas/Desktop/Output"
data = pd.read_csv(db, header=[0, 1])
data = spectral_data(data)
unknown_data = pd.read_csv(unknowndatacsv, header=[0, 1])
unknown_data = spectral_data(unknown_data)
unknown_data.interp(data.df['wvl'].columns)
data.mask(maskfile)
unknown_data.mask(maskfile)
el = 'SiO2'
nfolds_test = 6
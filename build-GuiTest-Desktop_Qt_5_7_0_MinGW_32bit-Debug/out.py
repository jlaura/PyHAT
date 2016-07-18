from pysat.spectral.spectral_data import spectral_data
from pysat.regression.pls_sm import pls_sm
import pandas as pd
maskfile = "C:/Users/nicholas/.bash_history"
unknowndatacsv = "C:/Users/nicholas/.gitconfig"
db = "C:/Users/nicholas/lifecynical.swf"
outpath = "C:/Users/nicholas/VirtualBox VMs"
data = pd.read_csv(db, header=[0, 1])
data = spectral_data(data)
unknown_data = pd.read_csv(unknowndatacsv, header=[0, 1])
unknown_data = spectral_data(unknown_data)
unknown_data.interp(data.df['wvl'].columns)
data.mask(maskfile)
unknown_data.mask(maskfile)

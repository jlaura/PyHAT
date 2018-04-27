#this function multiplies all the spectra in a data frame by a vector.
import numpy as np
import pandas as pd
def multiply_vector(df, vectorfile):
    df_spectra = df['wvl']
    # TODO: check to make sure wavelengths match before multiplying

    vector = np.array(pd.read_csv(vectorfile, sep=',', header=None))[:, 1]
    if df_spectra.shape[1] == vector.shape[0]:
        df['wvl'] = df_spectra.multiply(vector, axis=1)
    else:
        print('Vector is not the same size as the spectra!')
    return df
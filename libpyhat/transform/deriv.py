import copy
import numpy as np
#Take the derivative of a spectrum
def deriv(df):
    new_df = copy.deepcopy(df)
    wvls = np.array(df['wvl'].columns.values,dtype=float)
    new_df['wvl'] = df['wvl'].diff(axis=1) / wvls
    new_df = new_df.drop(('wvl', df['wvl'].columns.values[0]), axis=1)
    return new_df
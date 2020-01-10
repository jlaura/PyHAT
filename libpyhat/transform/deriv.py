#Take the derivative of a spectrum
def deriv(df):
    new_df = df.copy()
    wvls = df['wvl'].columns.values
    new_df['wvl'] = df['wvl'].diff(axis=1) / wvls
    new_df = new_df.drop(('wvl', df['wvl'].columns.values[0]), axis=1)
    return new_df
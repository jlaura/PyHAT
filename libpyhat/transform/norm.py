import numpy as np
import pandas as pd

# This function normalizes specified ranges of the data by their respective sums
def norm(df, ranges, col_var='wvl'):
    df_tonorm = df[col_var]
    top_level_cols = df.columns.levels[0]
    top_level_cols = top_level_cols[top_level_cols != col_var]
    df_other = df[top_level_cols]
    cols = df_tonorm.columns.values

    df_sub_norm = []
    allind = []
    for i in ranges:
        # Find the indices for the range
        ind = (np.array(cols, dtype='float') >= i[0]) & (np.array(cols, dtype='float') <= i[1])
        # find the columns for the range
        normcols = cols[ind]
        # keep track of the indices used for all ranges
        allind.append(ind)
        # normalize over the current range
        df_sub_norm.append(norm_total(df_tonorm[normcols]))

    # collapse the list of indices used to a single array
    allind = np.sum(allind, axis=0)
    # identify columns that were not used by where the allind array is less than 1
    cols_excluded = cols[np.where(allind < 1)]
    # create a separate data frame containing the un-normalized columns
    df_masked = df_tonorm[cols_excluded]
    # combine the normalized data frames into one
    df_norm = pd.concat(df_sub_norm, axis=1)

    # make the columns into multiindex
    df_masked.columns = [['masked'] * len(df_masked.columns), df_masked.columns]
    df_norm.columns = [[col_var] * len(df_norm.columns), df_norm.columns.values]

    # combine the normalized data frames, the excluded columns, and the metadata into a single data frame
    df_new = pd.concat([df_other, df_norm, df_masked], axis=1)
    df = df_new

    return df

def norm_total(df):
    df = df.div(df.sum(axis=1), axis=0)
    return df
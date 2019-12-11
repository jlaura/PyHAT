# -*- coding: utf-8 -*-

import numpy as np
from sklearn import cross_validation

#This function assigns spectra to folds randomly, but keeps spectra with the same value in a user-defined column together.
#This ensures that multiple spectra of the same target end up in the same fold

def random(df, nfolds=5, seed=10, groupby=None):
    df['Folds'] = 'None'  # Create an entry in the data frame that holds the folds
    foldslist = np.array(df['Folds'])
    if groupby == None:  # if no column name is listed to group on, just create random folds
        n = len(df.index)
        folds = cross_validation.KFold(n, nfolds, shuffle=True, random_state=seed)
        i = 1
        for train, test in folds:
            foldslist[test] = 'Fold' + str(i)
            i = i + 1

    else:
        # if a column name is provided, get all the unique values and define folds
        # so that all rows of a given value fall in the same fold
        # (this is useful to ensure that training and test data are truly independent)
        unique_inds = np.unique(df[groupby])
        folds = cross_validation.KFold(len(unique_inds), nfolds, shuffle=True, random_state=seed)
        foldslist = np.array(df['Folds'])
        i = 1
        for train, test in folds:
            tmp = unique_inds[test]
            tmp_full_list = np.array(df[groupby])
            tmp_ind = np.in1d(tmp_full_list, tmp)
            foldslist[tmp_ind] = 'Fold' + str(i)
            i = i + 1

    df['Folds'] = foldslist
    return df

# This function divides the data up into a specified number of folds, using sorting
# to try to get folds that look similar to each other.
# This function keeps spectra with the same value in a user-defined column together.
# This ensures that multiple spectra of the same target end up in the same fold
def stratified_folds(df, nfolds=5, sortby=None):
    df[('meta', 'Folds')] = np.NaN  # Create an entry in the data frame that holds the folds
    df.sort_values(by=sortby, inplace=True)  # sort the data frame by the column of interest
    uniqvals = np.unique(df[sortby])  # get the unique values from the column of interest

    # assign folds by stepping through the unique values
    fold_num = 1
    for i in uniqvals:
        ind = df[sortby] == i  # find where the data frame matches the unique value
        df.set_value(df.index[ind], ('meta', 'Folds'), fold_num)
        # Inrement the fold number, reset to 1 if it is greater than the desired number of folds
        fold_num = fold_num + 1
        if fold_num > nfolds:
            fold_num = 1

    # sort by index to return the df to its original order
    df.sort_index(inplace=True)

    return df
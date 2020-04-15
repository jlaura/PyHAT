import numpy as np
from sklearn import model_selection

#This function assigns spectra to folds randomly, but keeps spectra with the same value in a user-defined column together.
#This ensures that multiple spectra of the same target end up in the same fold

def random(df, col, nfolds=5, seed=10):
    df[('meta','Folds')] = 'None'  # Create an entry in the data frame that holds the folds
    foldslist = np.array(df[('meta','Folds')])
    folds = model_selection.GroupKFold(n_splits=nfolds)
    i = 1
    for train, test in folds.split(df,groups=df[col]):
        foldslist[test] = i
        i = i + 1

    df[('meta','Folds')] = foldslist
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
        df.at[df.index[ind], ('meta', 'Folds')] = fold_num
        # Inrement the fold number, reset to 1 if it is greater than the desired number of folds
        fold_num = fold_num + 1
        if fold_num > nfolds:
            fold_num = 1

    # sort by index to return the df to its original order
    df.sort_index(inplace=True)
    return df

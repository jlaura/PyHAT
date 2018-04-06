# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:16:11 2016
This function is used to run cross validation 
to help choose the optimal number of components. Folds are stratified 
according to a user-specified column

@author: rbanderson
"""
import warnings

import numpy as np
# from sklearn.linear_model import RANSACRegressor as RANSAC
import pandas as pd
from libpysat.regression.regression import regression
from sklearn.cross_validation import LeaveOneLabelOut
from sklearn.grid_search import ParameterGrid
from sklearn.linear_model import ElasticNetCV, LassoCV, RidgeCV, OrthogonalMatchingPursuitCV, LarsCV, LassoLarsCV, enet_path, ElasticNet
from sklearn.linear_model.base import _pre_fit
from sklearn.utils.validation import check_X_y, check_array
warnings.filterwarnings('ignore')
import time
import copy

def RMSE(ypred, y):
    return np.sqrt(np.mean((np.squeeze(ypred) - np.squeeze(y)) ** 2))

def ENet(X, y, X_holdout, y_holdout, alphas, paramgrid, colname = 'CV', intercept_in_colname = False):
    #make a copy of the parameters before popping things off
    copy_params = copy.deepcopy(paramgrid)
    fit_intercept = copy_params.pop('fit_intercept')
    normalize = copy_params.pop('normalize')
    precompute = copy_params.pop('precompute')
    copy_X = copy_params.pop('copy_X')

    # this code adapted from sklearn ElasticNet fit function, which unfortunately doesn't accept multiple alphas at once
    X, y = check_X_y(X, y, accept_sparse='csc',
                     order='F', dtype=[np.float64, np.float32],
                     copy=copy_X and fit_intercept,
                     multi_output=True, y_numeric=True)
    y = check_array(y, order='F', copy=False, dtype=X.dtype.type,
                    ensure_2d=False)

    #this is the step that gives the data to find intercept if fit_intercept is true.
    X, y, X_offset, y_offset, X_scale, precompute, Xy = _pre_fit(X, y, None, precompute, normalize,
                                                                 fit_intercept, copy=False)
    #do the path calculation, and tell how long it took
    print('Calculating path...')
    start_t = time.time()
    path_alphas, path_coefs, path_gaps = enet_path(X, y, alphas=alphas,
                                                   **copy_params)
    dt = time.time() - start_t
    print('Took ' + str(dt) + ' seconds')

    #create some empty arrays to store the result
    y_pred_holdouts = np.empty(shape=(len(alphas),len(y_holdout)))
    intercepts = np.empty(shape=(len(alphas)))
    rmses = np.empty(shape=(len(alphas)))
    cvcols = []
    for j in list(range(len(path_alphas))):

        coef_temp = path_coefs[0, :, j]

        if fit_intercept:
            coef_temp = coef_temp / X_scale
            intercept = y_offset - np.dot(X_offset, coef_temp.T)
        else:
            intercept = 0.

        y_pred_holdouts[j,:] = np.dot(X_holdout, path_coefs[0, :, j]) + intercept
        intercepts[j] = intercept
        rmses[j] = RMSE(y_pred_holdouts[j,:], y_holdout)
        if intercept_in_colname:
            cvcols.append(('predict','"Elastic Net - '+ colname+' - Alpha:' + str(path_alphas[j]) + ' - Intercept:' +
                 str(intercept) + '-' + str(paramgrid) + '"'))
        else:
            cvcols.append(('predict','"Elastic Net - ' + colname + ' - Alpha:' + str(path_alphas[j]) + ' - ' + str(paramgrid) + '"'))

    return path_alphas, path_coefs, intercepts, y_pred_holdouts, rmses, cvcols

class cv:
    def __init__(self, params,progressbar = None):
        if progressbar is not None:
            self.progress = progressbar
        print(params)
        self.paramgrid = list(ParameterGrid(params))  # create a grid of parameter permutations
        #self.paramgrid = ParameterGrid(params).param_grid
    def do_cv(self, Train, xcols='wvl', ycol=('comp', 'SiO2'), method='PLS',
              yrange=[0, 100], calc_path = False, alphas = None):


        try:
            cv_iterator = LeaveOneLabelOut(
            Train[('meta', 'Folds')])  # create an iterator for cross validation based on the predefined folds
        except:
            print('***No folds found! Did you remember to define folds before running cross validation?***')

        models = []
        modelkeys = []

        for i in list(range(len(self.paramgrid))):
            print(self.paramgrid[i])
            # create an empty output data frame to serve as template
            output_tmp = pd.DataFrame()
            # add columns for RMSEC, RMSECV, and RMSE for the folds
            output_tmp['RMSEC'] = 0
            output_tmp['RMSECV'] = 0
            for f in np.array(range(cv_iterator.n_unique_labels)) + 1:
                output_tmp['Fold ' + str(f)] = 0
            #fill in the output template based on the current permutation parameters
            for k in self.paramgrid[i].keys():
                output_tmp.at[0,k]=self.paramgrid[i][k]
            if alphas is not None:
                output_tmp = pd.concat([output_tmp]*len(alphas))
                output_tmp['alphas'] = alphas

            model = regression([method], [yrange], [self.paramgrid[i]])
            modelkey = "{} - {} - ({}, {}) {}".format(method, ycol[0][-1], yrange[0], yrange[1], self.paramgrid[i])

            rmsecv_folds_tmp = np.empty(shape=(0))  # Create empty array to hold RMSECV for each fold
            alphas_out = np.empty(shape=(0))
            cvcols_all = np.empty(shape=(0))

            pass
            foldcount = 1
            for train, holdout in cv_iterator:  # Iterate through each of the folds in the training set
                  # ycol[-1]+'_cv_'+method+'_param'+str(i))  #create the name of the column in which results will be stored

                cv_train = Train.iloc[train]  # extract the data to be used to create the model
                cv_holdout = Train.iloc[holdout]  # extract the data that will be held out of the model

                if calc_path:
                    if method == 'Elastic Net':

                        # get X and y data
                        X = cv_train[xcols]
                        y = cv_train[ycol]

                        #do the path calculation
                        path_alphas,\
                        path_coefs,\
                        intercepts,\
                        y_pred_holdouts,\
                        fold_rmses,\
                        cvcols = ENet(X, y, cv_holdout[xcols], cv_holdout[ycol], alphas, self.paramgrid[i])

                        output_tmp['Fold '+str(foldcount)] = fold_rmses
                        for n in list(range(len(path_alphas))):
                            Train.set_value(Train.index[holdout], cvcols[n], y_pred_holdouts[n])



                else:
                    cvcols = [('predict', '"'+method+'-CV-' + str(self.paramgrid[i]) + '"')]
                    #fit the model and predict teh held-out data
                    model.fit(cv_train[xcols], cv_train[ycol])
                    if model.goodfit:
                        y_pred_holdout = model.predict(cv_holdout[xcols])
                    else:
                        y_pred_holdout = cv_holdout[ycol] * np.nan
                    #add the predictions to the appropriate column in the training data
                    Train.set_value(Train.index[holdout], cvcols[0], y_pred_holdout)
                    #append the RMSECV to the list
                    output_tmp['Fold '+str(foldcount)]=RMSE(y_pred_holdout, cv_holdout[ycol])

                foldcount = foldcount + 1

            #now that all the folds have been held out and predicted, calculate the overall rmsecv and add it to the output
            rmsecv = []
            for col in cvcols:
                rmsecv.append(RMSE(Train[col], Train[ycol]))
            output_tmp['RMSECV']=rmsecv


            #fit the model on the full training set using the current settings
            if calc_path:
                X = Train[xcols]
                y = Train[ycol]

                path_alphas, \
                path_coefs, \
                intercepts, \
                ypred_train, \
                rmsec_train, \
                cols = ENet(X, y, X, y, alphas, self.paramgrid[i], intercept_in_colname=True, colname = 'Cal')


                for n in list(range(len(path_alphas))):
                    Train[cols[n]]=ypred_train[n] #put the training set predictions in the data frame
                    pass
                output_tmp['RMSEC'] = rmsec_train
            else:
                model.fit(Train[xcols], Train[ycol])
                #if the fit is good, then predict the training set
                if model.goodfit:
                    models.append(model)
                    modelkeys.append(modelkey)
                    ypred_train = model.predict(Train[xcols])

                else:
                    ypred_train = Train[ycol] * np.nan

                #add the calibration predictions to the appropriate column
                calcol = ('predict', '"'+method + '-Cal-' + str(self.paramgrid[i])+'"')
                Train[calcol] = ypred_train
                #append the RMSEC for the current settings to the cllection of all RMSECs
                output_tmp['RMSEC'] = RMSE(ypred_train, Train[ycol])


            try:
                output = pd.concat((output, output_tmp))
            except:
                output = output_tmp
            pass

        # rmsecv_folds = np.array(rmsecv_folds)
        # for i in list(range(len(rmsecv_folds[0, :]))):
        #     label = 'Fold' + str(i)
        #     output[label] = rmsecv_folds[:, i]
        #make the columns of the output data drame multi-indexed
        cols = output.columns.values
        cols = [('cv', i) for i in cols]
        output.columns = pd.MultiIndex.from_tuples(cols)

        return Train, output, models, modelkeys

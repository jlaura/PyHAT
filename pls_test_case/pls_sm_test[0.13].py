"""
Created on Tue May 10 12:09:29 2016

@author: rbanderson
"""
###################################################
# import all preprocessors
###################################################
from pysat.spectral.spectral_data import spectral_data
from pysat.regression.pls_sm import pls_sm
import pandas as pd

###################################################
# General setup
###################################################
outpath = r'C:\Users\User\Desktop\Output'
db = r"C:\Users\User\Desktop\full_db_mars_corrected_dopedTiO2_pandas_format.csv"
unknowndatacsv = r"C:\Users\User\Desktop\lab_data_averages_pandas_format.csv"
maskfile = r"C:\Users\User\Desktop\mask_minors_noise.csv"

###################################################
# Spectral setup
# spectral analysis data
###################################################
data = pd.read_csv(db, header=[0, 1])
data = spectral_data(data)
unknown_data = pd.read_csv(unknowndatacsv, header=[0, 1])
unknown_data = spectral_data(unknown_data)
unknown_data.interp(data.df['wvl'].columns)

data.mask(maskfile)
unknown_data.mask(maskfile)

###################################################
# Normalizing Data and getting Ranges
# range3: equivalent to norm3
# range1: equivalent to norm1
###################################################
def get_ranges(r0, r1, r2, r3):
    return [(r0, r1), (r1, r2), (r2, r3)]
ranges3 = get_ranges(0, 350, 470, 1000)
ranges1 = [(0, 1000)]

data3 = data
data3.norm(ranges3)
unknown_data3 = unknown_data
unknown_data3.norm(ranges3)

data1 = data
data1.norm(ranges1)
unknown_data1 = unknown_data
unknown_data1.norm(ranges1)

###################################################
# nfolds: the number of folds to divide data into to extract an overall test set
# testfold: which fold to use as the overall test set
# nfolds_cv: Number of folds for CV
# testfold_cv: Which fold to use as the test set for cross validation
# Cross Validation
###################################################
el = 'SiO2'
nfolds_test = 6
testfold_test = 4
nfolds_cv = 5
testfold_cv = 3

###################################################
# Composition Ranges
# These are the composition ranges for the submodels
# nc: max number of components
###################################################

compranges = [[-20, 50], [30, 70], [60, 100], [0, 120]]
nc = 20

###################################################
# remove a test set to be completely excluded from CV
# and used to assess the final blended model
###################################################
data3.stratified_folds(nfolds=nfolds_test, sortby=('meta', el))
data3_train = data3.rows_match(('meta', 'Folds'), [testfold_test], invert=True)
data3_test = data3.rows_match(('meta', 'Folds'), [testfold_test])

data1.stratified_folds(nfolds=nfolds_test, sortby=('meta', el))
data1_train = data1.rows_match(('meta', 'Folds'), [testfold_test], invert=True)
data1_test = data1.rows_match(('meta', 'Folds'), [testfold_test])

###################################################
# Create the models here in order: Low, Mid, High, Full
# The full model will be used as a references to determine which submodel is appropriate
# The Full model will be computed last
###################################################
ncs = [7, 7, 5, 9]
traindata = [data3_train.df, data3_train.df, data1_train.df, data3_train.df]
testdata = [data3_test.df, data3_test.df, data1_test.df, data3_test.df]
unkdata = [unknown_data3.df, unknown_data3.df, unknown_data1.df, unknown_data3.df]

sm = pls_sm()

sm.fit(traindata, compranges, ncs, el, figpath=outpath)

predictions_train = sm.predict(traindata)

predictions_test = sm.predict(testdata)

blended_train = sm.do_blend(predictions_train, traindata[0]['meta'][el])

blended_test = sm.do_blend(predictions_test)

###################################################
# Create all the Plots in Outpath
###################################################
sm.final(testdata[0]['meta'][el],
         blended_test,
         el=el,
         xcol='Ref Comp Wt. %',
         ycol='Predicted Comp Wt. %',
         figpath=outpath)

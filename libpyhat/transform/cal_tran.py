from libpyhat.transform.lra import low_rank_align as LRA
import numpy as np
from sklearn.cross_decomposition import CCA, PLSRegression

#apply calibration transfer to a data set to transform it to match a different data set.

class cal_tran:
    def __init__(self, params):

        self.algorithm_list = ['None',
                               'PDS - Piecewise Direct Standardization',
                               'DS - Direct Standardization',
                               'PDS-PLS - PDS using Partial Least Squares',
                               'LASSO DS',
                               'Ratio']
        self.method = params.pop('method')

        self.ct_obj = None

        if self.method == 'PDS - Piecewise Direct Standardization':
            self.ct_obj = piecewise_ds(**params)
        if self.method == 'None':
            self.ct_obj = no_transform()
        if self.method == 'PDS-PLS - PDS using Partial Least Squares':
            self.ct_obj = piecewise_ds(**params)
        if self.method == 'DS - Direct Standardization':
            self.ct_obj = ds(**params)
        if self.ct_obj==None:
            print('Method '+self.method+' not recognized!')

    def derive_transform(self,A,B):
        self.ct_obj.derive_transform(A,B)

    def apply_transform(self,C):
        return self.ct_obj.apply_transform(C)

class no_transform:
    def derive_transform(self,A,B):
        return
    def apply_transform(self,C):
        return C

class piecewise_ds:
    def __init__(self, win_size=5, pls=False, nc=5):
        self.pls = pls
        self.win_size=win_size
        self.pls_nc = nc
        assert win_size % 2 == 1, "Window size must be odd."
        self.padding = (win_size - 1) / 2

    def derive_transform(self, A, B):
        A = np.array(A)
        B = np.array(B)
        assert A.shape==B.shape, "Input matrices must be the same shape."
        self.B_shape = B.shape
        n_feats = B.shape[1]
        coefs = []
        for i in range(n_feats):
            row = np.zeros(n_feats)
            start = int(max(i-self.padding,0))
            end = int(min(i+self.padding,n_feats-1)+1)
            if self.pls:
                model = PLSRegression(n_components=self.pls_nc,scale=False)
                try:
                    model.fit(A[:,start:end],B[:,i])
                    row[start:end] = model.coef_.ravel()
                except:
                    pass
            else:
                row[start:end]=np.dot(np.linalg.pinv(A[:,start:end]),B[:,i])

            coefs.append(row)

        self.proj_to_B = np.array(coefs).T

    def apply_transform(self,C):
        C_transformed = np.dot(C, self.proj_to_B)
        return C_transformed

class ds:
    def __init__(self,fit_intercept=False):
        self.fit_intercept = fit_intercept

    def get_working_data(self,data):
        if self.fit_intercept:
            if len(data.shape)==1:
                data = np.reshape(data,(1,data.shape[0]))
            working = np.hstack((data, np.ones((data.shape[0], 1))))
        else:
            working = np.copy(data)
        return working

    def derive_transform(self, A, B):
        assert A.shape[0] == B.shape[0], (
            'Input matrices must have the same number of rows (i.e. samples).')
        working_A = self.get_working_data(A)
        self.proj_to_B = np.dot(np.linalg.pinv(working_A), B)

    def apply_transform(self, C):
        working_C = self.get_working_data(C)
        C_transformed = np.dot(working_C, self.proj_to_B)
        return C_transformed

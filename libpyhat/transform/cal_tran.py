from libpysat.transform.lra import low_rank_align as LRA
import numpy as np
#apply calibration transfer to a data set to transform it to match a different data set.

def cal_tran(df, refdata, matchcol_ref, matchcol_transform, method, methodparams):
    C_matrix = []
    col = np.array([j.upper() for j in df[('meta', matchcol_transform)]])
    col_ref = np.array([j.upper() for j in refdata[('meta', matchcol_ref)]])
    for i in col:
        matches = np.where(col_ref == i, 1, 0)
        C_matrix.append(matches)

    C_matrix = np.transpose(np.array(C_matrix))

    if method == 'LRA - Low Rank Alignment':
        refdata_trans, transdata_trans = LRA(np.array(refdata['wvl']), np.array(df['wvl']), C_matrix,
                                             methodparams['d'])
        refdata_trans = pd.DataFrame(refdata_trans)
        transdata_trans = pd.DataFrame(transdata_trans)
        pass
    if method == 'PDS Piecewise Direct Standardization':
        print('PDS not implemented yet!!')

    pass
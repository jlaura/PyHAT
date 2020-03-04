import numpy as np
import scipy.sparse as sparse
from sklearn.cluster import AffinityPropagation

def lfda(x, y, r=None, metric="plain", knn=5):
    # metric can be: "orthonormalized", "plain", "weighted"
    x = np.matrix(x).getT()
    y = np.matrix(y).getT()
    d = np.size(x,0) # number of rows
    n = np.size(x,1) # number of columns

    # if no dimension reduction requested, set r to d
    if r == None:
        r = d

    tSb = np.zeros((d, d))
    tSw = np.zeros((d, d))

    # compute the optimal scatter matrices in a classwise manner

    for value in set(y.flatten()):
        Xc = x[:, y == value]
        nc = np.size(Xc,1) # number of columns

        # determine local scaling for locality-preserving projection
        Xc2 = np.matrix(np.power(Xc.sum(axis=0), 2))

        # calculate the distance, using a self-defined repmat function that's the same
        # as repmat() in Matlab
        distance2 = np.matlib.repmat(Xc2, nc, 1) + np.matlib.repmat(Xc2.getT(), 1, nc) - 2 * np.multiply(Xc.getT(), Xc)

        '''
        NOTE: This is the Affinity Matrix code used in the R Package. Can compare later.
        getAffinityMatrix <- function(distance2, knn, nc) {
              sorted <- apply(distance2, 2, sort) # sort for each column by distance
              if (dim(sorted)[1] < knn + 1) {
                stop("knn is too large, please try to reduce it.")
              }
              kNNdist2 <- t(as.matrix(sorted[knn + 1, ])) # knn-th nearest neighbor
              sigma <- sqrt(kNNdist2)

              localscale <- t(sigma) %*% sigma
              # use only non-zero entries in localscale since this will be used in the denominator
              # to calculate the affinity matrix
              flag <- (localscale != 0)

              # define affinity matrix - the larger the element in the matrix, the closer two data points are
              A <- mat.or.vec(nc, nc)
              A[flag] <- exp(-distance2[flag] / localscale[flag])
              return(A)
            }
        '''
        # Get affinity matrix
        A = AffinityPropagation().fit(distance2).affinity_matrix_
        Xc1 = np.matrix(Xc.sum(axis=1))
        G = np.multiply(Xc, np.matlib.repmat(A.sum(axis=0), 1, d)) * Xc.getT() - np.multiply(np.multiply(Xc, A), Xc.getT())
        tSb = tSb + (G / n) + np.multiply(Xc, Xc.getT()) * (1 - nc / n) + np.multiply(Xc1, (Xc1.getT() / n))
        tSw = tsW + G / nc

    X1 = x.sum(axis=1)
    tSb = tSb -np.multiply(X1, X1.getT() / n) - tSw
    tSb = (tSb + tSb.getT()) / 2
    tSw = (tSw + tSw.getT()) / 2

     # find generalized eigenvalues and normalized eigenvectors of the problem

    if(r == d):
        # without dimensionality reduction
        eigTmp = np.multiply(np.linalg.solve(tSw,inv(np.matrix(tSw))), tSb)
    else:
        # dimensionality reduction (select only the r largest eigenvalues of the problem)
        eigVal, eigVec = sparse.linalg.eigs(A= np.multiply(np.linalg.solve(tSw,inv(np.matrix(tSw))), tSb), k=r)

    # Based on metric return other values
    # options to require a particular type of returned transform matrix
    if metric == "orthonormalized":
        q, r = np.linalg.qr(np.linalg.qr(eigVec), mode="complete")
        Tr = q
    elif metric == "weighted":
        Tr = eigVec * np.matlib.repmat(np.sqrt(eigVal).getT(), d, 1)
    elif metric == "plain":
        Tr = eigVec
    else:
        "Invalid Metric Type. Using 'plain'"
        Tr = eigVec

    Z = np.multiply(Tr.getT(), x).getT()

    return Tr, Z

def predict_lfda(T, newdata=None, type="raw"):
    if(newdata == "None"):
        raise NoDataError('You must provide data to be used for transformation.')
    if(type != "raw"):
        raise WrongTypeerror("Types other than 'raw' are currently unavailable.")

    newdata = np.matrix(newdata)

    transformMatrix = T

    result = np.multiply(newdata, transformMatrix)

    return result

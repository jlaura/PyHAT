import argparse
from scipy.optimize import lsq_linear

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('x')
    parser.add_argument('y')
    return parser.parse_args()

def lsqnn(x, y, thirdInput=False):
    if ($ARGC < 2):
        print("\nNonnegative least squares fitting\n")
        print("lsqnn(X,y) returns A such that X*A best approximates y\n")
        print(" by minimizing the sum of squares of the residuals,\n")
        print(" subject to the constraint that all elements of A are >= 0.\n")
        print(" That is, A for which sum((y_i - X_i*A_i)^2) is minimized.\n")
        print("The data input X should have m rows, n columns, and 1 plane.\n")
        print("The test input y should have m rows, 1 column, and 1 plane.\n")
        print("Optional third input controls output mode\n")
        print(" If $3 is 1 (or omitted), will print summary and return structure\n")
        print("  with errors and fitted spectrum, in addition to calculated\n")
        print("  coefficients.\n")
        print(" If $3 is 0, will only return structure with coefficients\n")
        print(" This means that the format of the output depends on $3.\n")
        print("This function uses an algorithm outlined in Lawson & Hanson 1974\n")
        print("Note that this function is set to stop after 100 iterations and\n")
        print(" return its best solution if no convergence is reached by then.\n")
        print("S.Marshall 10-31-2010\n\n") # Some revisions to comments, 12-07-2010

        return str.encode("0")

    # Unlike the earlier version, this needs to work such that the matrix passed to lsq doesn't have any columns of zeros
    # Add option to display strings if verbose >= 1?
    # But this could slow it down, as it would require an if check for each string - is there a way to avoid that?

    eE = np.array(x)
    ef = np.array(y)
    eEd = eE.shape # dim gives [columns, rows, planes]
    efd = ef.shape

    if(thirdInput):
        if(thirdInput == 0 or thirdInput == 1):
            iem = str.encode(thirdInput)
        else:
            return "Error: Invalid Third Input"
    else:
        iem = str.encode("1")

    if(efd[1,1,1] != 1 or eEd[3,1,1] != 1 or efd[3,1,1] != 1 or eEd[2,1,1] != efd[2,1,1]):
        return "Dimension Error!"

      print("\nInputs OK; proceeding with lsqnn...\n") # For debugging

      # Descriptions of procedure from: Lawson, C. L., and R. J. Hanson.
      # Solving Least Squares Problems, pp. 160-161 (Problem NNLS). Prentice-Hall, 1974.
      # Problem NNLS:
      # Initially given m-by-n matrix E, integers m and n, and m-vector f
      # 23.10: Algorithm NNLS(E,m,n,f,x,w,z,P,Z)
      em = eEd[2,1,1] # Rows (number of samples in each spectrum)
      en = eEd[1,1,1] # Columns (number of end members)
      ieps = 5.e-8 # Tolerance
      # 1. Set P = null, Z = {1,2,...,n}, x = 0
      iZ = np.arrange(1, en)
      iP =  np.zeros((en,), dtype=int) # Column vector; will hold indices for which values are positive
      ix =  np.zeros((en,), dtype='double')
      #printf("Step 1 complete; defined m, n, Z, P, x\n")
      ill = sum(np.where(iP > 0))
      # List of number of positive end members at beginning of each iteration (or after each iteration, if you count the first element as zero)
      ici = 0 # Number of iterations
      ig = str.encode('2') # Control switch - step to complete next, since algorithm is not a simple loop
      # Stops after 100 iterations; change that number if necessary
      # Note that Davinci only checks the criteria for a loop (e.g. ig < 12) at the beginning of each iteration (not continuously).
      #  So this loop has some intermediate checks for ig, in order to avoid unnecessary computations.
      while (ici < 100 and ig < 12):
          ici += 1 # Increment number of iterations
          print("\nBeginning iteration {} of main loop\n".format(ici))
          ill = np.append(ill, sum(np.where(iP > 0))), axis=x)
          if (ig < 6):
              np.transpose(eE)
              iw = np.dot(np.transpose(eE), (ef - np.dot(eE, ix)))
              if ((max(iZ) <= 0) or (max(iw*(iZ > 0)) <= 0)):
                  print("\nStep 12: Computation complete; breaking from main loop\n")
                  ig = str.encode("12") # Break
          if (ig < 6):
              ict = maxpos(iw*double(iZ > 0)) # That should handle the j dom Z part as quickly as possible
              ict = ict[2]
              iP[1,ict] = ict # Move index
              iZ[1,ict] = 0
          if (ig < 12):
              ict = 1
              iEPn = 0 # Number of end members in EP
              for (ict = 1; ict <= en; ict++):
                  if (iP[1,ict] > 0):
                      if (iEPn > 0):
                          iEP = cat(iEP, eE[ict,], axis=x)
                          iEPj = cat(iEPj, ict, axis=x)
                      else:
                          iEP = eE[ict,]
                          iEPj = ict # Tracks indices in iEP
               iEPn++

# TODO: USING SCIKIT LSQ_LINEAR FOR DAVINCI LSQ ---MAY NEED TO BE CHANGED---
lsq_linear(A, b, bounds=(iEP, ef), lsmr_tol='auto', verbose=1)
izP = lsq(iEP, ef, 0) # Final zero to skip calculation of errors

# Be careful, since the indices returned here do not match those of the original (input) E
#printf(" lsq complete; max component value is %f; re-arranging indices\n", max(izP))
ict = 1
iz = np.zeroes(1, en, 1, dtype=float32)
for i in range(1, iEPn):
    iz[1,iEPj[ict]] = izP[1,ict]

if (min(iz*(iP > 0) + (iZ > 0)) > 0.0):
    ix = iz
    ig = "" # And go to step 2
else:
    ict = 1 # Counter
    iq = 0 # Will store index of interest
    ia = double(1e7) # Will store value at that index
    itv = ia # Temporary variable for ict-th value of x/(x - z)
    for ict in range(1, int(en)):
        if ((iz[1,ict] <= 0.) && (iP[1,ict] > 0)):
            itv = ix[1,ict]/(ix[1,ict] - iz[1,ict])

            if (itv < ia):
                iq = ict # Remember this index
                ia = itv # And this value
    ix = ix + ia*(iz - ix)
    ict = 1
    for ict in range(1, int(en)):
        if (abs(ix[1,ict]) <= ieps):
            iP[1,ict] = 0
            iZ[1,ict] = ict
    ig = "6"


if (iem == 0):
    return ix
else:
    printf("\n%d iterations; %d significant (nonzero) end members\n", ici, sum(iP > 0))
    oA = ix
    printf("Errors in fitted spectrum:\n")
    oYf = mxm($1, oA) # Fit y
    oYfe = abs(oYf - $2) # Absolute errors in fit y
    oMAE = avg(oYfe)
    printf("Mean absolute error: %f\n", oMAE)
    oRMSE = sqrt(avg(oYfe*oYfe)) # RMS error
    printf("RMS error: %f\n", oRMSE)
    omaxE = max(oYfe)
    printf("Maximum absolute error: %f\n", omaxE)
    return {"A": oA,
            "Yfit": oYf,
            "MAE":oMAE,
            "RMSE":oRMSE,
            "maxE":omaxE,
            "np":ill[2:]}

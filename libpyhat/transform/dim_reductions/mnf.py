import pandas as pd
import pysptools.noise as pn
import pysptools.eea as eea
import numpy as np

# filepath = "/home/tthatcher/Documents/data/full_db_mars_corrected_dopedTiO2_pandas_format.csv"
# df = pd.read_csv(filepath)

a = np.zeros((100, 100,3))
a[:,:,0] = 255

b = np.zeros((100, 100,3))
b[:,:,1] = 255

c = np.zeros((100, 200,3))
c[:,:,2] = 255

img = np.vstack((c, np.hstack((a, b))))

# MNF
MNF_OBJ = pn.MNF()
MNF_OBJ.apply(img)
r = MNF_OBJ.get_components(1)
print(r)

# PPI
ppi_obj = eea.PPI()
x = ppi_obj.extract(img, 2)
print(x)


# N-FINDR
n_findr = eea.NFINDR()
x = n_findr.extract(img, 2)
print(x)

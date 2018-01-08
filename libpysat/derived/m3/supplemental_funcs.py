import numpy as np

def curv_func(bands):
    band0, band1, band2 = bands[1:4]

    return (band0 + band1) / (2 * band2)

def fe_est_func(bands):
    band0, band1 = bands[1:3]

    y0 = 1.19
    x0 = 0.08

    return (17.427*(-1*(np.arctan(((band1/band0)-y0)/(band0 - x0))))) - 7.565

def fe_mare_est_func(bands):
    band0, band1 = bands[1:3]

    return -137.97 * ((band0 * 0.9834)+((band1 / band0)*0.1813)) + 57.46

def luceyc_amat_func(bands):
    band0, band1 = bands[1:3]

    return (((band0-0.01)**2)+((band1/band0)-1.26)**2)**(1/2)

def luceyc_omat_func(bands):
    band0, band1 = bands[1:3]

    return (((band0-0.08)**2)+((band1/band0)-1.19)**2)**(1/2)

def mare_omat_func(bands):
    band0, band1 = bands[1:3]

    return (band0 * 0.1813) - ((band1/band0)*0.9834)

def tilt_func(bands):
    band0, band1 = bands[1:3]

    return band0 - band1

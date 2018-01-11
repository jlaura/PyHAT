from libpysat.derived.m3 import pipe

def mustard(data, wavelengths):
    red = pipe.bdi1000(data, wavelengths)
    green = pipe.bdi2000(data, wavelengths)
    blue = pipe.reflectance4(data, wavelengths)

    return [red, green, blue]

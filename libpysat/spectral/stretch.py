import numpy as np

def linear_stretch(array, clip = 2.0):
    minimum = array.min()
    maximum = array.max()
    newmin = minimum * ((100.0-clip)/100.0)
    newmax = maximum * ((100.0-clip)/100.0)
    return (array - minimum) * ((newmax - newmin) / (maximum - minimum)) + newmin

def standard_deviation_stretch(array, sigma = 2.0):
    array_mean = array.mean()
    array_standard_deviation = np.std(array)
    newmin = array_mean - (array_standard_deviation * sigma)
    newmax = array_mean + (array_standard_deviation * sigma)
    array  = np.subtract(array, newmin)
    print(array)
    array *= 1.0 / (newmax - newmin)
    return array

def inverse_stretch(array):
    maximum = array.max()
    array -= maximum
    return abs(array)

def histequ_stretch(array):
    '''Equalize the histogram'''

    def _gethist_cdf(array, num_bins=128):
        '''
        This function calculates the cumulative distribution function of a given array and requires that both the input array and the number of bins be provided.

        Returns: cumulative distribution function, bins
        '''
        hist, bins = np.histogram(array.flatten(), num_bins, density=False)
        cdf = hist.cumsum()
        cdf = cdf ** 0.5
        cdf = 256 * cdf / cdf[-1] #This needs to have a dtype lookup (16bit would be 2**16-1)
        return cdf, bins

    cdf, bins = _gethist_cdf(array)
    shape = array.shape
    #interpolate
    array = np.interp(array,bins[:-1],cdf)
    #reshape
    return array.reshape(shape)

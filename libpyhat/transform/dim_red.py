from bin.jade import JADE
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold.t_sne import TSNE
from sklearn.manifold.locally_linear import LocallyLinearEmbedding
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import NMF
#This function does dimensionality reduction on a data frame full of spectra. A number of different methos can be chosen

def dim_red(df, xcol, method, params, kws, load_fit=None, ycol=None):
    xdata = df[xcol]

    if method == 'PCA':
        do_dim_red = PCA(*params, **kws)
    if method == 'FastICA':
        do_dim_red = FastICA(*params, **kws)
    if method == 't-SNE':
        do_dim_red = TSNE(*params, **kws)
    if method == 'LLE':
        do_dim_red = LocallyLinearEmbedding(*params, **kws)
    if method == 'JADE-ICA':
        do_dim_red = JADE(*params, **kws)
    if method == 'LDA':
        do_dim_red = LinearDiscriminantAnalysis(*params, **kws)
    if method == 'NMF':
        add_const = kws.pop('add_constant')
        do_dim_red = NMF(*params, **kws)

    if load_fit:
        do_dim_red = load_fit
    else:
        if method != 't-SNE':
            if ycol != None:
                #find the multi-index that matches the specified single index
                ycol_tuple = [a for a in df.columns.values if ycol in a][0]
                ydata = df[ycol_tuple]
                do_dim_red.fit(xdata,ydata)
            else:
                if method == 'NMF':
                    if add_const:
                        if xdata.min().min()<0:
                            xdata = xdata-xdata.min().min()
                        else:
                            print('Data is already positive: no need to add a constant!')
                    check_positive(xdata)
                do_dim_red.fit(xdata)
            dim_red_result = do_dim_red.transform(xdata)
        else:
            dim_red_result = do_dim_red.fit_transform(xdata)

    for i in list(range(1, dim_red_result.shape[
                               1] + 1)):  # will need to revisit this for other methods that don't use n_components to make sure column names still mamke sense
        df[(method, method+'-'+str(i))] = dim_red_result[:, i - 1]

    return df, do_dim_red

def check_positive(data):
    if data.min().min()<0:
        print('NMF will not work with data containing negative values!')

import numpy as np
import pandas as pd

def mask(df,maskfile):
    """
    This function applies a mask to LIBS spectra to remove unwanted regions of the spectrum

    Parameters
    ----------
    maskfile = string specifying the path to the mask file.
    Mask file should have three comma-separated columns:
    column 0 = name of feature being masked
    column 1 = minimum wavelength to be masked for each feature
    column 2= maximum wavelength to be masked for each feature

    The first row of the file should contain column headings

    Returns
    df :
    """

    df_spectra=df['wvl'] #extract just the spectra from the data frame
    metadata_cols=df.columns.levels[0]!='wvl'  #extract just the metadata
    metadata=df[df.columns.levels[0][metadata_cols]]
    
    mask = pd.read_csv(maskfile, sep=',')  #read the mask file
    tmp=[]
    for i in mask.index:
        tmp.append((df['wvl'].columns>=mask.ix[i,'min_wvl'])&(df['wvl'].columns<=mask.ix[i,'max_wvl']))

    #combine the indexes for each range in the mask file into a single masking vector and use that to mask the spectra
    masked=np.any(np.array(tmp),axis=0)
    spectcols=list(df_spectra.columns)  #get the list of columns in the spectra dataframe
    for i,j in enumerate(masked):  #change the first level of the tuple from 'wvl' to 'masked' where appropriate
        if j==True:
            spectcols[i]=('masked',spectcols[i])
        else:
            spectcols[i]=('wvl',spectcols[i])
    df_spectra.columns=pd.MultiIndex.from_tuples(spectcols) #assign the multiindex columns based on the new tuples
    df=pd.concat([df_spectra,metadata],axis=1) #merge the masked spectra back with the metadata
    
    return df 
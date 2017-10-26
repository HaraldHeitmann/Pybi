import pandas as pd
from matplotlib import pyplos as plt
from sklearn import preprocessing

def plot_df(df,col,cat=None,linestyle=None,marker=None):
    '''df must be a pandas DataFrame,
    col and cat should be in df.columns and
    cat is a categorical variable
    outputs None, but generates a figure with the corresponding plots
    TO-DO: pass *args and **kwargs to the plot function
    '''
    if col not in df.columns:
        return
    if cat is None:
        df[col].plot()
    else:
        options=df[cat].unique()
        for opt in options:
            df[col][df[cat]==opt].plot(label=opt,linestyle=linestyle,marker=marker)
            plt.legend()

def plot_df_multiple(df,cols,cat=None,linestyle=None,marker=None,alpha=None):
    '''df must be a pandas DataFrame,
    cols is a list of columns of df
    cat is a column of categorical variables
    outputs None, but generates a figure with the corresponding plots
    TO-DO: pass *args and **kwargs to the plot function
    '''
    if len(set(cols)-set(df.columns))>0:
        print 1
        return
    if cat is None:
        df[cols].plot()
    else:
        options=df[cat].unique()
        for col in cols:
            for opt in options:
                df[col][df[cat]==opt].plot(label=opt,linestyle=linestyle,marker=marker,alpha=alpha)
                plt.legend()
            plt.show()


# data mangling 
from sklearn import preprocessing
def binarize(dataframe,column):
    '''dataframe is a pandas dataframe, and column must
    be a column name of the dataframe. the column values should be
    categorical.
    If the dataframe has n rows and the column has m different values,
    it outputs a numpy array of shape (n,m), which can be used to create
    a dataframe
    '''
    OHE = preprocessing.OneHotEncoder()
    return None





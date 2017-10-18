import pandas as pd
from matplotlib import pyplos as plt


def plot_df(df,col,cat=None,linestyle=None,marker=None):
    '''df must be a pandas DataFrame, 
    col and cat should be in df.columns and
    cat is a categorical variable
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
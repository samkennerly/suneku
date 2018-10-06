"""
Data visualization tools.
"""
from functools import wraps

COLORMAP = 'nipy_spectral_r'
FIGSIZE = (9,4)
LEGEND = {'bbox_to_anchor':(1,1), 'loc':'upper left'}

def restyle(func):
    """ function: Apply default style to a plotting function. """

    @wraps(func)
    def newfunc(*args,**kwargs):
        kwargs.setdefault('cmap',COLORMAP)
        figsize = kwargs.pop('figsize',FIGSIZE)

        fig = func(*args,**kwargs).legend(**LEGEND).get_figure()
        fig.set_size_inches(FIGSIZE)
        fig.tight_layout()

        return fig

    return newfunc

@restyle
def area(data,**kwargs):
    """ Figure: Area chart of columns in a DataFrame. """
    return data.plot.area(**kwargs)

@restyle
def bar(data,stacked=True,**kwargs):
    """ Figure: Stacked bar chart of Series or DataFrame. """
    return data.plot.bar(stacked=stacked,**kwargs)

@restyle
def hist(data,bins=42,stacked=True,**kwargs):
    """ Figure: Histogram(s) of Series or DataFrame. """
    return data.plot.hist(bins=bins,stacked=stacked,**kwargs)

@restyle
def line(data,**kwargs):
    """ Figure: Line plot of Series or DataFrame. """
    return data.plot.line(**kwargs)

@restyle
def quantile(data,q=(),**kwargs):
    """ Figure: Quantiles for each row of DataFrame. """
    q = list(q) or [0,0.05,0.25,0.50,0.75,0.95,1]
    data = data.quantile(q=q,axis=1).transpose()
    data.columns = data.columns.astype(str)

    return data.plot.line(**kwargs)




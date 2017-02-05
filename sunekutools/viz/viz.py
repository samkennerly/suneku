'''
Utility functions and classes for data vizualization
'''
import sunekutools as st


def log_hist(s,nBins=27,**kwargs):
    '''
    Show histogram with logarithmic x-axis.
    Caution: Only positive non-null values will be included.
    INPUTS:
      s         Series
      nBins     uint: number of bins
      kwargs    other keyword arguments for Series.hist() function
    '''

    # Get base-10 log of [s]. Replace any problematic values with
    # minimum positive element of [s]
    log_s = st.safelog(s,10)

    # Figure out where to draw bins
    bins = st.np.logspace(log_s.min(),log_s.max(),num=nBins)

    # Plot histogram
    s.hist(bins=bins,**kwargs).set_xscale('log')

def hist_stack(predictor,target,**kwargs):
    '''
    Show histogram of [predictor] colored by [target].
    Similar to the diagonal elements of Seaborn's pairplot().
    [predictor] and [target] must have the same index.
    INPUTS:
        predictor   Series
        target      Series which is categorical or can be converted to one
        **kwargs    optional keyword arguments for DataFrame.hist()
    '''

    # If [target] cannot be converted to categorical, then crash
    target = target.astype('category')

    # If names are missing, then use generic ones
    if predictor.name is None:
        predictor.name = 'Predictor'
    if predictor.index.name is None:
        predictor.index.name = 'Index'
    if target.name is None:
        target.name = 'Target'
        
    # Join [predictor] and [target]. Reshape so that each category gets a column.
    df = st.pd.concat([predictor,target],axis=1)
    df.index.name = predictor.index.name
    df = df.pivot_table(index=df.index,columns=target.name,values=predictor.name)
    
    # Plot stacked histogram
    df.plot.hist(stacked=True,title=predictor.name,**kwargs)

def hist_stack_multi(data_matrix,target_name,predictor_names=[],**kwargs):
    '''
    Show hist_stack() for multiple columns of [data_matrix].
    If no [predictors] input, then everything but target will be plotted.
    INPUTS:
        data_matrix     DataFrame with predictors, target, and possibly other columns
        target_name     string name of column to use as target
        predictors      optional list of string names of columns to use as predictors
        **kwargs        optional keyword arguments for DataFrame.hist()
    '''

    if len(predictor_names)==0:
        predictor_names = [ x for x in data_matrix.columns if x != target_name ]

    # Force target to be categorical, or else crash
    target = data_matrix[target_name].astype('category')

    for col in predictor_names:
        predictor = data_matrix[col]
        try:
            hist_stack(predictor,target,**kwargs)
        except:
            continue

def quantile_flow(df,**kwargs):
    '''
    For each row, find min, max, and some quantiles in between. Plot results.
    INPUTS
        df          DataFrame (typically where each column is a TimeSeries)
        **kwargs    keyword arguments for pandas.plot() function
    '''

    Q = st.pd.DataFrame(index=df.index.copy())
    Q['Max'] = df.max(axis=1)
    Q['Q90'] = df.quantile(0.90,axis=1)
    Q['Q75'] = df.quantile(0.75,axis=1)
    Q['Med'] = df.median(axis=1)
    Q['Q25'] = df.quantile(0.25,axis=1)
    Q['Q10'] = df.quantile(0.10,axis=1)
    Q['Min'] = df.min(axis=1)

    Q.plot(color=['0.75','m','b','g','y','r','0.75'],**kwargs)




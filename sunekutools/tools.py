'''
Convenience functions and classes for data exploration.

Even if you never use them, these tools might be handy
for remembering how to do common tasks. 
'''

# Shorthand imports
import pandas as pd
import numpy as np
import datetime as dt
import seaborn

# Other imports
import os
import json
import glob
import random
import subprocess
from scipy import stats



# Generic convenience functions

def byteprint(x,format='utf-8'):
    ''' Convert bytes object to string and print it '''
    print( x.decode(format) )

def cls():
    ''' Clear screen (in an interactive Python session) '''
    os.system('clear')

def dictprint(d):
    ''' Print a dictionary in human-readable form '''
    keys = d.keys()
    width = max([ len(key) for key in keys])
    for key in keys:
        printstr = '{:<' + str(width) + '}'
        print(printstr.format(key), d[key])

def is_folder(full_path):
    ''' Check whether a string is a filename or foldername '''
    if os.path.isfile(full_path):
        return False
    elif os.path.isdir(full_path):
        return True
    else:
        raise ValueError("Cannot find file or folder named %s" % full_path)

def list2string(l,separator=','):
    ''' Convert a list (or list-like object) into a string '''
    return ''.join( str(x) + separator for x in l )[0:-1]

def listjoin(list_of_lists,mode='outer'):
    '''
    Join several lists as if they were sets.
    CAUTION: Sets remove duplicates and do not preserve order!
    '''
    s = set()
    if mode == 'outer':
        s = s.union(*list_of_lists)
    elif mode == 'inner':
        s = s.intersection(*list_of_lists)
    return list(s)

def makefolder(foldername):
    ''' Make a new folder, unless one with that name exists '''
    if not os.path.isdir(foldername):
        os.makedirs(foldername)

def mode(s):
    ''' Return mode of array '''
    return stats.mode(s).mode[0]

def overlap(a,b):
    ''' Show count of union, intersection, and differences of two list-like objects '''
    aa = set(a).copy()
    bb = set(b).copy()
    a_and_b = aa.intersection(bb)
    a_or_b = aa.union(bb)
    a_not_b = aa - bb    
    b_not_a = bb - aa
    print( "%s distinct elements in either A or B" % len(a_or_b) )
    print( "%s distinct elements in both A and B" % len(a_and_b) )
    print( "%s distinct elements in A, but not in B" % len(a_not_b) )
    print( "%s distinct elements in B, but not in A" % len(b_not_a) )

def readjson(filename):
    ''' Load a dict stored with SKTools.savejson() '''
    with open(filename,'r') as f:
        d = json.load(f)
    return d

def recentfile(generic_fname,date=dt.date.today()):
    '''
    Return most recent filename up to and including selected date.
    Files must include date in YYYYMMDD format.
    EXAMPLE:
      >>> recentfile('20160101','/science/data/spam_????????.csv')
      '/science/data/spam_20151230.csv'
    INPUTS:
      generic_fname     string: full path with ???????? instead of date
      date              optional datetime, date, or string: cutoff date
    OUTPUTS:
      most_recent_fname string: filename
    '''

    # Force date into string YYYYMMDD format.
    date_ymd = pd.to_datetime(date).strftime('%Y%m%d')

    # Figure out filename on cutoff date
    cutoff_fname = generic_fname.replace('????????',date_ymd)

    # Find the most recent file
    if os.path.isfile(cutoff_fname):
        most_recent_fname = cutoff_fname
        timeprint( "Found file %s" % cutoff_fname )
    else:
        valid_fnames = glob.glob(generic_fname)
        valid_fnames = [ x for x in valid_fnames if x<= cutoff_fname ]
        most_recent_fname = sorted(valid_fnames)[-1]
        timeprint()
        print( '*** Cannot find %s' % cutoff_fname )
        print( '    Using older %s instead.\n' % most_recent_fname )

    return most_recent_fname

def run_command(command,verbose=True):
    ''' Run a shell command as a subprocess '''
    if verbose:
        print(command)
        output = subprocess.check_output(command.split(),universal_newlines=True)
        print(output)
    else:
        subprocess.run(command.split(),check=True)

def safestring(s):
    ''' Replace space with _ and remove all other non-alphanumeric characters '''
    s = s.replace(' ','_')
    return ''.join( x for x in s if (x.isalnum() or x=='_') )

def savejson(d,filename):
    '''
    Save a dict to a JSON file.
    Caution: strings become unicode and tuples become lists.
    Caution: order of list might not be preserved.
    '''
    with open(filename,'w') as f:
        json.dump(d,f)

def sqlstring(l):
    ''' Convert list into SQL-readable string '''
    
    # Cast everything in list as string wrapped by single quotes
    s = [ "'%s'" % x for x in l ]
    
    # Combine everything into a single string separated by commas
    s = ','.join(s)
    
    # Wrap string in parentheses
    s = '(%s)' % s
    
    return s

def timeprint(*args,**kwargs):
    ''' Display human-readable message along with time and date '''
    stamp = str(dt.datetime.now())
    print( stamp[0:19], *args, **kwargs )

def ymd(day):
    ''' Convert a datetime object to a string YYYYMMDD '''
    return day.strftime('%Y%m%d')



# PANDAS convenience functions

def afew(x,nSamples=10):
    ''' Grab a few random elements from a list, Series, or DataFrame '''
    nElements   = len(x)
    nSamples    = min(nSamples,nElements)
    Indices     = random.sample(range(nElements),nSamples)
    Indices.sort()
    if isinstance(x,pd.Series):         xSmall = x.iloc[Indices]
    elif isinstance(x,pd.DataFrame):    xSmall = x.iloc[Indices]
    else:                               xSmall = [ x[i] for i in Indices ]
    return xSmall

def badrows(df,cols=None):
    '''
    Return only the rows of a DataFrame with at least one NaN.
    Use 'cols' to restrict NaN detection to specific rows.
    '''
    if cols is None:
        cols = df.columns
    fBadRow = df[cols].isnull().any(axis=1)
    BadRows = df.loc[fBadRow,:]
    return BadRows

def blank2nan(s):
    ''' Convert an object of length 0 to Numpy NaN '''
    if len(s)==0:
        return np.nan
    else:
        return s

def categorize(s,left=None,right=None,nCats=5):
    '''
    Convert numeric Series into categories, e.g. (0,1], (1,2], ...
    WARNING: Values outside (left,right] will be converted to NaN's.
      INPUTS:
        s       numeric Series
        left    left endpoint (not included)
        right   right endpoint [included]
        nCats   number of categories to use
    '''
    if left is None:
        left = s.dropna().min()
    if right is None:
        right = s.dropna().max()
    bin_edges   = np.linspace(left,right,nCats+1)
    cats        = pd.cut(s,bins=bin_edges)
    return cats

def cleanpct(df):
    ''' Show percentage of non-null values in each column of a DataFrame '''
    return (df.notnull().mean()*100).round()

def datefail(x):
    ''' Return True iff pd.to_datetime() fails to parse x '''
    try:
        pd.to_datetime(x)
        return False
    except:
        return True

def datesafe(x):
    ''' Convert to datetime if possible; else mark NaT '''
    try:
        return pd.to_datetime(x)
    except:
        return pd.NaT

def dfinfo(x,nRows=5):
    ''' Print info about a DataFrame or Series '''
    print( 'Object type:     ', type(x) )
    print( 'Index type:      ', type(x.index) )
    print( 'Shape:           ', x.shape )
    try:
        for col in x.columns:
            print( col, type(x[col].iat[0]) )
    except:
        pass

def dfnumeric(df,cols):
    '''
    Convert column(s) of a DataFrame to numeric type.
    NOTE: [cols] must be a list
    '''
    df[cols] = df[cols].apply(pd.to_numeric)
    return df

def dfretype(df,cols,new_type):
    '''
    Convert column(s) of a DataFrame to another type.
    NOTE: [cols] must be a list
    '''
    df[cols] = df[cols].astype(new_type)
    return df

def dfretype_multi(df,coltypes):
    '''
    Convert columns of a DataFrame to types indicated in type_dict, e.g.
    coltypes = { 'datetime':['StartDate','StopDate'], 'int':['Revenue'] }
    '''

    for k in coltypes.keys():
        kvars = coltypes[k]
        try:

            if (k.lower() == 'datetime'):
                df = dftime(df,coltypes[k])

            elif (k.lower() == 'numeric'):
                df = dfnumeric(df,coltypes[k])

            elif (k.lower() == 'category'):
                for col in coltypes[k]:
                    df[col] = df[col].astype('category')

            else:
                df = dfretype(df,coltypes[k],k)

        except:

            msg = "Could not convert %s to %s" % (coltypes[k],k)
            raise ValueError(msg)

    return df

def dropsort(df,sort_cols):
    ''' Sort rows and columns. Delete index column. '''
    return df.sort_values(sort_cols).reset_index(drop=True).sort_index(axis=1)

def dftime(df,cols):
    '''
    Convert column(s) of a DataFrame to datetime64 objects.
    NOTE: [cols] must be a list.
    '''
    df[cols] = df[cols].apply(pd.to_datetime)
    return df

def groupstats(df,col,groupby,dropna=True,fast=False):
    '''
    Calculate some common aggregation stats for a column of a DataFrame.
    INPUTS
      df        DataFrame
      col       string: column of data to be aggregated
      groupby   string or list: name(s) of columns to use for grouping
      fast      bool: skip slower calculations
    '''

    # Drop invalid columns and warn user?
    if dropna:
        fBad = df[col].isnull()
        groups = df.loc[~fBad].groupby(groupby)[col]
        nBad = fBad.sum()
        if nBad > 0:
            print( "*** groupstats() ignored %s rows with invalid '%s' value" % (nBad,col) )
    else:
        groups = df.groupby(groupby)[col]

    # Apply some common aggregation functions to each group
    agg             = pd.DataFrame()
    agg['Count']    = groups.count()
    agg['Min']      = groups.min()
    if not fast:
        agg['Q25']      = groups.quantile(0.25)
    agg['Mean']     = groups.mean()
    agg['Median']   = groups.median()
    if not fast:
        agg['Mode']     = groups.apply(mode)
        agg['Q75']      = groups.quantile(0.75)
    agg['Max']      = groups.max()

    return agg

def homogenize(s,default_value=np.nan):
    ''' Replace all entries in a Series with last not-null value '''

    valid_values = s.dropna()
    if len(valid_values) > 0:
        last_valid_value = valid_values.iat[-1]
    else:
        last_valid_value = default_value
    new_s = pd.Series(last_valid_value,index=s.index)        
    return new_s

def keepcols(df,col_names):
    '''
    Only keep certain columns of a DataFrame, if they exist.
    INPUTS
        df          DataFrame
        col_names   list or set of strings
    OUTPUTS
        df          DataFrame
    '''

    col_names       = set(col_names)
    available_cols  = set(df.columns)
    col_names = list( available_cols.intersection(col_names) )

    return df[col_names]

def key2value(df,key,value):
    '''
    Extract a key-value lookup Series from a DataFrame.
    If multiple values exist for each key, then take the *last* one
    '''
    return df[[key,value]].groupby(key).last()[value]

def mad(s):
    ''' Calculate median absolute deviation '''

    mean        = s.mean()
    deviation   = s - mean

    return deviation.abs().median()

def moretime(x,periods,freq='D'):
    ''' Extend a Series or DataFrame with Timestamp indices into the future '''

    last_time = x.index.max()
    new_times = pd.date_range(last_time,periods=periods+1,freq=freq)
    new_times = new_times[1:]       # Don't duplicate x.index.max()
    if isinstance(x,Series):
        new_data = Series(index=new_times)
    else:
        new_data = DataFrame(index=new_times)

    return x.append(new_data)

def nullpct(s):
    '''
    Figure out what % of values in a Series or DataFrame are null.
    Series input => float output. Dataframe input => Series output.
    '''

    nancount = s.isnull().sum()

    return 100 * nancount / float(len(s))

def pairinterp(x0,x1,y0,y1,step):
    '''
    Given two points in a plane, interpolate some points between them.
    Caution: if step is not an integer, then endpoint may be duplicated.
    '''

    y = Series([y0,y1],index=[x0,x1])
    x = np.arange(x0,x1,step)
    x = np.append(x,x1)
    y = y.reindex(x)

    return y.interpolate(method='index')

def pct(s):
    ''' Find mean of a (typically Boolean) series and show as a percent '''
    return round( 100 * s.mean() )
    
def periodavg(s,freq='M'):
    ''' Average a TimeSeries over periods of selected frequency '''

    groups = s.groupby(pd.TimeGrouper(freq)).mean()
    groups.index = groups.index.to_period(freq)

    return groups

def perioderror(modelval,trueval,freq='M'):
    ''' Calculate some error measures over periods of selected frequency '''

    error   = modelval - trueval
    df      = dict()
    df['MeanDeviation']     = periodavg(error,freq)
    df['MeanAbsDeviation']  = periodavg(error.abs(),freq)
    df['RootMeanSquare']    = np.sqrt(periodavg(error*error,freq))
    df      = DataFrame(df)

    return df

def read_excel_multi(filename):
    '''
    Read multiple sheets from a single Excel file.
    Return a dict of form { sheet_name : DataFrame }.
    '''

    with pd.ExcelFile(filename) as xl:
        sheetz = { name : xl.parse(name) for name in xl.sheet_names }

    return sheetz

def readgz(full_path):
    ''' Import a gzip'd CSV file as a DataFrame '''
    return pd.io.parsers.read_csv(full_path,compression='gzip')

def relabel(s,label_dict):
    '''
    Replace values in a Series with some other values.
    label_dict should be of form { old_value:new_value }.
    '''

    for key, val in label_dict.items():
        s = s.replace(to_replace=key,value=val)

    return s

def safelog(s,base=None):
    '''
    Return logarithm of s, but replace any 0's with minimum nonzero element of s.
    If no base input, then use natural logarithm. (This is slightly faster.)
    '''

    s_new           = s.copy()
    fPosi           = s_new > 0
    s_new[~fPosi]   = s_new[fPosi].min()
    s_new           = np.log(s_new)
    if base is not None:
        s_new = (1.0 / np.log(base) ) * s_new

    return s_new

def stripframe(df,indexcol,valuecol):
    ''' Make a Series from 2 columns from a DataFrame. Use one as index and other as data. '''

    s = df[valuecol].copy()
    s.index = df[indexcol].copy()

    return s

def standardize(s):
    ''' Adjust a numeric Series to have mean 0 and variance 1 '''
    return ( s - s.mean() ) / s.std()

def standardize_robust(s):
    ''' Like standardize(), but with median 0 and median abs deviation 1 '''

    s_new = s - s.median()
    s_new /= s_new.abs().median()

    return s_new



# Custom decorators

def nansafe(defval=np.nan):
    '''
    Try to do func(). Return NaN if it fails.
    func() can accept multiple arguments, but not keyword args.
    Use defval to set a different placeholder for bad values.
    Example:
        @nansafe(defval='BAD_VALUE')
        def first_3_letters(word):
            return word[0:3]
    '''

    def wrapper(func):
        def try_function(*args):
            try:
                return func(*args)
            except:
                return defval
        return try_function

    return wrapper



# Custom classes

class PandaBox():
    '''
    PandaBox objects are containers for storing pandas Series and DataFrame objects.
    PandaBoxes can save themselves to a single HDF5 file and reload from that file.
    PandaBoxes can also copy themselves and self-diagnose missing data.
    I often use PandaBox as a base class for custom data-manipulation classes.
    '''

    def __repr__(self):
        ''' String representation: show table names '''
        
        msg         = "PandaBox object containing: "
        var_names   = sorted(vars(self).keys())

        for x in var_names:
            msg += x + ', '
        return msg[0:-2]

    def show_clean(self,exclude=None):
        '''
        Show percentage of non-null values in each column of each table.
        To exclude tables, input a list of names to exclude.
        '''
        
        print( )
        table_names = self.__dict__.keys()
        
        if exclude is not None:
            table_names = [ x for x in table_names if x not in exclude ]
        
        for name in table_names:
            table = self.__dict__[name]
            print( "[%s] percent clean:" % name )
            print( cleanpct(table) )
            print( )

    def save(self,output_file,verbose=True):
        '''
        Save all Series and DataFrame objects to one HDF5 file.
        WARNING: Overwrites any existing file with same name!
        '''

        all_tables = self.__dict__

        # Overwrite file if it already exists
        if os.path.exists(output_file):
            os.remove(output_file)

        # Save each Series and DataFrame in this PandaBox
        for name, table in all_tables.items():

            if isinstance(table,pd.DataFrame):
                format = 'table'
            elif isinstance(table,pd.Series):
                format = 'fixed'
            else:
                continue

            if verbose:
                timeprint( "Saving [%s] to %s" % (name,output_file) )

            table.to_hdf(output_file,name,format=format)

    @classmethod
    def load(cls,filename,verbose=True):
        '''
        Create a new object with tables loaded from an HDF5 file.
        CAUTION: Tables must be stored at root level within file.
        '''

        newbox = cls()

        # Open HDF5 filestore object
        with pd.HDFStore(filename) as store:

            # CAUTION: This is a kludgy way to get all table names,
            # not including weird stuff like meta-tables.
            table_names = [ x.split('/')[1] for x in store.keys() ]
            table_names = list(set(table_names))

            # Assume each key is a table name and load that table
            for name in table_names:
                if verbose:
                    timeprint( "Loading [%s] from %s" % (name,filename) )
                try:
                    newbox.__dict__[name] = store.get(name)
                except:
                    raise LookupError( "Could not load [%s] from %s" % (name,filename) )

        return newbox

    def copy(self):
        ''' Make a copy of this object '''

        new_copy            = self.__class__()
        new_copy.__dict__   = self.__dict__.copy()

        return new_copy




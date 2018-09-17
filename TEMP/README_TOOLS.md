# sunekutools

This custom Python package consists of utility functions in [tools.py](https://github.com/samkennerly/suneku/blob/master/sunekutools/tools.py) and these sub-packages:

* **[ml](https://github.com/samkennerly/suneku/tree/master/sunekutools/ml)** for machine learning and related tools
* **[viz](https://github.com/samkennerly/suneku/tree/master/sunekutools/viz)** for visualizing data

Many of the functions in [tools.py](https://github.com/samkennerly/suneku/blob/master/sunekutools/tools.py) aren't really necessary, but I often use them as a quick-reference guide when I forget how to do something like "use `os.makedirs()` to make a new folder"

## demo notebooks

For each `.py` module in `sunekutools`, there is an `.ipynb` notebook demonstrating how to use that module.


## importing sunekutools

If you're using a [suneku lab](https://github.com/samkennerly/suneku/tree/master/labs), `sunekutools` can be imported just like any other Python package:
```python
import sunekutools as st
```
Importing `sunekutools` will automatically import everything in [tools.py](https://github.com/samkennerly/suneku/blob/master/sunekutools/tools.py), including:

- several packages like `pandas` and `seaborn`
- convenience functions like `makefolder()` and `timeprint()`
- the `PandaBox()` class for storing collections of Series and DataFrame objects

These packages and convenience functions can be called like so:

```python
st.timeprint("Hello, world!")                          # print timestamp and message
array_of_ints = st.np.random.randint(0,100,size=[5,5]) # use NumPy to make an array of random integers
st.seaborn.heatmap(array_of_ints)                      # use Seaborn to draw a heatmap
my_box = st.PandaBox()                                 # create a new PandaBox object
```

Note that `numpy` is abbreviated `np`. See the top of [tools.py](https://github.com/samkennerly/suneku/blob/master/sunekutools/tools.py) for all packages and abbreviations.


## importing other Python packages

Calling packages with the `st` prefix helps avoid redundant imports. But if you want, you can still do this:
```python
import sunekutools as st
import numpy as np
```
This example would make `np` and `st.np` two different names for `numpy`.


## the `PandaBox()` class

sunekutools includes the `PandaBox()` class for storing a collection of Series and DataFrame objects.

I routinely need to load several tables from various sources: SQL databases, S3 buckets, third-party APIs, etc. The raw tables often require some (possibly complicated) cleaning, joining, and other transformations. By storing tables in a `PandaBox`, I can save pre-processed data to a single [HDF5 file](https://support.hdfgroup.org/HDF5/whatishdf5.html) like so:
```
import sunekutools as st
Data = st.PandaBox()
Data.Energy    = st.pd.read_csv('/suneku/data/Energy.csv',index_col='Year').fillna(0)
Data.ZonalTemp = st.pd.read_csv('/suneku/data/ZonalTempAnomaly.csv',index_col='Year')
Data.Merged    = st.pd.merge(Data.Energy,Data.ZonalTemp,how='left',left_index=True,right_index=True)
Data.save('/suneku/data/Box.h5')
```
Instead of re-loading and re-processing several tables, I can just use
```
Data = st.PandaBox.load('/suneku/data/Box.h5')
```
to recover my data with (mostly!) correct indexing, formatting, and datatypes.

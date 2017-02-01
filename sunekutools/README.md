# UNDER CONSTRUCTION

# sunekutools

This custom Python package consists of utility functions in [tools.py](https://github.com/samkennerly/suneku/blob/master/sunekutools/tools.py) and these sub-packages:

* **[ml](https://github.com/samkennerly/suneku/tree/master/sunekutools/ml)** for machine learning and related tools
* **[viz](https://github.com/samkennerly/suneku/tree/master/sunekutools/viz)** for visualizing data

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

**Caution:** Be careful using *star imports*:
```python
from st import *      # not recommended
```
Star imports rely on the `__all__` lists within each module's `__init__.py` file. Because `sunekutools` is often under construction, maintaining accurate `__all__` lists is difficult.

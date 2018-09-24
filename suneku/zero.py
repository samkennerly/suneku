"""
Top-level constants and utility functions.
"""
from pathlib import Path

from pandas import Series, Timestamp, to_datetime

REPO = Path(__file__).resolve().parent.parent

def echo(msg=''):
    """ None: Print timestamped message. """
    print(isonow()[:19].replace('T',' '),msg)

def fullpath(path_or_str=''):
    """
    Path: Expand path relative to current working directory.
    Accepts string or pathlib.Path input. String can include '~'.
    Does not expand absolute paths. Does not resolve dots.
    """
    path = Path(path_or_str).expanduser()
    if not path.is_absolute():
        path = Path.cwd().resolve()/path

    return path

def hello(obj):
    """ None: Print short description of any Python object. """
    print(type(obj).__name__,obj.__doc__,sep='\n')

def isonow():
    """ str: Current UTC date and time in ISO-format microseconds. """
    return Timestamp.utcnow().tz_localize(None).isoformat()

def zulutime(t):
    """
    Timestamp: UTC time from string or timelike input.
    OR Series: Series of UTC Timestamps from Series input.
    OR DatetimeIndex: UTC Timestamps from iterable input.
    """
    t = to_datetime(t,cache=True,utc=True)
    t = (t.dt if isinstance(t,Series) else t).tz_localize(None)

    return t




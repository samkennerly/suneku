#!/usr/bin/env python
"""
Test script: print some messages.
"""
import sys
import sunekutools as st

print('Python:',sys.version)
print('Repository:',st.REPO)
print('Working directory:',st.fullpath())

st.hello(st)

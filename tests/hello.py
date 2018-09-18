#!/usr/bin/env python
"""
Test script: print some messages.
"""
from sys import implementation as imp
from sunekutools import echo, fullpath, REPO

echo()
print("Hello, {}!".format(imp.name))
print('Version:','.'.join(map(str,imp.version)))
print('Repository:',REPO)
print('Working directory:',fullpath())
print()

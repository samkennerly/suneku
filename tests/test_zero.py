"""
Unit tests for suneku.zero module.
"""
from pathlib import Path

from suneku import *

class TestZero:

    def test_echo(self):
        echo('This is a test. This is only a test.')

    def test_fullpath(self):
        assert Path.home() < fullpath('~/not/a/real/path')

    def test_hello(self):
        hello(hello)

    def test_isonow(self):
        print(isonow())

    def test_zulutime(self):
        print(zulutime(isonow()))




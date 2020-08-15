# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
import os

import pytest

from fsoopify import Path

on_win = pytest.mark.skipif(os.name != 'nt', reason="only run on windows")
on_unix = pytest.mark.skipif(os.name == 'nt', reason="only run on unix")

def test_is_abspath():
    abspath = Path.from_argv()
    assert abspath.is_abspath()
    assert abspath == sys.argv[0]
    assert abspath is abspath.get_abspath()

    relpath = Path('abc') # rel path
    assert relpath.get_abspath().is_abspath()
    assert relpath.get_abspath() == os.path.abspath('abc')

def test_abspath_get_parent():
    path = Path.from_argv(0)
    parent = path.get_parent()
    assert parent == os.path.dirname(sys.argv[0])

@on_win
def test_abspath_get_parent_on_win32():
    src_path = os.path.join('c:\\', 'd', 'e')
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    assert path.get_parent(1) == os.path.join('c:\\', 'd')
    assert path.get_parent(2) == 'c:\\'
    assert path.get_parent(3) is None
    assert path.get_parent(4) is None

@on_unix
def test_abspath_get_parent_on_unix():
    src_path = os.path.join('/', 'd', 'e')
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    assert path.get_parent(1) == os.path.join('/', 'd')
    assert path.get_parent(2) == '/'
    assert path.get_parent(3) is None
    assert path.get_parent(4) is None

def test_abspath_property():
    pass

@on_win
def test_abspath_property_on_win32():

    # test root:
    for root_str in ['c:', 'c:\\']:
        root_path = Path(root_str)
        assert root_path.name == 'c:'

@on_unix
def test_abspath_propertye_on_unix():

    # test root:
    root_path = Path('/')
    assert root_path.name == '/'

def test_abspath_join():
    # join with pardir
    path = Path.from_argv() / os.path.pardir
    assert path.is_abspath()
    assert path == os.path.dirname(sys.argv[0])

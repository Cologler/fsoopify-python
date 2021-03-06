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
    assert not Path('abc').is_abspath()

def test_get_abspath():
    relpath = Path('abc')
    abspath = relpath.get_abspath()
    assert abspath.is_abspath()
    assert abspath == os.path.abspath('abc')

def test_get_relpath():
    relpath = Path('abc')
    assert relpath.get_relpath() is relpath
    assert relpath.get_relpath(os.path.curdir) == relpath
    cwd = os.getcwd()
    pardir = os.path.basename(cwd)
    assert relpath.get_relpath(os.path.pardir) == os.path.join(pardir, 'abc')

def test_relpath_get_parent_when_root_is_dir():
    src_path = os.path.join('a', 'b', 'c')
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    assert path.get_parent(1) == os.path.join('a', 'b')
    assert path.get_parent(2) == os.path.join('a')
    assert path.get_parent(3) == os.path.curdir
    for i in range(1, 10):
        assert path.get_parent(3+i) == os.path.join(*([os.path.pardir] * i))

def test_relpath_get_parent_when_root_is_curdir():
    src_path = os.path.join(os.path.curdir, 'a', 'b', 'c')
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    assert path.get_parent(1) == os.path.join(os.path.curdir, 'a', 'b')
    assert path.get_parent(2) == os.path.join(os.path.curdir, 'a')
    assert path.get_parent(3) == os.path.curdir
    for i in range(1, 10):
        assert path.get_parent(3+i) == os.path.join(*([os.path.pardir] * i))

def test_relpath_get_parent_when_path_is_curdir():
    src_path = os.path.curdir
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    for i in range(1, 10):
        assert path.get_parent(i) == os.path.join(*([os.path.pardir] * i))

def test_relpath_get_parent_when_path_is_pardir():
    src_path = os.path.pardir
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    for i in range(1, 10):
        assert path.get_parent(i) == os.path.join(*([os.path.pardir] * (1+i)))

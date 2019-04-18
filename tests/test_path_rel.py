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

NT = sys.platform == 'win32'

def test_get_parent_when_root_is_dir():
    src_path = os.path.join('a', 'b', 'c')
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    assert path.get_parent(1) == os.path.join('a', 'b')
    assert path.get_parent(2) == os.path.join('a')
    assert path.get_parent(3) == os.path.curdir
    for i in range(1, 10):
        assert path.get_parent(3+i) == os.path.join(*([os.path.pardir] * i))

def test_get_parent_when_root_is_curdir():
    src_path = os.path.join(os.path.curdir, 'a', 'b', 'c')
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    assert path.get_parent(1) == os.path.join(os.path.curdir, 'a', 'b')
    assert path.get_parent(2) == os.path.join(os.path.curdir, 'a')
    assert path.get_parent(3) == os.path.curdir
    for i in range(1, 10):
        assert path.get_parent(3+i) == os.path.join(*([os.path.pardir] * i))

def test_get_parent_when_path_is_curdir():
    src_path = os.path.curdir
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    for i in range(1, 10):
        assert path.get_parent(i) == os.path.join(*([os.path.pardir] * i))

def test_get_parent_when_path_is_pardir():
    src_path = os.path.pardir
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    for i in range(1, 10):
        assert path.get_parent(i) == os.path.join(*([os.path.pardir] * (1+i)))

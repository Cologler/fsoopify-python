# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# test path class
# ----------

import sys
import os

import pytest

from fsoopify import Path

def get_path_from_argv_0():
    path_str = sys.argv[0]
    path = Path(path_str)
    return path_str, path

def test_path_types():
    _, path = get_path_from_argv_0()
    assert isinstance(path, Path)
    assert isinstance(path, str)
    assert issubclass(Path, str)

def test_path_equals():
    path_str, path = get_path_from_argv_0()
    assert path == path_str
    assert path_str == path
    assert path == os.path.normcase(path_str.upper())
    assert path == os.path.normcase(path_str.lower())

def test_path_normalcase():
    path_str, path = get_path_from_argv_0()
    assert path.normalcase == os.path.normcase(path_str)

def test_path_abspath():
    path_str, path = get_path_from_argv_0()
    assert path.is_abspath() == os.path.isabs(path_str)
    assert path.get_abspath().is_abspath()
    assert path.get_abspath() == os.path.abspath(path_str)

    path_str = 's'
    path = Path(path_str)
    assert path.is_abspath() == os.path.isabs(path_str)
    assert path.get_abspath().is_abspath()
    assert path.get_abspath() == os.path.abspath(path_str)

@pytest.mark.skipif(sys.platform != 'win32', reason="only run on windows")
def test_path_abspath_win32_root():
    path_str = 'c:\\'
    path = Path(path_str)
    assert os.path.isabs(path_str)
    assert path.is_abspath() == os.path.isabs(path_str)
    assert path.get_abspath().is_abspath()
    assert path.get_abspath() == os.path.abspath(path_str)

    # c: should be abspath
    path_str = 'c:'
    path = Path(path_str)
    assert not os.path.isabs(path_str)
    assert path.is_abspath()
    assert path.get_abspath() == os.path.abspath(path_str)

def test_path_dirname():
    path_str, path = get_path_from_argv_0()
    assert path.dirname == os.path.dirname(path_str)

def test_path_dirname_root():
    if sys.platform == 'win32':
        top_dir = Path('c:')
        assert top_dir.name == 'c:'
    else: # posix
        top_dir = Path('/')
        assert top_dir.name == '/'
    assert top_dir.dirname == ''

def test_path_name():
    path_str, path = get_path_from_argv_0()
    assert path.name == os.path.split(path_str)[1]

def test_path_name_pure_name():
    path_str, path = get_path_from_argv_0()
    assert path.name.pure_name == os.path.splitext(os.path.split(path_str)[1])[0]

def test_path_name_ext():
    path_str, path = get_path_from_argv_0()
    assert path.name.ext == os.path.splitext(os.path.split(path_str)[1])[1]

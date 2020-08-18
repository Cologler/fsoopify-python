# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# test path class
# ----------

import sys
import os
import itertools

import pytest

from fsoopify import Path

on_win = pytest.mark.skipif(os.name != 'nt', reason="only run on windows")
on_unix = pytest.mark.skipif(os.name == 'nt', reason="only run on unix")

NT = sys.platform == 'win32'

def get_path_from_argv_0():
    path_str = sys.argv[0]
    path = Path(path_str)
    return path_str, path

def test_path_types():
    path = Path.from_argv()
    assert isinstance(path, Path)
    assert isinstance(path, str)
    assert issubclass(Path, str)

def test_path_equals():
    path = Path.from_argv()
    path_str = sys.argv[0]
    assert type(path) != type(path_str)
    assert path == path_str
    assert path_str == path

@on_win
def test_path_equals_on_win32():
    # ignore case
    for l, r in itertools.product(['c:', 'C:'], repeat=2):
        assert Path(l) == Path(r)

    # ignore drive sep
    for l, r in itertools.product(['c:\\', 'C:'], repeat=2):
        assert Path(l) == Path(r)

    path_str, path = get_path_from_argv_0()
    assert path == path_str.upper()
    assert path == path_str.lower()
    assert path == os.path.normcase(path_str.upper())
    assert path == os.path.normcase(path_str.lower())

def test_path_normalcase():
    _, path = get_path_from_argv_0()
    assert isinstance(path.normalcase, str)

@pytest.mark.skipif(sys.platform != 'win32', reason="only run on windows")
def test_abspath_with_root_on_win32():
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
    assert path.get_abspath() == os.path.abspath('c:\\')

def test_abspath_dirname_and_name():
    path_str, path = get_path_from_argv_0()
    assert path.dirname == os.path.dirname(path_str)
    assert path.name == os.path.basename(path_str)

    if NT:
        path = Path('a:\\b\\c\\d')
        dirname = path.dirname
        assert str(dirname) == 'a:\\b\\c'
        dirname = dirname.dirname
        assert str(dirname) == 'a:\\b'
        dirname = dirname.dirname
        assert str(dirname) == 'a:\\'

        assert Path('C:').dirname is None
        assert Path('C:\\').dirname is None
    else:
        assert Path('/').dirname is None

def test_relpath_dirname_and_name():
    path_str = 's'
    path = Path(path_str)

    dirname, name = path.dirname, path.name
    assert str(dirname) == '.'
    assert str(name) == 's'
    dirname, name = dirname.dirname, dirname.name
    assert str(dirname) == '..'
    assert str(name) == '.'
    dirname, name = dirname.dirname, dirname.name
    assert str(dirname) == os.path.join('..', '..')
    assert str(name) == '..'
    dirname, name = dirname.dirname, dirname.name
    assert str(dirname) == os.path.join('..', '..', '..')
    assert str(name) == '..'
    dirname, name = dirname.dirname, dirname.name
    assert str(dirname) == os.path.join('..', '..', '..', '..')
    assert str(name) == '..'

def test_path_name_pure_name():
    path_str, path = get_path_from_argv_0()
    assert path.name.pure_name == os.path.splitext(os.path.split(path_str)[1])[0]

def test_path_name_ext():
    path_str, path = get_path_from_argv_0()
    assert path.name.ext == os.path.splitext(os.path.split(path_str)[1])[1]

def test_path_div():
    ' allow to use `Path() / str()` expr '

    path = Path.from_argv()
    new_path = path / 'abc'
    assert isinstance(path, Path)
    assert new_path == os.path.join(sys.argv[0], 'abc')

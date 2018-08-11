# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# test path class
# ----------

import sys
import os

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
    _, path = get_path_from_argv_0()
    assert path.is_abspath()
    assert path.get_abspath() is path

    assert Path('c:\\').get_abspath() == 'c:\\'
    assert Path('c:').get_abspath() == 'c:\\'
    assert not Path('s').is_abspath()

def test_path_dirname():
    path_str, path = get_path_from_argv_0()
    assert path.dirname == os.path.dirname(path_str)

    # since `os.path.split('c:')` return `('c:', '')`:
    top_dir = Path('c:')
    assert top_dir.dirname == 'c:'
    assert top_dir.name == ''

def test_path_name():
    path_str, path = get_path_from_argv_0()
    assert path.name == os.path.split(path_str)[1]

def test_path_name_pure_name():
    path_str, path = get_path_from_argv_0()
    assert path.name.pure_name == os.path.splitext(os.path.split(path_str)[1])[0]

def test_path_name_ext():
    path_str, path = get_path_from_argv_0()
    assert path.name.ext == os.path.splitext(os.path.split(path_str)[1])[1]

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

def only_run_on_win(func):
    return pytest.mark.skipif(sys.platform != 'win32', reason="only run on windows")(
        func
    )

def only_run_on_unix(func):
    return pytest.mark.skipif(sys.platform == 'win32', reason="only run on unix")(
        func
    )

def test_abspath_get_parent():
    path = Path.from_argv(0)
    parent = path.get_parent()
    assert parent == os.path.dirname(sys.argv[0])

def _assert_root_abspath_unable_get_parent(path: Path):
    assert path.is_abspath()

    # unable to get parent
    with pytest.raises(ValueError, match='max level is 0'):
        path.get_parent()

    # dirname is None
    assert path.dirname is None

@only_run_on_win
def test_abspath_get_parent_on_win32():
    src_path = os.path.join('c:\\', 'd', 'e')
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    assert path.get_parent(1) == os.path.join('c:\\', 'd')
    assert path.get_parent(2) == 'c:\\'
    with pytest.raises(ValueError, match='max level is 2'):
        path.get_parent(3)

    # test root:
    _assert_root_abspath_unable_get_parent(Path('C:'))
    _assert_root_abspath_unable_get_parent(Path('C:\\'))

@only_run_on_unix
def test_abspath_get_parent_on_unix():
    src_path = os.path.join('/', 'd', 'e')
    path = Path(src_path)
    assert path.get_parent(1) == path.dirname
    assert path.get_parent(1) == os.path.join('/', 'd')
    assert path.get_parent(2) == '/'
    with pytest.raises(ValueError, match='max level is 2'):
        path.get_parent(3)

    # test root:
    _assert_root_abspath_unable_get_parent(Path('/'))

def test_abspath_property():
    pass

@only_run_on_win
def test_abspath_property_on_win32():

    # test root:
    for root_str in ['c:', 'c:\\']:
        root_path = Path(root_str)
        assert root_path.name == 'c:'

@only_run_on_unix
def test_abspath_propertye_on_unix():

    # test root:
    root_path = Path('/')
    assert root_path.name == '/'

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

def test_abspath_get_parent():
    path = Path.from_argv(0)
    parent = path.get_parent()
    assert parent == os.path.dirname(sys.argv[0])

def _assert_root_abspath_unable_get_parent(path: Path):
    assert path.is_abspath()
    with pytest.raises(ValueError, match='max level is 0'):
        path.get_parent()

@pytest.mark.skipif(not NT, reason="only run on windows")
def test_abspath_get_parent_win32():
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

@pytest.mark.skipif(NT, reason="only run on unix")
def test_abspath_get_parent_unix():

    # test root:
    _assert_root_abspath_unable_get_parent(Path('/'))

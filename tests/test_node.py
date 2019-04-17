# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# test base class `NodeInfo`
# ----------

import sys
import os

import pytest

from fsoopify import NodeInfo, FileInfo, DirectoryInfo

# create by static methods:

def test_node_from_path():
    assert isinstance(NodeInfo.from_path(sys.argv[0]), FileInfo)
    assert isinstance(NodeInfo.from_path(os.path.dirname(sys.argv[0])), DirectoryInfo)

def test_node_from_cwd():
    dir_info = NodeInfo.from_cwd()
    assert isinstance(dir_info, DirectoryInfo)
    assert dir_info.path == os.getcwd()

def test_node_from_argv0():
    file_info = NodeInfo.from_argv0()
    assert isinstance(file_info, FileInfo)
    assert file_info.path == sys.argv[0]

def test_node_get_parent():
    # parent of abs
    file_info = NodeInfo.from_argv0()
    parent_dir = file_info.get_parent()
    assert isinstance(parent_dir, DirectoryInfo)
    assert parent_dir.path == os.path.dirname(sys.argv[0])

@pytest.mark.skipif(sys.platform == 'win32', reason="does not run on windows")
def test_node_get_parent_posix():
    # parent of root is None
    top_dir = DirectoryInfo('/')
    assert top_dir.get_parent() is None

# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from fsoopify import DirectoryInfo, FileInfo, NodeType

def test_dir_node_type():
    assert DirectoryInfo('.').node_type is NodeType.dir

def test_get_fileinfo():
    dir_info = DirectoryInfo('.')
    assert isinstance(dir_info.get_fileinfo('a'), FileInfo)

def test_get_dirinfo():
    dir_info = DirectoryInfo('.')
    assert isinstance(dir_info.get_dirinfo('a'), DirectoryInfo)

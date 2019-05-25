# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import tempfile

from fsoopify import DirectoryInfo, FileInfo, NodeType

def test_dir_node_type():
    assert DirectoryInfo('.').node_type is NodeType.dir

def test_get_fileinfo():
    dir_info = DirectoryInfo('.')
    assert isinstance(dir_info.get_fileinfo('a'), FileInfo)

def test_get_dirinfo():
    dir_info = DirectoryInfo('.')
    assert isinstance(dir_info.get_dirinfo('a'), DirectoryInfo)

def test_get_unique_name():
    with tempfile.TemporaryDirectory() as tmpdir:
        dir_info = DirectoryInfo(tmpdir)
        name = 'abc'

        unique_name = dir_info.get_unique_name(name, '.py')
        assert unique_name == 'abc.py'

        dir_info.get_fileinfo(unique_name).write_text('')
        unique_name = dir_info.get_unique_name(name, '.py')
        assert unique_name == 'abc (1).py'

        dir_info.get_fileinfo(unique_name).write_text('')
        unique_name = dir_info.get_unique_name(name, '.py')
        assert unique_name == 'abc (2).py'

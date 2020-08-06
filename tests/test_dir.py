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

def test_make_tree():
    with tempfile.TemporaryDirectory() as tmpdir:
        dir_info = DirectoryInfo(tmpdir)
        dir_info.make_tree({
            'a.txt': 'abc',
            'b.txt': b'cde',
            'subdir': {
                'e.txt': 'ddd'
            }
        })

        assert dir_info.get_fileinfo('a.txt').read_text() == 'abc'
        assert dir_info.get_fileinfo('b.txt').read_text() == 'cde'

        subdir = dir_info.get_dirinfo('subdir')
        assert subdir.is_directory()
        assert subdir.get_fileinfo('e.txt').read_text() == 'ddd'

def test_get_tree():
    with tempfile.TemporaryDirectory() as tmpdir:
        tree = {
            'a.txt': b'abc',
            'b.txt': b'cde',
            'subdir': {
                'e.txt': b'ddd'
            }
        }
        dir_info = DirectoryInfo(tmpdir)
        dir_info.make_tree(tree)

        assert dir_info.get_tree() == tree

def test_make_tree_with_stream():
    with tempfile.TemporaryDirectory() as tmpdir:
        tree = {
            'a.txt': b'abc',
            'b.txt': b'cde',
            'subdir': {
                'e.txt': b'ddd'
            }
        }
        dir_info = DirectoryInfo(tmpdir)
        dir_info.make_tree(tree)

        with dir_info.get_tree(as_stream=True) as stree:
            with tempfile.TemporaryDirectory() as tmpdir2:
                dir_info_2 = DirectoryInfo(tmpdir2)
                dir_info_2.make_tree(stree)
                assert dir_info_2.get_tree() == tree

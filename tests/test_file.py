#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import tempfile

from fsoopify import (
    NodeType,
    DirectoryInfo, FileInfo
)

def test_dir_node_type():
    assert DirectoryInfo('.').node_type is NodeType.dir

def test_file_node_type():
    assert FileInfo('abc').node_type is NodeType.file

def test_get_file_hash():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        fi.write_bytes(b'd1s5a')
        hashs = fi.get_file_hash('crc32', 'md5', 'sha1')
        assert hashs == ('2c34fc25', 'f8fc4601b857c7acc459f7118fbca878', 'fe0b025ab8735a2a7bd431b249b42e888e2df1f6')

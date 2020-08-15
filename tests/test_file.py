#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from fsoopify import (
    NodeType,
    DirectoryInfo, FileInfo
)

def test_dir_node_type():
    assert DirectoryInfo('.').node_type is NodeType.dir

def test_file_node_type():
    assert FileInfo('abc').node_type is NodeType.file

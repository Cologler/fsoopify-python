#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import tempfile

from fsoopify import (
    NodeType,
    DirectoryInfo, FileInfo
)

def test_dir_node_type():
    assert DirectoryInfo('.').node_type is NodeType.dir

def test_file_node_type():
    assert FileInfo('abc').node_type is NodeType.file

def test_write_bytes():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_exists()
        fi.write_bytes(b'd1s5a')
        assert fi.read_bytes() == b'd1s5a'
        fi.write_bytes(bytearray(b'fnnuah'), append=False)
        assert fi.read_bytes() == b'fnnuah'
        fi.write_bytes(b'd1s5a', append=True)
        assert fi.read_bytes() == b'fnnuahd1s5a'

def test_iadd_str():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_exists()
        fi += 'd1s5a'
        assert fi.is_exists()
        assert fi.read_text() == 'd1s5a'
        fi += 'fdsaf'
        assert fi.read_text() == 'd1s5afdsaf'

def test_iadd_bytes():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_exists()
        fi += b'd1s5a'
        assert fi.is_exists()
        assert fi.read_bytes() == b'd1s5a'
        fi += b'fdsaf'
        assert fi.read_bytes() == b'd1s5afdsaf'
        fi += bytearray(b'fhue')
        assert fi.read_bytes() == b'd1s5afdsaffhue'

def test_iadd_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        fi.write_bytes(b'd1s5a')
        fi2 = DirectoryInfo(tmpdir).get_fileinfo('tmp2.txt')
        fi2.write_bytes(b'dsami')
        fi2 += fi
        assert fi2.read_bytes() == b'dsamid1s5a'

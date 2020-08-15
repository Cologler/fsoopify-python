# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import tempfile

import pytest

from fsoopify import *

def test_open_or_create_text():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_file()
        with pytest.raises(FileNotFoundError):
            with fi.open('r+'):
                pass
        with fi.open_or_create('r+') as fp:
            fp.write('123')
            fp.seek(0)
            assert fp.read() == '123'
        with pytest.raises(FileExistsError):
            with fi.open('x+'):
                pass
        with fi.open_or_create('r+') as fp:
            assert fp.read() == '123'
        assert fi.read_text() == '123'

def test_open_or_create_bytes():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_file()
        with pytest.raises(FileNotFoundError):
            with fi.open('r+b'):
                pass
        with fi.open_or_create('r+b') as fp:
            fp.write(b'123')
            fp.seek(0)
            assert fp.read() == b'123'
        with pytest.raises(FileExistsError):
            with fi.open('x+'):
                pass
        with fi.open_or_create('r+b') as fp:
            assert fp.read() == b'123'
        assert fi.read_bytes() == b'123'

def test_awt_file_atomic():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        with fi.open('a+', atomic=True) as fp:
            fp.write('12')
        with fi.open('a+', atomic=True) as fp:
            fp.write('34')
        assert fi.read_text() == '1234'

def test_awb_file_atomic():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')

        with fi.open('a+b', atomic=True) as fp:
            fp.write(b'12')

        with fi.open('a+b', atomic=True) as fp:
            fp.write(b'34')

        assert fi.read_bytes() == b'1234'

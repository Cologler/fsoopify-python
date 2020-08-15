# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import tempfile
import itertools

import pytest

from fsoopify import *

lock_atomic_params = (
    'lock, atomic',
    list(itertools.product([True, False], repeat=2))
)

@pytest.mark.parametrize(*lock_atomic_params)
def test_open_text(lock, atomic):
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_file()

        with fi.open('x', lock=lock, atomic=atomic) as fp:
            fp.write('ctn')
        assert fi.read_text() == 'ctn'

        with fi.open('r', lock=lock, atomic=atomic) as fp:
            assert fp.read() == 'ctn'
        assert fi.read_text() == 'ctn'

        with fi.open('w', lock=lock, atomic=atomic) as fp:
            assert fp.write('dsjai')
        assert fi.read_text() == 'dsjai'

        with fi.open('a', lock=lock, atomic=atomic) as fp:
            assert fp.write('fwq523')
        assert fi.read_text() == 'dsjai' + 'fwq523'

@pytest.mark.parametrize(*lock_atomic_params)
def test_open_text_rw(lock, atomic):
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_file()

        with fi.open('x+', lock=lock, atomic=atomic) as fp:
            fp.write('ctn')
            fp.seek(0)
            assert fp.read() == 'ctn'
        assert fi.read_text() == 'ctn'

        with fi.open('r+', lock=lock, atomic=atomic) as fp:
            assert fp.read() == 'ctn'
            fp.seek(0)
            fp.write('fjwi')
            fp.seek(0)
            assert fp.read() == 'fjwi'
        assert fi.read_text() == 'fjwi'

        with fi.open('w+', lock=lock, atomic=atomic) as fp:
            assert fp.read() == ''
            assert fp.write('d')
        assert fi.read_text() == 'd'

        with fi.open('a+', lock=lock, atomic=atomic) as fp:
            fp.seek(0)
            assert fp.read() == 'd'
            fp.seek(0)
            assert fp.write('fwq523')
        assert fi.read_text() == 'd' + 'fwq523'

@pytest.mark.parametrize(*lock_atomic_params)
def test_open_bytes(lock, atomic):
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_file()

        with fi.open('xb', lock=lock, atomic=atomic) as fp:
            fp.write(b'ctn')
        assert fi.read_bytes() == b'ctn'

        with fi.open('rb', lock=lock, atomic=atomic) as fp:
            assert fp.read() == b'ctn'
        assert fi.read_bytes() == b'ctn'

        with fi.open('wb', lock=lock, atomic=atomic) as fp:
            assert fp.write(b'dsjai')
        assert fi.read_bytes() == b'dsjai'

        with fi.open('ab', lock=lock, atomic=atomic) as fp:
            assert fp.write(b'fwq523')
        assert fi.read_bytes() == b'dsjai' + b'fwq523'

@pytest.mark.parametrize(*lock_atomic_params)
def test_open_bytes_rw(lock, atomic):
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_file()

        with fi.open('x+b', lock=lock, atomic=atomic) as fp:
            fp.write(b'ctn')
            fp.seek(0)
            assert fp.read() == b'ctn'
        assert fi.read_bytes() == b'ctn'

        with fi.open('r+b', lock=lock, atomic=atomic) as fp:
            assert fp.read() == b'ctn'
            fp.seek(0)
            fp.write(b'fjwi')
            fp.seek(0)
            assert fp.read() == b'fjwi'
        assert fi.read_bytes() == b'fjwi'

        with fi.open('w+b', lock=lock, atomic=atomic) as fp:
            assert fp.read() == b''
            assert fp.write(b'd')
        assert fi.read_bytes() == b'd'

        with fi.open('a+b', lock=lock, atomic=atomic) as fp:
            fp.seek(0)
            assert fp.read() == b'd'
            fp.seek(0)
            assert fp.write(b'fwq523')
        assert fi.read_bytes() == b'd' + b'fwq523'

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

def test_rwt_file_atomic():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')

        with fi.open('r+', atomic=True) as fp:
            fp.write('12')

        with fi.open('r+', atomic=True) as fp:
            assert fp.read() == '12'
            fp.write('34')

        assert fi.read_text() == '1234'

        with fi.open('r+', atomic=True) as fp:
            fp.write('56')

        assert fi.read_text() == '5634'

def test_rwb_file_atomic():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')

        with fi.open('r+b', atomic=True) as fp:
            fp.write(b'12')

        with fi.open('r+b', atomic=True) as fp:
            fp.write(b'34')

        assert fi.read_bytes() == b'34'

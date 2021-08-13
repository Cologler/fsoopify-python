# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import tempfile
import itertools
import io

import pytest

from fsoopify import *

param_lock = pytest.mark.parametrize("lock", [True, False])
param_atomic = pytest.mark.parametrize("atomic", [True, False])

@param_lock
@param_atomic
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

@param_lock
@param_atomic
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

@param_lock
@param_atomic
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

@param_lock
@param_atomic
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

@param_lock
@param_atomic
def test_open_or_create_text(lock, atomic):
    kwargs = dict(lock=lock, atomic=atomic, or_create=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_file()
        with pytest.raises(FileNotFoundError):
            with fi.open('r+'):
                pass
        with fi.open('r+', **kwargs) as fp:
            fp.write('123')
            fp.seek(0)
            assert fp.read() == '123'
        with pytest.raises(FileExistsError):
            with fi.open('x+'):
                pass
        with fi.open('r+', **kwargs) as fp:
            assert fp.read() == '123'
        assert fi.read_text() == '123'

@param_lock
@param_atomic
def test_open_or_create_bytes(lock, atomic):
    kwargs = dict(lock=lock, atomic=atomic, or_create=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        with fi.open('rb', **kwargs) as fp:
            assert fp.read() == b''

    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')

        with fi.open('r+b', **kwargs) as fp:
            assert fp.read() == b''
            fp.write(b'123')
            fp.seek(0)
            assert fp.read() == b'123'
        assert fi.read_bytes() == b'123'

        with fi.open('r+b', **kwargs) as fp:
            assert fp.read() == b'123'

        assert fi.read_bytes() == b'123'

def test_read_bytes():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        with open(fi.path, 'xb') as fp:
            fp.write(b'fjasij')
        assert fi.read_bytes() == b'fjasij'

def test_read_text():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        with open(fi.path, 'xt') as fp:
            fp.write('fjasij')
        assert fi.read_text() == 'fjasij'

@pytest.mark.parametrize('encoding', ['utf-8', 'utf-16', 'utf-16-be'])
def test_read_text_with_encoding(encoding):
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        with open(fi.path, 'xb') as fp:
            fp.write('fjasij'.encode(encoding))
        assert fi.read_text(encoding) == 'fjasij'

def test_read_into_stream():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not src.is_exists()
        src.write_bytes(b'd1s5afajjmogjfwiughweuihgw')

        dest = io.BytesIO()
        src.copy_to_stream(dest)
        assert dest.getvalue() == b'd1s5afajjmogjfwiughweuihgw'

        dest = io.BytesIO()
        src.copy_to_stream(dest, buffering=6)
        assert dest.getvalue() == b'd1s5afajjmogjfwiughweuihgw'

        dest = io.StringIO()
        src.copy_to_stream(dest)
        assert dest.getvalue() == 'd1s5afajjmogjfwiughweuihgw'

def test_write_text():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        fi.write_text('dsajuidhsa')
        assert fi.read_text() == 'dsajuidhsa'
        fi.write_text('你好')
        assert fi.read_text() == 'dsajuidhsa你好'

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

def test_write_from_stream():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        fi.write_from_stream(io.StringIO('dsajuidhsa'))
        assert fi.read_text() == 'dsajuidhsa'
        fi.write_from_stream(io.BytesIO(b'fdsamdks'), append=True)
        assert fi.read_bytes() == b'dsajuidhsafdsamdks'

def test_copy_to():
    with tempfile.TemporaryDirectory() as tmpdir:
        data = b'fhuiwhwe uieh'

        root = DirectoryInfo(tmpdir)
        src = root.get_fileinfo('src.txt')
        src.write_bytes(data)

        # copy with `str`
        dest1_fi = root.get_fileinfo('dst1.txt')
        src.copy_to(dest1_fi.path)
        assert data == dest1_fi.read_bytes()

        # copy with `FileInfo`
        dest2_fi = root.get_fileinfo('dst2.txt')
        src.copy_to(dest2_fi)
        assert data == dest2_fi.read_bytes()

        # copy with `DirectoryInfo`
        dest3_dir = root.get_dirinfo('djsai')
        dest3_dir.ensure_created()
        src.copy_to(dest3_dir)
        assert data == dest3_dir.get_fileinfo(src.path.name).read_bytes()

def test_copy_from():
    with tempfile.TemporaryDirectory() as tmpdir:
        data = b'fhuiwhwe uieh'

        root = DirectoryInfo(tmpdir)
        src = root.get_fileinfo('src.txt')
        src.write_bytes(data)

        # copy with `str`
        dest1_fi = root.get_fileinfo('dst1.txt')
        dest1_fi.copy_from(src.path)
        assert data == dest1_fi.read_bytes()

        # copy with `FileInfo`
        dest2_fi = root.get_fileinfo('dst2.txt')
        dest2_fi.copy_from(src)
        assert data == dest2_fi.read_bytes()

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

def test_iadd_stream():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        assert not fi.is_exists()
        fi += io.BytesIO(b'd1s5a')
        assert fi.is_exists()
        assert fi.read_bytes() == b'd1s5a'
        fi += io.StringIO('fdsaf')
        assert fi.read_bytes() == b'd1s5afdsaf'

def test_iadd_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        fi = DirectoryInfo(tmpdir).get_fileinfo('tmp.txt')
        fi.write_bytes(b'd1s5a')
        fi2 = DirectoryInfo(tmpdir).get_fileinfo('tmp2.txt')
        fi2.write_bytes(b'dsami')
        fi2 += fi
        assert fi2.read_bytes() == b'dsamid1s5a'
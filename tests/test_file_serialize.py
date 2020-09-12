# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import tempfile
import contextlib

import pytest
from pytest import raises

from fsoopify import DirectoryInfo, FormatNotFoundError, FileInfo

example_data_1 = {
    'a': 1,
    'b': '2',
    'c': {
        'd': 'ddddd'
    }
}

param_data = pytest.mark.parametrize("data", [example_data_1])
param_lock = pytest.mark.parametrize("lock", [True, False])
param_atomic = pytest.mark.parametrize("atomic", [True, False])

@param_data
@pytest.mark.parametrize('format', ['json', 'json5', 'yaml', 'toml', 'pickle'])
@pytest.mark.parametrize('ext', ['', 'json', 'bin', 'txt'])
def test_dump_load_with_format(data, format, ext):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_info = DirectoryInfo(tmpdir).get_fileinfo(f'data' + ext)
        file_info.dump(data, format)
        assert data == file_info.load(format)

@param_data
@pytest.mark.parametrize('ext', ['json', 'json5', 'yaml', 'toml'])
def test_dump_load_with_ext(data, ext):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_info = DirectoryInfo(tmpdir).get_fileinfo(f'data_.{ext}')
        file_info.dump(data)
        assert data == file_info.load()

@param_data
@param_lock
@param_atomic
def test_load_context(data, lock: bool, atomic: bool):
    with tempfile.TemporaryDirectory() as tmpdir:
        dir_info = DirectoryInfo(tmpdir)
        file_info = dir_info.get_fileinfo('test_load_context.json')

        # test create
        assert not file_info.is_exists()
        with file_info.load_context(lock=lock, atomic=atomic) as s:
            assert s.data is None
            assert not file_info.is_exists()
            s.data = data
        assert file_info.is_exists()

        # test read and write
        with file_info.load_context(lock=lock, atomic=atomic) as s:
            assert s.data == data
            s.data = {}
        with file_info.load_context(lock=lock, atomic=atomic) as s:
            assert s.data == {}

        # test remove
        with file_info.load_context(lock=lock, atomic=atomic) as s:
            s.data = None
        assert not file_info.is_exists()

@param_data
@param_lock
@param_atomic
def test_load_context_with_error(data, lock, atomic):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_info = DirectoryInfo(tmpdir).get_fileinfo('a.json')
        assert not file_info.is_exists()

        with file_info.load_context(lock=lock, atomic=atomic) as s:
            assert s.data is None
            s.data = data
        assert file_info.is_exists()

        with contextlib.suppress(ValueError):
            with file_info.load_context(lock=lock, atomic=atomic) as s:
                assert s.data == data
                s.data = {}
                raise ValueError # raise any error

        with file_info.load_context(lock=lock, atomic=atomic) as s:
            assert s.data == data # still not changes

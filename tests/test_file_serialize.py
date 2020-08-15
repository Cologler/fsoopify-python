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

test_data_dir = DirectoryInfo('test_data_dir')
test_data_dir.ensure_created()

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
def test_dump_load_with_format(data):
    with tempfile.TemporaryDirectory() as tmpdir:
        dir_info = DirectoryInfo(tmpdir)

        for fmt in ('json', 'json5', 'yaml', 'toml', 'pickle'):
            file_info = dir_info.get_fileinfo(f'data_{fmt}.{fmt}')
            file_info.dump(data, fmt)
            assert data == file_info.load(fmt)

@param_data
def test_dump_load_with_ext(data):
    with tempfile.TemporaryDirectory() as tmpdir:
        dir_info = DirectoryInfo(tmpdir)

        for ext in ('json', 'json5', 'yaml', 'toml'):
            file_info = dir_info.get_fileinfo(f'data_.{ext}')
            file_info.dump(data)
            assert data == file_info.load()

        for fmt in ('pickle', ):
            fi = dir_info.get_fileinfo(f'data_{fmt}.{fmt}')
            with raises(FormatNotFoundError):
                fi.dump(data)
            with raises(FormatNotFoundError):
                fi.load()

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

def test_load_context_with_error():
    data = example_data_1
    name = 'test_load_context.json'
    with tempfile.TemporaryDirectory() as tmpdir:
        dir_info = DirectoryInfo(tmpdir)
        file_info = dir_info.get_fileinfo(name)
        assert not file_info.is_exists()

        with file_info.load_context(lock=True) as s:
            assert s.data is None
            s.data = data
        assert file_info.is_exists()

        with contextlib.suppress(ValueError):
            with file_info.load_context(lock=True) as s:
                assert s.data == data
                s.data = {}
                raise ValueError # raise any error

        with file_info.load_context(lock=True) as s:
            assert s.data == data # still not changes


def test_pipfile():
    import pipfile
    from fsoopify.serialize import NotSupportError
    assert FileInfo('Pipfile').load() == pipfile.load('Pipfile').data
    with raises(NotSupportError):
        FileInfo('Pipfile').dump({})

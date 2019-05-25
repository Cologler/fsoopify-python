# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import tempfile

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

def test_dump_load_with_format():
    data = example_data_1

    with tempfile.TemporaryDirectory() as tmpdir:
        dir_info = DirectoryInfo(tmpdir)

        for fmt in ('json', 'json5', 'yaml', 'toml', 'pickle'):
            file_info = dir_info.get_fileinfo(f'data_{fmt}.{fmt}')
            file_info.dump(data, fmt)
            assert data == file_info.load(fmt)

def test_dump_load_with_ext():
    data = example_data_1

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

def test_pipfile():
    import pipfile
    assert FileInfo('Pipfile').load() == pipfile.load('Pipfile').data
    with raises(NotImplementedError):
        FileInfo('Pipfile').dump({})

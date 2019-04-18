# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

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
    for fmt in ('json', 'json5', 'yaml', 'toml', 'pickle'):
        file_info = test_data_dir.get_fileinfo(f'test_data_1_{fmt}.{fmt}')
        file_info.dump(example_data_1, fmt)
        assert example_data_1 == file_info.load(fmt)

def test_dump_load_with_ext():

    for ext in ('json', 'json5', 'yaml', 'toml'):
        file_info = test_data_dir.get_fileinfo(f'test_data_2.{ext}')
        file_info.dump(example_data_1)
        assert example_data_1 == file_info.load()

    for fmt in ('pickle', ):
        fi = test_data_dir.get_fileinfo(f'test_data_2_{fmt}.{fmt}')
        with raises(FormatNotFoundError):
            fi.dump(example_data_1)
        with raises(FormatNotFoundError):
            fi.load()

def test_pipfile():
    import pipfile
    assert FileInfo('Pipfile').load() == pipfile.load('Pipfile').data
    with raises(NotImplementedError):
        FileInfo('Pipfile').dump({})
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback
import unittest
from fsoopify import (
    Path,
    NodeInfo, DirectoryInfo, FileInfo,
)

class Test(unittest.TestCase):
    def test_node(self):
        NodeInfo.from_path('.').list_items

    def test_path(self):
        rpath = r'D:\Projects-Arc\fsoopify-python.xx'
        path = Path(rpath)

        self.assertEqual(path, rpath)
        self.assertEqual(path.normalcase, os.path.normcase(rpath))
        self.assertTrue(path.equals(rpath.upper()))

        self.assertEqual(path.dirname, os.path.dirname(rpath))
        self.assertEqual(path.name, os.path.split(rpath)[1])
        self.assertEqual(path.name.pure_name, os.path.splitext(os.path.split(rpath)[1])[0])
        self.assertEqual(path.name.ext, os.path.splitext(os.path.split(rpath)[1])[1])

    test_data_dir = DirectoryInfo('test_data_dir')
    test_data_dir.ensure_created()

    def test_extra(self):
        for fmt in ('json', 'json5', 'yaml', 'toml', 'pickle'):
            fi = self.test_data_dir.get_fileinfo(f'test_data_1_{fmt}.{fmt}')
            example = {
                'a': 1,
                'b': '2',
                'c': {
                    'd': 'ddddd'
                }
            }
            fi.dump(example, fmt)
            data = fi.load(fmt)
            self.assertDictEqual(example, data)

    def test_extra_auto_format(self):
        example = {
            'a': 1,
            'b': '2',
            'c': {
                'd': 'ddddd'
            }
        }

        for fmt in ('json', 'json5', 'yaml', 'toml'):
            fi = self.test_data_dir.get_fileinfo(f'test_data_2_{fmt}.{fmt}')
            fi.dump(example)
            data = fi.load()
            self.assertDictEqual(example, data)

        for fmt in ('pickle', ):
            fi = self.test_data_dir.get_fileinfo(f'test_data_2_{fmt}.{fmt}')
            with self.assertRaises(RuntimeError):
                fi.dump(example)
            with self.assertRaises(RuntimeError):
                data = fi.load()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        unittest.main()
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()

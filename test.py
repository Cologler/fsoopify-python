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

    def test_ext_json(self):
        fi = FileInfo('abc.json')
        example = { 'a': 1, 'b': '2' }
        fi.dump('json', example)
        data = fi.load('json')
        self.assertDictEqual(example, data)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        unittest.main()
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()

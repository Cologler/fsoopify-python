# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import tempfile

from fsoopify import *

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

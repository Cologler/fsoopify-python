# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os

from fsoopify import FileInfo

def test_file_get_parent():
    a_topdir_relpath = [os.pardir] * 50
    ofile = FileInfo(os.path.join(*a_topdir_relpath))
    assert ofile.get_parent() is None


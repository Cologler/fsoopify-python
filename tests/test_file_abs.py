# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys

import pytest

from fsoopify import FileInfo

NT = sys.platform == 'win32'

@pytest.mark.skipif(not NT, reason="only run on windows")
def test_file_get_parent_nt():
    ofile = FileInfo('c:\\d\\e')
    assert ofile.get_parent().path == 'c:\\d'
    assert ofile.get_parent(1).path == 'c:\\d'
    assert ofile.get_parent(2).path == 'c:'
    assert ofile.get_parent(3) is None

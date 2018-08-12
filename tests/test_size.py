# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from fsoopify.size import Size

def test_size_value():
    assert Size(10000000) == 10000000

def test_size_str():
    assert str(Size(10000000)) == '9.537 MB'

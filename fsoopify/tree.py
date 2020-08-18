# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from contextlib import ExitStack

class ContentTree(dict):
    def __init__(self, iterable=None):
        super().__init__(iterable or ())
        self._es = ExitStack()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._es.__exit__(exc_type, exc_val, exc_tb)

    def set_context(self, key, value):
        self[key] = self._es.enter_context(value)

# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
# a package use for test Path.from_caller_? api
# ----------

from fsoopify import Path

path_caller_file = Path.from_caller_file()
path_caller_module_root = Path.from_caller_module_root()

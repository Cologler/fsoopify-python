# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
import os
import importlib

from fsoopify import Path

def test_path_from_argv():
    path = Path.from_argv()
    assert path == sys.argv[0]

def test_path_from_main_file():
    path = Path.from_main_file()
    assert path.endswith('.py') # should run by pytest

def _get_example_modules():
    yield importlib.import_module('ex_module_2')
    yield importlib.import_module('ex_package_1')
    yield importlib.import_module('ex_package_1.ex_module_1')
    yield importlib.import_module('ex_package_1.ex_package_2')
    yield importlib.import_module('ex_package_1.ex_package_2.ex_module_1')


def test_path_from_caller_file():
    path = Path.from_caller_file()
    assert path == __file__

    dot = os.path.abspath('.')
    caller_files = [m.path_caller_file for m in _get_example_modules()]
    assert caller_files == [
        os.path.join(dot, 'tests', 'ex_module_2.py'),
        os.path.join(dot, 'tests', 'ex_package_1', '__init__.py'),
        os.path.join(dot, 'tests', 'ex_package_1', 'ex_module_1.py'),
        os.path.join(dot, 'tests', 'ex_package_1', 'ex_package_2', '__init__.py'),
        os.path.join(dot, 'tests', 'ex_package_1', 'ex_package_2', 'ex_module_1.py'),
    ]

def test_path_from_caller_module_root():
    path = Path.from_caller_module_root()
    assert path == __file__

    dot = os.path.abspath('.')
    caller_module_root = [m.path_caller_module_root for m in _get_example_modules()]
    assert caller_module_root == [
        os.path.join(dot, 'tests', 'ex_module_2.py'),
        os.path.join(dot, 'tests', 'ex_package_1', '__init__.py'),
        os.path.join(dot, 'tests', 'ex_package_1', '__init__.py'),
        os.path.join(dot, 'tests', 'ex_package_1', '__init__.py'),
        os.path.join(dot, 'tests', 'ex_package_1', '__init__.py'),
    ]

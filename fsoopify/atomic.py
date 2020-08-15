# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import io
import shutil
import types

import atomicwrites

class _ProxyDescriptor:
    def __init__(self, name=None):
        self._name = name

    def __get__(self, obj, cls=None):
        return getattr(obj.__io, self._name)

    def __set__(self, obj, value) -> None:
        setattr(obj.__io, self._name)

    def __delete__(self, obj) -> None:
        # if an object defines `__set__()` or `__delete__()`,
        # it is considered a data descriptor.
        delattr(obj.__io, self._name)

    def __set_name__(self, owner_cls, name):
        # New in version 3.6
        # only called implicitly as part of the type constructor
        self._name = name


class IOProxyBase:
    def __init__(self, gen):
        self.__gen = gen
        self.__io = gen.__enter__()

    def __enter__(self):
        return self.__io

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.__gen.__exit__(exc_type, exc_val, exc_tb)

    def __getattr__(self, name):
        return getattr(self.__io, name)

    __iter__ = _ProxyDescriptor()

for name in set(dir(io.TextIOWrapper)) | set(dir(io.BufferedRandom)):
    if not name.startswith('__'):
        setattr(IOProxyBase, name, _ProxyDescriptor(name))


class BufferedIOProxy(IOProxyBase, io.BufferedIOBase):
    pass


class TextIOProxy(IOProxyBase, io.TextIOBase):
    pass


def open_atomic(path: str, mode : str, **kwargs):
    if 'r' in mode and '+' not in mode:
        # readonly mode, open direct.
        return open(path, mode, **kwargs)

    overwrite = 'x' not in mode

    atomic_mode = 'w'
    if 'b' in mode:
        atomic_mode += 'b'

    dest = atomicwrites.atomic_write(path, mode=atomic_mode,
        overwrite=overwrite,
        **kwargs)
    if 'b' in mode:
        dest = BufferedIOProxy(dest)
    else:
        dest = TextIOProxy(dest)

    try:
        if 'w' not in mode:
            # read+write or append
            with open(path) as reader:
                shutil.copyfileobj(reader, dest)

            if 'a' not in mode:
                # read+write
                dest.seek(0)

        return dest
    except Exception:
        dest.close()
        raise

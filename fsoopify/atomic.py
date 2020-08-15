# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import io
import shutil
import types
import contextlib

import portalocker
import atomicwrites

class _ProxyDescriptor:
    def __init__(self, name=None):
        self._name = name

    def __get__(self, obj, cls=None):
        return getattr(obj._baseio, self._name)

    def __set__(self, obj, value) -> None:
        setattr(obj._baseio, self._name)

    def __delete__(self, obj) -> None:
        # if an object defines `__set__()` or `__delete__()`,
        # it is considered a data descriptor.
        delattr(obj._baseio, self._name)

    def __set_name__(self, owner_cls, name):
        # New in version 3.6
        # only called implicitly as part of the type constructor
        self._name = name


class IOProxyBase:
    def __init__(self, gen):
        self._gen = gen
        self._baseio = gen.__enter__()
        self._append_mode = False # for append mode

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._gen.__exit__(exc_type, exc_val, exc_tb)

    def write(self, *args, **kwargs):
        pos = None
        if self._append_mode and  self._baseio.seekable():
            pos = self._baseio.tell()
            self._baseio.seek(0, io.SEEK_END)
        try:
            return self._baseio.write(*args, **kwargs)
        finally:
            if pos is not None:
                self._baseio.seek(pos)

    __iter__ = _ProxyDescriptor()

for name in set(dir(io.TextIOWrapper)) | set(dir(io.BufferedRandom)):
    if not name.startswith('__') and not hasattr(IOProxyBase, name):
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
    if '+' in mode or 'w' not in mode:
        atomic_mode += '+'
    if 'b' in mode:
        atomic_mode += 'b'

    dest = atomicwrites.atomic_write(path, mode=atomic_mode, overwrite=overwrite, **kwargs)

    if 'b' in mode:
        dest = BufferedIOProxy(dest)
    else:
        dest = TextIOProxy(dest)

    try:
        if 'w' not in mode and 'x' not in mode:
            if os.path.isfile(path):
                with contextlib.suppress(FileNotFoundError):
                    # read+write or append
                    read_mode = 'r'
                    if 'b' in mode:
                        read_mode += 'b'
                    with open(path, read_mode) as reader:
                        portalocker.lock(reader, portalocker.LOCK_EX) # ensure file not change when we clone.
                        shutil.copyfileobj(reader, dest)

                if 'a' in mode:
                    dest._append_mode = True
                else:
                    # read+write
                    dest.seek(0)
        return dest
    except Exception:
        dest.close()
        raise

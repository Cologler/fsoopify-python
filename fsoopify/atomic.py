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

from .openers import ContextManagerFileOpener


class COWAtomicWriter(atomicwrites.AtomicWriter):
    'copy on write atomic writer'

    def get_fileobject(self, final_mode, lock, **kwargs):
        with super().get_fileobject(**kwargs) as tmp_fp:
            name = tmp_fp.name
            if os.path.isfile(self._path):
                with contextlib.suppress(FileNotFoundError):
                    # read+write or append
                    with open(self._path, 'rb') as reader:
                        if lock:
                            portalocker.lock(reader, portalocker.LOCK_EX)
                        shutil.copyfileobj(reader, tmp_fp)

        return io.open(name, final_mode, **kwargs)


def open_atomic(path: str, mode: str, lock: bool=False, **kwargs):
    if 'r' in mode and '+' not in mode:
        # readonly mode
        raise RuntimeError

    # overwrite mean writeable if the file exists.
    # if not 'x' or 'x+',
    # we should be able to write the file.
    overwrite = 'x' not in mode
    atomic_mode = mode.replace('x', 'w')

    # if mode is 'r+', 'a', 'a+',
    # we should clone the file before we write.
    if 'r' in mode or 'a' in mode:
        kwargs['mode'] = 'wb'
        kwargs['final_mode'] = atomic_mode
        kwargs['lock'] = lock
        writer_cls = COWAtomicWriter
    else:
        kwargs['mode'] = atomic_mode
        writer_cls = atomicwrites.AtomicWriter

    cm = writer_cls(path, overwrite=overwrite, **kwargs).open()
    return ContextManagerFileOpener(cm)

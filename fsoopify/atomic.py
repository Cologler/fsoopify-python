# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import io
import shutil

import atomicwrites

class AtomicWriterProxy:
    def __init__(self, gen):
        self.__gen = gen
        self.__io = gen.__enter__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.__gen.__exit__(exc_type, exc_val, exc_tb)

    def __getattr__(self, name):
        return getattr(self.__io, name)


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
    dest = AtomicWriterProxy(dest)

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

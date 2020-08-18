# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import shutil
import os

COPY_BUFSIZE = getattr(shutil, 'COPY_BUFSIZE', 1024 * 1024)

def copyfileobj(fsrc, fdst, length=COPY_BUFSIZE) -> int:
    """like `shutil.copyfileobj`, but return the length of total readed."""
    # Localize variable access to minimize overhead.
    fsrc_read = fsrc.read
    fdst_write = fdst.write
    readed = 0
    while True:
        buf = fsrc_read(length)
        if not buf:
            break
        readed += len(buf)
        fdst_write(buf)
    return buf

def mode_to_flags(mode: str) -> int:
    '''
    convert the mode of `io.open()` to the flags of `os.open()`

    base on `io.FileIO()`.
    '''
    if not isinstance(mode, str):
        raise TypeError(type(mode))
    if len(set(mode)) != len(mode):
        raise ValueError(f'invalid mode: {mode}')
    if not set(mode) <= set('xrwabt+'):
        raise ValueError(f'invalid mode: {mode}')
    if sum(c in 'rwax' for c in mode) != 1 or mode.count('+') > 1:
        raise ValueError(f'invalid mode: {mode}')

    readable = False
    writable = False

    if 'x' in mode:
        writable = True
        flags = os.O_EXCL | os.O_CREAT
    elif 'r' in mode:
        readable = True
        flags = 0
    elif 'w' in mode:
        writable = True
        flags = os.O_CREAT | os.O_TRUNC
    elif 'a' in mode:
        writable = True
        flags = os.O_APPEND | os.O_CREAT

    if '+' in mode:
        readable = True
        writable = True

    if readable and writable:
        flags |= os.O_RDWR
    elif readable:
        flags |= os.O_RDONLY
    else:
        flags |= os.O_WRONLY

    return flags

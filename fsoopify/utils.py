# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import shutil

def copyfileobj(fsrc, fdst, length=shutil.COPY_BUFSIZE) -> int:
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

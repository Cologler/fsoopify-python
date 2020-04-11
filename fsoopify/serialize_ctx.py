# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from contextlib import contextmanager

from .serialize import *

class Context:
    data = None
    save_on_exit = True

@contextmanager
def load_context(f, format: str=None, *, load_kwargs: dict, dump_kwargs: dict, lock: bool):
    if lock:
        import portalocker

    serializer = get_serializer(f, format)

    is_exists = f.is_file()
    fp = f.open('r+b' if is_exists else 'wb')
    if lock:
        portalocker.lock(fp, portalocker.LOCK_EX)
    if is_exists:
        data = serializer.loadf(fp, options={})
    else:
        data = None

    ctx = Context()
    ctx.data = data
    yield ctx
    data = ctx.data

    if ctx.save_on_exit:
        if data is not None:
            buf = serializer.dumpb(data, options={
                'origin_kwargs': dump_kwargs
            })
            fp.seek(0)
            fp.write(buf)
            fp.truncate()
            fp.close()
        else:
            fp.close()
            if f.is_file():
                f.delete()

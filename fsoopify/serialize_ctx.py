# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
from contextlib import contextmanager

from .serialize import *

class Context:
    data = None
    save_on_exit = True

    def __init__(self, file_info, *, serializer, load_kwargs: dict, dump_kwargs: dict, lock: bool):
        super().__init__()
        self._file_info = file_info
        self._serializer = serializer
        self._load_kwargs = load_kwargs
        self._dump_kwargs = dump_kwargs
        self._lock = lock
        # states:
        self._lock_ctx = None
        self._fp = None

    def __enter__(self):
        is_exists = self._file_info.is_file()
        try:
            self._fp = self._file_info.open('r+b' if is_exists else 'wb')
            self._lock_ctx = self._lock(self._file_info, self._fp)
            self._lock_ctx.__enter__()
            if is_exists:
                self.data = self._serializer.loadf(self._fp, options={
                    'origin_kwargs': self._load_kwargs
                })
            else:
                self.data = None
        except Exception:
            self._cleanup()
            raise
        return self

    def _cleanup(self):
        if self._lock_ctx is not None:
            self._lock_ctx.__exit__(*sys.exc_info())
            self._lock_ctx = None
        if self._fp is not None:
            self._fp.close()
            self._fp = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_val is None and self.save_on_exit:
                assert self._fp is not None
                if self.data is None:
                    self._fp.close()
                    if self._file_info.is_file():
                        self._file_info.delete()
                else:
                    buf = self._serializer.dumpb(self.data, options={
                        'origin_kwargs': self._dump_kwargs
                    })
                    self._fp.seek(0)
                    self._fp.write(buf)
                    self._fp.truncate()
                    self._fp.close()
                self._fp = None

        finally:
            self._cleanup()

@contextmanager
def lock_with_nop(fi, fp):
    yield

@contextmanager
def lock_with_portalocker(fi, fp):
    import portalocker
    portalocker.lock(fp, portalocker.LOCK_EX)
    yield

def load_context(f, format: str=None, *, load_kwargs: dict, dump_kwargs: dict, lock: bool):
    if lock:
        if lock is True:
            lock = lock_with_portalocker
    else:
        lock = lock_with_nop

    serializer = get_serializer(f, format)

    ctx = Context(f,
        serializer=serializer,
        load_kwargs=load_kwargs, dump_kwargs=dump_kwargs,
        lock=lock
    )
    return ctx

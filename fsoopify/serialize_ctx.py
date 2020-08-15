# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
from contextlib import contextmanager, suppress

from .serialize import *

class Context:
    data = None
    save_on_exit = True

    def __init__(self, file_info, *, serializer, load_kwargs: dict, dump_kwargs: dict, lock: bool, atomic: bool):
        super().__init__()
        self._file_info = file_info
        self._serializer = serializer
        self._load_kwargs = load_kwargs
        self._dump_kwargs = dump_kwargs
        self._lock = lock
        self._atomic = atomic
        # states:
        self._lock_ctx = None
        self._openfd_ctx = None
        self._fd = None

    def __enter__(self):
        def _read_data_from(fp):
            self.data = self._serializer.loadf(fp, options={
                'origin_kwargs': self._load_kwargs
            })

        try:
            is_exists = self._file_info.is_file()

            if self._atomic:
                self._openfd_ctx = self._file_info.open('wb', atomic=True)
            else:
                self._openfd_ctx = self._file_info.open_or_create('r+b')

            self._fd = self._openfd_ctx.__enter__()

            self._lock_ctx = self._lock(self._file_info, self._fd)
            self._lock_ctx.__enter__()

            if is_exists:
                if self._atomic:
                    with self._file_info.open_for_read_bytes() as fp:
                        _read_data_from(fp)
                else:
                    self._fd.seek(0)
                    _read_data_from(self._fd)

        except Exception:
            self._cleanup()
            raise

        return self

    def _cleanup(self):
        if self._lock_ctx is not None:
            self._lock_ctx.__exit__(*sys.exc_info())
            self._lock_ctx = None

        if self._fd is not None:
            assert self._openfd_ctx is not None
            self._fd = None

        if self._openfd_ctx is not None:
            self._openfd_ctx.__exit__(*sys.exc_info())
            self._openfd_ctx = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        remove_file = False
        try:
            # only save if no exceptions:
            if exc_val is None and self.save_on_exit and self._fd:
                self._fd.seek(0)
                if self.data is None:
                    remove_file = True
                else:
                    buf = self._serializer.dumpb(self.data, options={
                        'origin_kwargs': self._dump_kwargs
                    })
                    self._fd.write(buf)
                self._fd.truncate()
        finally:
            self._cleanup()

        if remove_file and self._file_info.is_file():
            self._file_info.delete()

@contextmanager
def lock_with_nop(fi, fp):
    yield

@contextmanager
def lock_with_portalocker(fi, fp):
    import portalocker
    portalocker.lock(fp, portalocker.LOCK_EX)
    yield

@contextmanager
def lock_with_filelock(fi, fp):
    import filelock
    with filelock.FileLock(fi.path + '.lock'):
        yield

def load_context(f, format: str=None, *, load_kwargs: dict, dump_kwargs: dict, lock: bool, atomic: bool):
    if lock:
        if lock is True:
            lock = lock_with_filelock if atomic else lock_with_portalocker
    else:
        lock = lock_with_nop

    serializer = get_serializer(f, format)

    ctx = Context(f,
        serializer=serializer,
        load_kwargs=load_kwargs, dump_kwargs=dump_kwargs,
        lock=lock,
        atomic=atomic,
    )
    return ctx

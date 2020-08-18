# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
from contextlib import contextmanager, suppress

import portalocker
import filelock

from .serialize import *


@contextmanager
def lock_with_portalocker(fp):
    'use `portalocker.lock` as context manager.'
    import portalocker
    portalocker.lock(fp, portalocker.LOCK_EX)
    yield


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
        self._lock_cm = None
        self._fp_cm = None
        self._fp = None

    def __enter__(self):
        def _read_data_from(fp):
            self.data = self._serializer.loadf(fp, options={
                'origin_kwargs': self._load_kwargs
            })

        is_exists = self._file_info.is_file()
        # we did not want to copy data from src on atomic mode
        mode = 'wb' if self._atomic else 'r+b'

        try:
            if self._lock and self._atomic:
                self._lock_cm = filelock.FileLock(self._file_info.path + '.lock')
                self._lock_cm.__enter__()

            self._fp_cm = self._file_info.open(mode, atomic=self._atomic, or_create=True)
            self._fp = self._fp_cm.__enter__()

            if self._lock and not self._atomic:
                self._lock_cm = lock_with_portalocker(self._fp)
                self._lock_cm.__enter__()

            if is_exists:
                if self._atomic:
                    with self._file_info.open_for_read_bytes() as fp:
                        _read_data_from(fp)
                else:
                    self._fp.seek(0)
                    _read_data_from(self._fp)

        except:
            self._cleanup()
            raise

        return self

    def _cleanup(self):
        if self._lock_cm is not None:
            self._lock_cm.__exit__(*sys.exc_info())
            self._lock_cm = None

        if self._fp is not None:
            assert self._fp_cm is not None
            self._fp = None

        if self._fp_cm is not None:
            self._fp_cm.__exit__(*sys.exc_info())
            self._fp_cm = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        remove_file = False
        try:
            # only save if no exceptions:
            if exc_val is None and self.save_on_exit and self._fp:
                self._fp.seek(0)
                if self.data is None:
                    remove_file = True
                else:
                    buf = self._serializer.dumpb(self.data, options={
                        'origin_kwargs': self._dump_kwargs
                    })
                    self._fp.write(buf)
                self._fp.truncate()
        finally:
            self._cleanup()

        if remove_file and self._file_info.is_file():
            self._file_info.delete()


def load_context(f, format: str=None, *, load_kwargs: dict, dump_kwargs: dict, lock: bool, atomic: bool):
    serializer = get_serializer(f, format)

    ctx = Context(f,
        serializer=serializer,
        load_kwargs=load_kwargs, dump_kwargs=dump_kwargs,
        lock=lock,
        atomic=atomic,
    )
    return ctx

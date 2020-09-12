# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
from contextlib import contextmanager, suppress

import filelock

from .serialize import *

def exit_ctxmgr(cm) -> None:
    'exit a context manager if it is not `None`, return `None`.'
    if cm is not None:
        cm.__exit__(*sys.exc_info())

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
        self._writer_cm = None
        self._writer = None

    def __enter__(self):
        def _read_data_from(fp):
            self.data = self._serializer.loadf(fp, options={
                'origin_kwargs': self._load_kwargs
            })

        if self._lock:
            self._lock_cm = filelock.FileLock(self._file_info.path + '.lock')
            self._lock_cm.__enter__()

        reader_cm = None
        try:
            reader_cm = self._file_info.open('r+b')
            try:
                reader = reader_cm.__enter__()
            except FileNotFoundError:
                reader_cm = exit_ctxmgr(reader_cm)
            else:
                _read_data_from(reader)

                if not self._atomic:
                    self._writer_cm = reader_cm
                    self._writer = reader
                else:
                    reader_cm = exit_ctxmgr(reader_cm)
        except:
            self._cleanup()
            raise

        return self

    def _open_for_write(self):
        if self._writer is None:
            assert self._writer_cm is None
            try:
                self._writer_cm = self._file_info.open('w+b', atomic=self._atomic)
                self._writer = self._writer_cm.__enter__()
            except:
                self._writer = exit_ctxmgr(self._writer)
                self._writer_cm = exit_ctxmgr(self._writer_cm)
                raise
        else: # opened for read
            self._writer.seek(0)
        return self._writer

    def _cleanup_cm(self, cm) -> None:
        if cm is not None:
            cm.__exit__(*sys.exc_info())
        return None

    def _cleanup(self):
        self._writer_cm = exit_ctxmgr(self._writer_cm)
        self._writer = None
        self._lock_cm = exit_ctxmgr(self._lock_cm)

    def __exit__(self, exc_type, exc_val, exc_tb):
        remove_file = False
        try:
            # only save if no exceptions:
            if exc_val is None and self.save_on_exit:
                fp = self._open_for_write()
                if self.data is None:
                    remove_file = True
                else:
                    buf = self._serializer.dumpb(self.data, options={
                        'origin_kwargs': self._dump_kwargs
                    })
                    fp.write(buf)
                fp.truncate()
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

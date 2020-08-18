# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import ABC, abstractmethod
import os

import portalocker

from .utils import mode_to_flags

class FileOpenerBase(ABC):
    'the base file opener'

    __slots__ = ('_cm')

    @abstractmethod
    def _get_contextmanager(self):
        raise NotImplementedError

    def __enter__(self):
        self._cm = self._get_contextmanager()
        return self._cm.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        rv = self._cm.__exit__(exc_type, exc_val, exc_tb)
        del self._cm
        return rv


class FileOpener(FileOpenerBase):
    'the file opener for builtin `open`'

    __slots__ = ('_lock', '_openargs')

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._lock = kwargs.pop('lock', False)
        self._openargs = (args, kwargs)

    def _get_contextmanager(self):
        args, kwargs = self._openargs
        del self._openargs
        fp = open(*args, **kwargs)
        if self._lock:
            try:
                portalocker.lock(fp, portalocker.LOCK_EX)
            except:
                fp.close()
                raise
        return fp


class ContextManagerFileOpener(FileOpenerBase):
    'the file opener for any context manager.'

    def __init__(self, cm):
        self._cm = cm

    def _get_contextmanager(self):
        return self._cm

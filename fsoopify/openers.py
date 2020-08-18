# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import ABC, abstractmethod

import portalocker

class FileOpenerBase(ABC):
    __slots__ = ('_openargs', '_ctx')

    def __init__(self, *args, **kwargs):
        self._openargs = (args, kwargs)

    @abstractmethod
    def _get_context(self, args, kwargs):
        raise NotImplementedError

    def __enter__(self):
        args, kwargs = self._openargs
        del self._openargs
        self._ctx = self._get_context(args, kwargs)
        return self._ctx.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        rv = self._ctx.__exit__(exc_type, exc_val, exc_tb)
        del self._ctx
        return rv


class FileOpener(FileOpenerBase):
    __slots__ = ('_lock')

    def __init__(self, *args, lock, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = lock

    def _get_context(self, args, kwargs):
        fp = open(*args, **kwargs)
        if self._lock:
            try:
                portalocker.lock(fp, portalocker.LOCK_EX)
            except:
                fp.close()
                raise
        return fp

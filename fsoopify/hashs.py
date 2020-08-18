# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import binascii
import hashlib

ALGORITHMS = set(hashlib.algorithms_available)
ALGORITHMS.add('crc32')

class Crc32Proxy:
    def __init__(self):
        self._value = 0

    def update(self, buffer):
        self._value = binascii.crc32(buffer, self._value)

    def hexdigest(self):
        return "%08x" % self._value

def _create(algorithm: str):
    if algorithm == 'crc32':
        return Crc32Proxy()
    return hashlib.new(algorithm)

class Hasher:
    def __init__(self, path: str, algorithms: Tuple[str, ...], *, blocksize=1024 * 64):
        for algorithm in algorithms:
            if not algorithm in ALGORITHMS:
                raise ValueError(f'unsupport algorithm: {algorithm}')

        self._path = path
        self._algorithms = algorithms
        self._blocksize = blocksize
        self._result = None
        self._total_read = 0

        # lazy init:
        self._total_size = None
        self._stream = None
        self._hashers = None

    def __enter__(self):
        self._stream = open(self._path, 'rb')
        self._hashers = [_create(x) for x in self._algorithms]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stream.close()

    def read_block(self) -> bool:
        if self._result is not None:
            return False

        buffer = self._stream.read(self._blocksize)
        if buffer:
            self._total_read += len(buffer)
            for m in self._hashers:
                m.update(buffer)
        else:
            self._result = tuple(m.hexdigest() for m in self._hashers)

        return True

    @property
    def total_read(self):
        return self._total_read

    @property
    def total_size(self):
        if self._total_size is None:
            import os
            self._total_size = os.path.getsize(self._path)
        return self._total_size

    @property
    def progress(self):
        return self._total_read / self.total_size

    @property
    def result(self) -> Tuple[str, ...]:
        if self._result is None:
            raise RuntimeError
        return self._result
        
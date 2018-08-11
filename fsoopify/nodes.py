#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
import os
from abc import abstractmethod
from .paths import Path

class FormatNotFoundError(Exception):
    pass


class SerializeError(Exception):
    pass


class NodeInfo:
    ''' the abstract base class for file system node. '''

    def __init__(self, path):
        self._path: Path = Path(path)

    def __str__(self):
        return str(self._path)

    def __repr__(self):
        return '{}(\'{}\')'.format(type(self).__name__, self._path)

    @property
    def path(self) -> Path:
        '''
        return a Path object.
        '''
        return self._path

    def rename(self, dest_path: str):
        '''
        use `os.rename()` to move the node.
        '''
        if not isinstance(dest_path, str):
            raise TypeError
        os.rename(self._path, dest_path)
        self._path = Path(dest_path)

    def get_parent(self):
        '''
        get parent dir as a `DirectoryInfo`.

        return `None` if self is top.
        '''
        parent_path = self.path.dirname
        if self._path.is_abspath():
            parent_path = self.path.dirname
            if parent_path == self.path:
                return None
        else:
            if parent_path == '':
                if self._path == os.path.curdir:
                    parent_path = os.path.pardir
                elif self._path == os.path.pardir:
                    parent_path = os.path.join(os.path.pardir, self._path)
                else:
                    parent_path = os.path.curdir
            elif parent_path == '..':
                parent_path = os.path.join(os.path.pardir, self._path)
        if parent_path:
            return DirectoryInfo(parent_path)

    @staticmethod
    def from_path(path):
        '''
        create from path.

        return `None` if path is not exists.
        '''
        if os.path.isdir(path):
            return DirectoryInfo(path)

        if os.path.isfile(path):
            return FileInfo(path)

        return None

    @staticmethod
    def from_cwd():
        '''
        get a `DirectoryInfo` by `os.getcwd()`
        '''
        return DirectoryInfo(os.getcwd())

    @staticmethod
    def from_argv0():
        '''
        get a `FileInfo` by `sys.argv[0]`
        '''
        return FileInfo(sys.argv[0])

    # common methods

    def is_exists(self):
        '''
        get whether the node is exists on disk.
        '''
        return os.path.exists(self._path)

    def is_directory(self):
        '''
        get whether the node is a exists directory.
        '''
        return False

    def is_file(self):
        '''
        get whether the node is a exists file.
        '''
        return False

    # abstract methods

    @abstractmethod
    def delete(self):
        ''' remove the node from disk. '''
        raise NotImplementedError

    @abstractmethod
    def create_hardlink(self, dest_path: str):
        ''' create hardlink for the node. '''
        raise NotImplementedError


class FileInfo(NodeInfo):

    def open(self, mode='r', *, buffering=-1, encoding=None, newline=None, closefd=True):
        ''' open the file. '''
        return open(self._path,
                    mode=mode,
                    buffering=buffering,
                    encoding=encoding,
                    newline=newline,
                    closefd=closefd)

    @property
    def size(self):
        ''' get file size. '''
        return os.path.getsize(self.path)

    def write(self, data, *, mode=None, buffering=-1, encoding=None, newline=None):
        ''' write data into the file. '''
        if mode is None:
            mode = 'w' if isinstance(data, str) else 'wb'
        with self.open(mode=mode, buffering=buffering, encoding=encoding, newline=newline) as fp:
            return fp.write(data)

    def read(self, mode='r', *, buffering=-1, encoding=None, newline=None):
        ''' read data from the file. '''
        with self.open(mode=mode, buffering=buffering, encoding=encoding, newline=newline) as fp:
            return fp.read()

    def write_text(self, text: str, *, encoding='utf-8', append=True):
        ''' write text into the file. '''
        mode = 'a' if append else 'w'
        return self.write(text, mode=mode, encoding=encoding)

    def write_bytes(self, data: bytes, *, append=True):
        ''' write bytes into the file. '''
        mode = 'ab' if append else 'wb'
        return self.write(data, mode=mode)

    def copy_to(self, dest_path: str, buffering: int = -1):
        ''' copy the file to dest path. '''
        with open(self._path, 'rb', buffering=buffering) as source:
            # use x mode to ensure dest does not exists.
            with open(dest_path, 'xb') as dest:
                for buffer in source:
                    dest.write(buffer)

    def read_text(self, encoding='utf-8') -> str:
        ''' read all text into memory. '''
        with self.open('r', encoding=encoding) as fp:
            return fp.read()

    def read_bytes(self) -> bytes:
        ''' read all bytes into memory. '''
        with self.open('rb') as fp:
            return fp.read()

    # override common methods

    def is_exists(self) -> bool:
        return self.is_file()

    def is_file(self) -> bool:
        ''' check if this is a exists file. '''
        return os.path.isfile(self._path)

    # override @abstractmethod

    def delete(self):
        ''' remove the file from disk. '''
        os.remove(self._path)

    def create_hardlink(self, dest_path: str):
        ''' create hardlink for the file. '''
        os.link(self._path, dest_path)

    # load/dump system.

    _REGISTERED_SERIALIZERS = {}

    def load(self, fmt=None, *, kwargs={}):
        '''
        deserialize object from the file.

        auto detect format by file extension name if `fmt` is None.
        for example, `.json` will detect as `json`.

        * raise `FormatNotFoundError` on unknown format.
        * raise `SerializeError` on any exceptions.
        '''
        if fmt is None:
            fmt = self._detect_fmt()
        serializer = self._load_serializer(fmt)
        try:
            return serializer.load(self, kwargs)
        except Exception as err:
            raise SerializeError(err)

    def dump(self, obj, fmt=None, *, kwargs={}):
        '''
        serialize the `obj` into file.

        * raise `FormatNotFoundError` on unknown format.
        * raise `SerializeError` on any exceptions.
        '''
        if fmt is None:
            fmt = self._detect_fmt()
        serializer = self._load_serializer(fmt)
        try:
            return serializer.dump(self, obj, kwargs)
        except Exception as err:
            raise SerializeError(err)

    def _detect_fmt(self):
        fmt_table = {
            '.json' : 'json',
            '.json5': 'json5',
            '.yaml' : 'yaml',
            '.toml' : 'toml'
        }
        ext = self.path.name.ext
        try:
            return fmt_table[ext.lower()]
        except KeyError:
            raise RuntimeError(f'cannot detect format from ext "{ext}".')

    @classmethod
    def _load_serializer(cls, fmt):
        if not isinstance(fmt, str):
            raise TypeError(f'format must be str.')

        if fmt not in cls._REGISTERED_SERIALIZERS:
            import importlib
            try:
                importlib.import_module('.extras.' + fmt, 'fsoopify')
            except ImportError:
                cls._REGISTERED_SERIALIZERS[fmt] = None

        typ = cls._REGISTERED_SERIALIZERS.get(fmt)
        if typ is None:
            raise FormatNotFoundError(f'unknown format: {fmt}')
        return typ()

    @classmethod
    def register_format(cls, fmt):
        ''' register a serializer for load and dump. '''
        def w(c):
            cls._REGISTERED_SERIALIZERS[fmt] = c
            return c
        return w


class DirectoryInfo(NodeInfo):

    def create(self):
        ''' create directory. '''
        os.mkdir(self.path)

    def ensure_created(self):
        ''' ensure the directory was created. '''
        if not self.is_directory():
            self.create()

    def iter_items(self, depth: int = 1):
        '''
        get items from directory.
        '''
        if depth is not None and not isinstance(depth, int):
            raise TypeError
        def itor(root, d):
            if d is not None:
                d -= 1
                if d < 0:
                    return
            for name in os.listdir(root):
                path = os.path.join(root, name)
                node = NodeInfo.from_path(path)
                yield node
                if isinstance(node, DirectoryInfo):
                    yield from itor(path, d)
        yield from itor(self._path, depth)

    def list_items(self, depth: int = 1):
        '''
        get items from directory.
        '''
        return list(self.iter_items(depth))

    def get_fileinfo(self, name: str):
        '''
        get a `FileInfo` for a file (without create actual file).
        '''
        return FileInfo(os.path.join(self._path, name))

    def create_file(self, name: str, generate_unique_name: bool = False):
        '''
        create a `FileInfo` for a new file.

        if the file was exists, and `generate_unique_name` if `False`, raise `FileExistsError`.

        the op does mean the file is created on disk.
        '''
        def enumerate_name():
            yield name
            index = 0
            while True:
                index += 1
                yield f'{name} ({index})'
        for n in enumerate_name():
            path = os.path.join(self._path, n)
            if os.path.exists(path):
                if not generate_unique_name:
                    raise FileExistsError
            return FileInfo(path)

    create_fileinfo = create_file # keep old name

    # override common methods

    def is_exists(self) -> bool:
        return self.is_directory()

    def is_directory(self) -> bool:
        ''' check if this is a exists directory. '''
        return os.path.isdir(self._path)

    # override @abstractmethod

    def delete(self):
        ''' remove the directory from disk. '''
        os.rmdir(self._path)

    def create_hardlink(self, dest_path: str):
        ''' create hardlink for the directory (includes childs). '''

        # self
        dirinfo = DirectoryInfo(dest_path)
        dirinfo.ensure_created()

        # child
        for item in self.list_items():
            item.create_hardlink(os.path.join(dest_path, item.path.name))

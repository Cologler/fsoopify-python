# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import ABC, abstractmethod
from typing import Optional

import anyser
from anyser import FormatNotFoundError, NotSupportError, SerializeError
from anyser.abc import ISerializer

def resolve_format(file_info, format: Optional[str]) -> str:
    available_formats = set(anyser.get_available_formats())
    if format is None:
        ext = file_info.path.name.ext.lower()
        if ext in available_formats:
            return ext
        name = file_info.path.name.lower()
        if name in available_formats:
            return name
        raise FormatNotFoundError(f'Cannot detect format from file {file_info!r}')
    else:
        if format in available_formats:
            return format
        raise FormatNotFoundError(f'unknown format: {format}')

def load(file_info, format=None, *, kwargs={}):
    format = resolve_format(file_info, format)
    with file_info.open('rb') as fp:
        return anyser.loadf(fp, format, origin_kwargs=kwargs)

def dump(file_info, obj, format=None, *, kwargs={}, atomic=False):
    format = resolve_format(file_info, format)
    data = anyser.dumpb(obj, format, origin_kwargs=kwargs)
    file_info.write_bytes(data, append=False, atomic=atomic)

@anyser.register_format('pipfile')
class PipfileSerializer(ISerializer):
    format_name = 'pipfile'

    def __init__(self):
        super().__init__()
        import pipfile
        self.pipfile = pipfile

    def loads(self, s, options):
        raise NotSupportError

    def loadb(self, b, options):
        raise NotSupportError

    def loadf(self, fp, options):
        pipfile = self.pipfile.load(fp.fileno())
        try:
            fp.close()
            # first fp.close() will raise IOError: Bad file descriptor beacuse pipfile.load close fd.
            # catch here to prevent raise on outside
        except IOError:
            pass
        return pipfile.data

    def dumpf(self, obj, fp, options):
        raise NotSupportError('dump `pipfile` is not supported.')

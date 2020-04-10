# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import ABC, abstractmethod
from typing import Optional

import anyser
import anyser.core
from anyser.abc import ISerializer
from anyser.core import register_format
from anyser.err import FormatNotFoundError, SerializeError, NotSupportError

def load(file_info, format=None, *, kwargs={}):
    serializer = get_serializer(file_info, format)
    with file_info.open('rb') as fp:
        return serializer.loadf(fp, options={})

def dump(file_info, obj, format=None, *, kwargs={}):
    serializer = get_serializer(file_info, format)
    data = serializer.dumpb(obj, options={
        'origin_kwargs': kwargs.copy()
    })
    file_info.write_bytes(data, append=False)

def get_serializer(file_info, format: Optional[str]):
    if not isinstance(format, (str, type(None))):
        raise TypeError(f'format must be str.')

    if format is None:
        ext = file_info.path.name.ext.lower()
        serializer = anyser.core.find_serializer(file_info.path.name.ext.lower())
        if serializer is None:
            raise FormatNotFoundError(f'Cannot detect format from file {file_info!r}')

    else:
        serializer = anyser.core.find_serializer(format)
        if serializer is None:
            raise FormatNotFoundError(f'unknown format: {format}')

    return serializer

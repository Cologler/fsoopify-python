#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os

class PathComponent(str):
    def __init__(self, val):
        if not isinstance(val, str):
            raise TypeError
        self._normcased: str = None

    def __repr__(self):
        return '{}(\'{}\')'.format(type(self).__name__, self)

    def __eq__(self, other):
        if isinstance(other, PathComponent):
            return self.normalcase == other.normalcase
        if isinstance(other, str):
            return self.normalcase == os.path.normcase(other)
        return NotImplemented

    def __hash__(self):
        return hash(self.normalcase)

    @property
    def normalcase(self):
        '''
        get normcase path which create by `os.path.normcase()`.
        '''
        if self._normcased is None:
            self._normcased = os.path.normcase(self)
        return self._normcased


class Name(PathComponent):
    '''
    the name part of path.
    '''

    def __init__(self, val):
        super().__init__(val)
        self._pure_name = None
        self._ext = None

    def __ensure_pure_name(self):
        if self._pure_name is None:
            pn, ext = os.path.splitext(self)
            self._pure_name = PathComponent(pn)
            self._ext = PathComponent(ext)

    @property
    def pure_name(self) -> PathComponent:
        ''' get name without ext from path. '''
        self.__ensure_pure_name()
        return self._pure_name

    @property
    def ext(self) -> PathComponent:
        ''' get ext from path. '''
        self.__ensure_pure_name()
        return self._ext

    def replace_pure_name(self, val):
        if not isinstance(val, str):
            raise TypeError
        return Name(val + self.ext)

    def replace_ext(self, val):
        if not isinstance(val, str):
            raise TypeError
        return Name(self.pure_name + val)


class Path(PathComponent):
    def __init__(self, val):
        super().__init__(val)
        self._dirname = None
        self._name = None

    def __truediv__(self, right):
        if isinstance(right, str):
            return Path(os.path.join(self, right))
        return NotImplemented

    def __ensure_dirname(self):
        if self._dirname is None:
            dn, fn = os.path.split(self)
            self._dirname = Path(dn)
            self._name = Name(fn)

    @property
    def dirname(self):
        ''' get directory path from path. '''
        self.__ensure_dirname()
        return self._dirname

    @property
    def name(self) -> Name:
        ''' get name from path. '''
        self.__ensure_dirname()
        return self._name

    @property
    def pure_name(self) -> PathComponent:
        ''' get name without ext from path. '''
        return self.name.pure_name

    @property
    def ext(self) -> PathComponent:
        ''' get ext from path. '''
        return self.name.ext

    def is_ext_equals(self, val):
        ''' use `self.ext.equals()` instead。 '''
        return self.ext == val

    def replace_dirname(self, val):
        if not isinstance(val, str):
            raise TypeError
        return Path(os.path.join(val, self.name))

    def replace_name(self, val):
        if not isinstance(val, str):
            raise TypeError
        return Path(os.path.join(self.dirname, val))

    def replace_pure_name(self, val):
        return Path(os.path.join(self.dirname, self.name.replace_pure_name(val)))

    def replace_ext(self, val):
        return Path(os.path.join(self.dirname, self.name.replace_ext(val)))

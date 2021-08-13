# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from contextlib import ExitStack

from .visitor import AbsNodeVisitor

class ContentTree(dict):
    def __init__(self, iterable=None):
        super().__init__(iterable or ())
        self._es = ExitStack()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._es.__exit__(exc_type, exc_val, exc_tb)

    def set_context(self, key, value):
        self[key] = self._es.enter_context(value)

    def set_with_enter(self, key, value):
        self[key] = self._es.enter_context(value)

    def set_without_enter(self, key, value):
        self[key] = value


class BuildTreeVisitor(AbsNodeVisitor):
    as_stream: bool = False

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.tree = ContentTree()

    def get_visitor_for_childs(self):
        return type(self)(**self.__dict__)

    def visit_dir(self, d):
        visitor = self.get_visitor_for_childs()
        for item in d.list_items():
            visitor.visit(item)
        name = str(d.path.name)
        self.tree.set_with_enter(name, visitor.tree)
        return self.tree

    def visit_file(self, f):
        name = str(f.path.name)
        if self.as_stream:
            self.tree.set_with_enter(name, f.open_for_read_bytes())
        else:
            self.tree.set_without_enter(name, f.read(mode='rb'))
        return self.tree

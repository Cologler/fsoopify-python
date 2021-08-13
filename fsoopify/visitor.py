# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from .consts import NodeType

class AbsNodeVisitor:
    def visit(self, n):
        if n.node_type == NodeType.file:
            return self.visit_file(n)
        elif n.node_type == NodeType.dir:
            return self.visit_dir(n)
        else:
            return self.visit_default(n)

    def visit_default(self, n):
        raise NotImplementedError

    def visit_dir(self, d):
        return self.visit_default(d)

    def visit_file(self, f):
        return self.visit_default(f)

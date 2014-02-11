#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MTError(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(MTError):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

    def __repr__(self):
        return "\r\n".join(("[%s] %s" % (self.__class__.__name__, self.msg),
                            "\t%r" % self.expr,))

    __str__ = __repr__


class TemplateError(MTError):
    """Exception raised for errors in the template.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
        stage  -- template stage
    """

    def __init__(self, expr, msg, stage):
        self.expr = expr
        self.msg = msg
        self.stage = stage
        
    def __repr__(self):
        return "\r\n".join(("[%s] %s; stage: %s" % (self.__class__.__name__, self.msg, self.stage),
                            "\t%r" % self.expr))

    __str__ = __repr__

class ExpressionError(TemplateError):
    """Exception raise to indicate error in expression

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
        stage  -- template stage
    """

    def __init__(self, expr, msg, stage='compiling'):
        super(ExpressionError, self).__init__(expr, msg, stage)

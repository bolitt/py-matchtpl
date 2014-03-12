#!/usr/bin/env python
# -*- coding: utf-8 -*-

from error import ExpressionError
import re
from regexp import Regexp
#import ast
#from pprint import pprint

class Evaluater:
    KEYNAME = '_running_context_'
    
    def __init__(self, eval_value, key_ctx, g, l):
        self.eval_value = eval_value
        self.key_ctx = key_ctx
        self.globals = g
        self.locals = l
        self.build_expr_chain()

    def __call__(self, ):
        self.ret = None
        for i in xrange(0, len(self.funcs)):
            try:
                self.ret = self.funcs[i]()
                #print self.ret
                self.locals.update({self.key_ctx: self.ret,})
            except Exception, e:
                print e
                print self.segs[i]
        return self.ret

    def build_expr_chain(self):
        self.segs = parse_eval(self.eval_value)
        self.funcs = []
        if len(self.segs) == 0:
            raise ExpressionError(self.eval_value, '1+ expression(s) is needed')
        self.funcs.append(self.build_expr_first())
        for seg in self.segs[1:]:
            self.funcs.append(self.build_expr_others(seg))
        
    def build_expr_first(self):
        expr = "%s." % self.key_ctx + self.segs[0]
        code_ast = compile(expr, expr, 'eval')
        def func():
            # usage: eval(expression[, globals[, locals]])
            return eval(code_ast, self.globals, self.locals)
        return func

    def build_expr_others(self, seg):
        f = None
        if self.globals.has_key(seg):
            f = self.globals[seg]
        elif self.locals.has_key(seg):
            f = self.locals[seg]
        # if it is existed function:
        if f is not None:
            expr = seg + '(%s)' % self.key_ctx
            code_ast = compile(expr, expr, 'eval')        
            def func():
                return eval(code_ast, self.globals, self.locals)
            return func
        # doesn't exist the function, then try Regexp
        try:
            f = Regexp(seg)
            def func():
                return f(self.ret)
            return func
        except:
            pass

        # could not recognize seg
        raise ExpressionError(seg, 'could not recognize expression: not an existed function or valid regular expression')
        

# This pattern aims to ignore '|' inside the regular expression.
#   it matches "A |B", "A| B", or "A | B", but ignores "A|B". 
# Alternative solution is to use AST parser
PATTERN_DELIMITER = r"""
\s+\|       #  spaces + |
|           #or
\|\s+       #  | + spaces
"""
RE_DELIMITER = re.compile(PATTERN_DELIMITER, re.UNICODE | re.X)

def parse_eval(s, regex_delimiter=RE_DELIMITER):
    segs = [i.strip() for i in regex_delimiter.split(s)]
    for i in segs:
        if i == '':
            raise ExpressionError(s, 'invalid expression')
    return segs



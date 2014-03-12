#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from eval import parse_eval, Evaluater
from error import ExpressionError

class TestEval(unittest.TestCase):
    def test_parse(self):
        actual_iterable = parse_eval('''eval() | upper | lower | mtrequest | s/|/<sep>/ig | 
            dfa
        ''')
        self.assertSequenceEqual(actual_iterable, ['eval()', 'upper', 'lower', 'mtrequest', 's/|/<sep>/ig', 'dfa'] )

        self.assertRaises(ExpressionError, parse_eval, '''eval() | upper | lower | mtrequest | |  ''')


    def test_evaluator(self):
        expr = 'strip() | lower | title | s/\./?/ig '
        ev = Evaluater(expr, '_context_', {'lower': str.lower, 'title': str.title}, {'_context_': ' abf.zZz#bbB.zZz|dd ' } )
        self.assertEqual(ev(), 'Abf?Zzz#Bbb?Zzz|Dd')
        

if __name__ == "__main__":
    unittest.main()

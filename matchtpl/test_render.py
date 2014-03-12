#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from render import render

class TestRenderFunctions(unittest.TestCase):

    def test_render(self):
        s = render('hello, {{ name }}', dic={'name': 'jack'})
        self.assertEqual(s, 'hello, jack')

if __name__ == "__main__":
    unittest.main()

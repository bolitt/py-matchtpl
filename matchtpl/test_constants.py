#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from constants import VALID_ID as VALID_ID


class TestConstants(unittest.TestCase):

    def test_valid_id(self):
        # invalid
        self.assertTrue(VALID_ID.match("") is None)
        self.assertTrue(VALID_ID.match(" _ ") is None)
        self.assertTrue(VALID_ID.match(" _") is None)
        self.assertTrue(VALID_ID.match("$a") is None)
        self.assertTrue(VALID_ID.match("a b") is None)

        # valid
        self.assertTrue(VALID_ID.match("_") is not None)
        self.assertTrue(VALID_ID.match("a") is not None)
        self.assertTrue(VALID_ID.match("anApple") is not None)
        self.assertTrue(VALID_ID.match("_anApple__") is not None)
        self.assertTrue(VALID_ID.match("_an_apple") is not None)

if __name__ == "__main__":
    unittest.main()

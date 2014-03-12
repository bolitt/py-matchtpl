#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from error import ExpressionError

from regexp import IS_MATCH_MODE, IS_SUB_MODE, IS_INSENSITIVE, IS_GLOBAL, GET_DELIMITER
from regexp import regexp_parse, Regexp
import re

class TestRegexp(unittest.TestCase):
    def test_basic(self):
        self.assertIsNotNone(IS_MATCH_MODE.search(u'm/dfaf/i'))
        self.assertIsNotNone(IS_MATCH_MODE.search(u'/dfaf/'))
        self.assertIsNotNone(IS_MATCH_MODE.search(u'm#dfaf#'))
        self.assertIsNotNone(IS_SUB_MODE.search(u's/dfaf/dfaf'))

        self.assertIsNotNone(IS_INSENSITIVE.search(u'ig'))
        self.assertIsNone(IS_INSENSITIVE.search(u''))

        self.assertIsNotNone(IS_GLOBAL.search(u'ig'))
        self.assertIsNone(IS_GLOBAL.search(u''))

        self.assertEqual(GET_DELIMITER.findall(u's/dfa')[0], '/')
        self.assertEqual(GET_DELIMITER.findall(u'm/dfa')[0], '/')
        self.assertEqual(GET_DELIMITER.findall(u'##')[0], '#')

    def test_split(self):
        self.assertEqual(len( u's/1/2/'.split('/')), 4)
        self.assertEqual(len( u'#1#2#'.split('#')), 4)

    def test_valid(self):
        # return (r1, r2, kind, opts, origin)
        actual = regexp_parse('m/dfaf/ig')
        expected = ('dfaf', '', 'search', re.UNICODE | re.IGNORECASE, 'm/dfaf/ig')
        self.assertSequenceEqual(actual, expected)

        actual = regexp_parse('m#dfaf#')
        expected = ('dfaf', '', 'search', re.UNICODE, 'm#dfaf#')
        self.assertSequenceEqual(actual, expected)

        actual = regexp_parse('s#^[fda]$#dd#i')
        expected = ('^[fda]$', 'dd', 'sub_1', re.UNICODE | re.IGNORECASE, 's#^[fda]$#dd#i')
        self.assertSequenceEqual(actual, expected)

        actual = regexp_parse('s#^[fda]$#dd#ig')
        expected = ('^[fda]$', 'dd', 'sub_all', re.UNICODE | re.IGNORECASE, 's#^[fda]$#dd#ig')
        self.assertSequenceEqual(actual, expected)

    def test_invalid(self):
        # more than 4 segments
        with self.assertRaises(ExpressionError):
            regexp_parse('m/dfaf///ig')
        with self.assertRaises(ExpressionError):
            regexp_parse('s/dfaf///ig')
        with self.assertRaises(ExpressionError):
            regexp_parse('s#dfaf####ig')

        # only 2 segments
        with self.assertRaises(ExpressionError):
            regexp_parse('m/')
        # only 1 segment
        with self.assertRaises(ExpressionError):
            regexp_parse('s')
        # 0 segment
        with self.assertRaises(ExpressionError):
            regexp_parse('')
        
        # cannot recognize
        with self.assertRaises(ExpressionError):
            regexp_parse('#dfaf##ig')

    def test_regexp_kind(self):
        self.assertEqual(Regexp(r'm/F/i').kind, 'search')
        self.assertEqual(Regexp(r'/F/i').kind, 'search')
        self.assertEqual(Regexp(r'm#F#!\1!#i').kind, 'search_extract')
        self.assertEqual(Regexp(r's/F/1/i').kind, 'sub_1')
        self.assertEqual(Regexp(r's/F/1/gi').kind, 'sub_all')

    def test_regex_search(self):
        """ print 'search', 'F/i' """
        self.assertEqual(Regexp(r'm/F/i')('dddfaf fdadf'), True)
        """ print 'search', 'F/' """
        self.assertEqual(Regexp(r'm/F/')('dddfaf fdadf'), False)
        """ print 'search', 'f/' """
        self.assertEqual(Regexp(r'm/f/')('dddfaf fdadf'), True)

    def test_regex_search_extract(self):
        """ print 'search_extract', '' """
        s = Regexp(r'm/(\w+) (\w+)/\2_\1/')('hello world ! ok done !')
        self.assertEqual(s, 'world_hello')

    def test_regex_sub1(self):
        """ print 'sub_1', 'D/Z/i' """
        self.assertEqual(Regexp(r's/D/Z/i')('dddfaf fdadf'), 'Zddfaf fdadf')
        """ print 'sub_1', 'D=/Z/i' """
        self.assertEqual(Regexp(r's/D+/Z/i')('dddfaf fdadf'), 'Zfaf fdadf')

    def test_regex_sub_all(self):
        """ print 'sub_all', 'D/Z/ig' """
        self.assertEqual(Regexp(r's/D/Z/ig')('dddfaf fdadf'), 'ZZZfaf fZaZf')
        """ print 'sub_all', 'D/Z/g' """
        self.assertEqual(Regexp(r's/D/Z/g')('dddfaf fdadf'), 'dddfaf fdadf')
        """ print 'sub_all', 'D+/Z/ig' """
        self.assertEqual(Regexp(r's/D+/Z/ig')('dddfaf fdadf'), 'Zfaf fZaZf')
        

if __name__ == "__main__":
    unittest.main()

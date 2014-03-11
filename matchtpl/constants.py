#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

''' lib directory '''
LIB_DIR = os.path.dirname(__file__)

''' template directory name & path '''
TEMPLATE_DIRNAME = 'template'
TEMPLATE_PATH = os.path.join(LIB_DIR, TEMPLATE_DIRNAME)

''' monitor directory name & path '''
MONITOR_DIRNAME = 'web'
MONITOR_PATH = os.path.join(LIB_DIR, MONITOR_DIRNAME)

''' serialization options: (default) '''
JSON_CONF = {'encoding': 'utf-8',
             'ensure_ascii': False,
             'indent': 4,
             'sort_keys': True,
             }

YAML_CONF = {'encoding': 'utf-8',
             'allow_unicode': True,
             'default_flow_style': False,
             'line_break': True,
             'indent': 4, }

''' valid element id '''
VALID_ID = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]*$')




def test():
    # invalid
    print VALID_ID.match("") is None
    print VALID_ID.match(" _ ") is None
    print VALID_ID.match(" _") is None
    print VALID_ID.match("$a") is None
    print VALID_ID.match("a b") is None

    # valid
    print VALID_ID.match("_") is not None
    print VALID_ID.match("a") is not None
    print VALID_ID.match("anApple") is not None
    print VALID_ID.match("_anApple__") is not None
    print VALID_ID.match("_an_apple") is not None

if __name__ == "__main__":
    test()

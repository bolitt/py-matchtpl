#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

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


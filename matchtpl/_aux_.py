#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

def _load_file_(path):
    content = None
    with codecs.open(path, 'r') as f:
        content = f.read()
    return content

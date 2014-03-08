#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

def _load_file_(path):
    f = codecs.open(path, 'r')
    content = f.read()
    f.close()
    return content

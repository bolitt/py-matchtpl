#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

'''constants:
    FIXPATH_FILE: this file
    MATCHTPL_DIR: the real dir of this file
'''
from constants import LIB_DIR


'''add path to the environment
'''
def fixpath(path=LIB_DIR):
    if path not in sys.path:
        sys.path.append(path)

#sys.path.append(os.path.join(os.getcwd()))
#print 'path, cwd', os.getcwd()
#print 'path, __file__', __file__
#print 'path, cwd', os.getcwd()
#print 'path, __file__', __file__


def usemodule(name):
    module = __import__(name, {}, {})
    # print 'To load: ', name
    return module

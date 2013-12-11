#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re
import os
import codecs
from pprint import pprint

sys.path.append(os.path.join(os.getcwd(), '..'))

from core import *

def test_amazon_template():
    env = MTemplateEnv(template = 'amazon_template.xml')
    t = MTemplate()
    t.build(env)
    #print t.root
    
    parser = MTemplateParser(t)
    results = parser.parse("amazon.html")
    
    #print "[Results]"
    print results
    #print "[/Results]"

if __name__ == "__main__":
    test_amazon_template()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re
import os
import codecs
from pprint import pprint

sys.path.append(os.path.join(os.getcwd(), '..'))

from core import *

def test_login_action(results, attrs):
    print "Login Action:"
    print "results:", results
    print "attrs", attrs
    return "Login with: " + str(results)
    
def test_action_template():
    env = MTemplateEnv(template = 'action_template.xml')
    t = MTemplate()
    t.build(env)
    print t.root

    parser = MTemplateParser(t)
    results = parser.parse("action_template.html", login=test_login_action)

    print "[Results]"
    print results
    print "[/Results]"

if __name__ == "__main__":
    test_action_template()

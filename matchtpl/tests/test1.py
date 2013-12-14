#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re
import os
import codecs
from pprint import pprint


sys.path.append(os.path.join(os.getcwd(), '..'))

from core import *

def test_default_template():
    env = MTemplateEnv(template = 'default_template.xml')
    t = MTemplate()
    t.build(env)

def test_mytemplate():
    env = MTemplateEnv(template = 'template1.xml')
    t = MTemplate()
    t.build(env)
    print t.root

    parser = MTemplateParser(t)
    results = parser.parse("template1.html")

    print "[Results]"
    print results
    print "[/Results]"


def test_login_action(results, attrs):
    print "Login Action:"
    print "results:", results
    print "attrs", attrs
    return "Login with: " + str(results)
    
def test_action_template():
    env = MTemplateEnv(template = 'action.xml')
    t = MTemplate()
    t.build(env)
    print t.root

    parser = MTemplateParser(t)
    results = parser.parse("action.html", login=test_login_action)

    print "[Results]"
    print results
    print "[/Results]"

def test_amazon_template():
    env = MTemplateEnv(template = 'amazon.xml')
    t = MTemplate()
    t.build(env)
    print t.root
    
    parser = MTemplateParser(t)
    results = parser.parse("amazon.html")
    
    print "[Results]"
    print results
    print "[/Results]"

if __name__ == "__main__":
    test_mytemplate()
    test_action_template()
    test_amazon_template()

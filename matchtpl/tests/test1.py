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
    env = MTemplateEnv(template = 'action_template.xml')
    t = MTemplate()
    t.build(env)
    print t.root

    parser = MTemplateParser(t)
    results = parser.parse("action_template.html", login=test_login_action)

    print "[Results]"
    print results
    print "[/Results]"

def test_5i5j_template():
    env = MTemplateEnv(template = '5i5j_exchange.xml')
    t = MTemplate()
    t.build(env)
    print t.root
    
    parser = MTemplateParser(t)
    results = parser.parse("5i5j_exchange.html")
    
    print "[Results]"
    pprint(results)
    print "[/Results]"
    with codecs.open("5i5jexchange.txt", 'w', "utf-8") as f:
        for house in results[0]:
            f.write(u"%s\r\n" % house['title'])
            for k,v in house.iteritems():
                v = v.strip() # strip begin and end
                v = re.sub('\\s{2,}', '', v.strip()) # replace empty space >= 2
                f.write(u"%s\t%s\r\n" % (k, v))
            f.write("\r\n")
        f.close()

if __name__ == "__main__":
    test_mytemplate()
    test_action_template()
    test_5i5j_template()

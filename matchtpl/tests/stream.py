#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re
import os
import codecs
from pprint import pprint
import argparse

reload(sys)
sys.setdefaultencoding('utf-8')

from matchtpl import MTemplateEnv, MTemplate, MTemplateParser

def build_parser(template):
    env = MTemplateEnv(template = template)
    t = MTemplate()
    t.build(env)
    parser = MTemplateParser(t)
    return parser
 
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Help of stream (py-matchtpl)')
    argparser.add_argument('-t', '--template', metavar='file', type=str, nargs=1,
                   help='file of template to build parser')
    argparser.add_argument('-i', '--input', metavar='input', type=str, nargs=1,
                   help='html/xml to build parse')
    args = argparser.parse_args()
    if args.template is None:
        argparser.print_help()
        exit()
    try:
        parser = build_parser(args.template[0])
    except Exception, e:
        print "Error in building parser:"
        print e
        exit()
    
    if args.input is None:
        content = sys.stdin.readlines()
        content = "".join(content)
        r = parser.parse_content(content)
        sys.stdout.write(u"%s" % r)
    else:
        r = parser.parse(args.input[0])
        sys.stdout.write(u"%s" % r)

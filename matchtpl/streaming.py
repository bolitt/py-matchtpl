#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re
import os
import codecs
from pprint import pprint
import argparse
import traceback

# use this for testers
from core import MTemplateEnv, MTemplate, MTemplateParser

# use this in your code
#from matchtpl import MTemplateEnv, MTemplate, MTemplateParser

def build_parser(template):
    env = MTemplateEnv(template=template)
    t = MTemplate()
    t.build(env)
    parser = MTemplateParser(t)
    return parser

argparser = argparse.ArgumentParser(description='Help of stream (py-matchtpl)')
argparser.add_argument('-t', '--template', metavar='file', type=str, nargs=1,
               help='file of template to build parser')
argparser.add_argument('-i', '--input', metavar='input', type=str, nargs=1,
               help='html/xml to build parse')
args = argparser.parse_args()

def streaming(args=args, stdin=sys.stdin, stdout=sys.stdout):    
    if args.template is None:
        argparser.print_help()
        exit()
    try:
        parser = build_parser(args.template[0])
    except Exception, e:
        print "Error in building parser:"
        print repr(e)
        traceback.print_exc()
        exit()

    if args.input is None:
        content = stdin.readlines()
        content = "".join(content)
        r = parser.parse_content(content)
        stdout.write("%s" % r)
    else:
        r = parser.parse(args.input[0])
        stdout.write("%s" % r)

if __name__ == "__main__":
    streaming(args)

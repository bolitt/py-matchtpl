#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

from pyquery import PyQuery as py
from lxml import etree
import urllib
from eval import Evaluater
from _aux_ import _load_file_

utf8_parser = etree.HTMLParser(encoding='utf-8')

class MTemplateEnv:
    """ default environment of template """
    def __init__(self, template=None, stream=None):
        self.parser = etree.XMLParser(encoding='utf-8', remove_comments=True)
        if template is not None:
            self.template = self.build_env_file(template)
        elif stream is not None:
            self.template = self.build_env_content(stream)
        else:
            raise Exception('[Error] Both file and stream are None')

    def build_env_file(self, file):
        content = _load_file_(file)
        template = etree.fromstring(content, parser=self.parser)
        return template

    def build_env_content(self, content):
        template = etree.fromstring(content, parser=self.parser)
        return template


class MTBuild(object):
    ATTRS = {"select": None, #selection
             "get": None,    #get value
             "eval": None,   #eval value
             "key": None,    #key: for dict
             "default": None, #default: default value
             "as": None,     #as: type converter
             "encoding": None, #encoding
             "type": None, # script's type
            }
    TAGS = {}
    #TAGS_KEYWORDS = {"map": self.build_map,
    #                 "array": self.build_array,
    #                 "s": self.build_string,
    #                 "script": self.build_script,
    #                }

    def __init__(self, keyword=None, kind=None):
        #print "inside MTBuild.__init__()", keyword
        self.keyword = keyword
        self.kind = kind
        if kind is None:
            raise Exception('[error]need to specify kind: %s' % kind)
        if kind == 'tag' and self.TAGS.has_key(keyword):
            raise Exception('[error]keyword existed: %s' % keyword)
        if kind == 'attr' and self.ATTRS.has_key(keyword):
            raise Exception('[error]attribute existed: %s' % keyword)

    def __call__(self, original_func):
        decorator_self = self
        if self.kind == 'tag':
            self.TAGS[self.keyword] = original_func
            return original_func
        if self.kind == 'attr':
            self.ATTRS[self.keyword] = original_func

    @staticmethod
    def tags():
        return MTBuild.TAGS

    @staticmethod
    def attrs():
        return MTBuild.ATTRS


def mtdebug(s):
    from pprint import pprint
    sys.stderr.write("[MTDEBUG] ")
    pprint(s, stream=sys.stderr)
    return s


class MTContext:
    GLOBAL = { 'escape': urllib.quote,
               'unescape': urllib.unquote,
               'lower': str.lower,
               'trim': str.strip,
               'upper': str.upper,
               'capitalize': str.capitalize,
               'title': str.title,
               'mtrequest': py,
               'mtdebug': mtdebug,
               }
    LOCAL = { Evaluater.CONTEXT: None, }

    def __init__(self):
        pass

    @staticmethod
    def globals(**kw):
        if kw is not None:
            MTContext.GLOBAL.update(kw)
        return MTContext.GLOBAL

    @staticmethod
    def locals(**kw):
        if kw is not None:
            MTContext.LOCAL.update(kw)
        return MTContext.LOCAL


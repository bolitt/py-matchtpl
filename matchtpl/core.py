#!/usr/bin/env python
# -*- coding: utf-8 -*-


from basic import *
from pyquery import PyQuery as py

from log import LOGGER as logger
from callsite import *
from _aux_ import _load_file_
import os
import warnings
from error import TemplateError
from constants import VALID_ID as VALID_ID


class MTNode(dict):
    def __init__(self, meta, attrs, orig_ele, kind, children=None, callsite=None):
        self['exp_meta'] = meta            #'root'
        self['exp_attrs'] = attrs
        self['exp_node'] = orig_ele        # ele
        self['exp_children'] = children    # self.triggers
        self['exp_kind'] = kind            # 'root'
        self['exp_callsite'] = callsite    # RootCallSite(x)



class MTemplate:
    """ build abstract syntex tree (AST) based on template """
    def __init__(self):
        self.triggers = []
        self.ids = {}
        self.root_CallSite = None

    def build(self, env):
        doc = py(env.template)
        #print "[Template]"
        #print doc
        #print "[/Template]"
        self.fromdoc(doc)
        #pprint(self.triggers)

    def fromdoc(self, doc):
        attrs = self.extract_attrs(doc)
        root_node = self.build_root(doc, attrs)
        self.root = root_node['exp_callsite']

    def build_node_index(self, attrs, x):
        if attrs.has_key('id'):
            id = attrs['id'] ## TODO
            # logger.debug('[id] %s' % id)
            if VALID_ID.match(id) is None or self.ids.has_key(id) :
                raise TemplateError('id:%s is duplicated!' % attrs['id'])
            else:
                self.ids[id] = x

    def extract_attrs(self, ele):
        """ Extract attrs """
        attrs = {}
        #manipulation keywords
        TARGET_KEYWORDS = MTBuild.attrs()
        for a in TARGET_KEYWORDS.iterkeys():
            if py(ele).attr(a):
                attrs[a] = py(ele).attr(a)

        #get tag name
        attrs['_TAG_'] = py(ele)[0].tag
        #future: deal with internal property like <a><a.href></a.href></a>
        return attrs

    def build_element(self, ele):
        attrs = self.extract_attrs(ele)
        TARGET_KEYWORDS = MTBuild.tags()
        # deal with different data type
        tagname = ele.tag
        # print '[Test]tagname', tagname
        if TARGET_KEYWORDS.has_key(tagname):
            callback = TARGET_KEYWORDS.get(tagname)
            yield callback(self, ele, attrs)
        else:
            warnings.warn('Ignore tag: %s. Cannot be recognized.' % tagname)
            children = []
            for cl in py(ele).children():
                for i in self.build_element(cl):
                    children.append(i)
            for i in children:
                yield i

    @MTBuild(keyword='root', kind='tag')
    def build_root(self, ele, attrs):
        ch = []
        for child in py(ele).children():
            for node in self.build_element(child):
                ch.append(node)
        # from pprint import pprint
        # pprint(ch)
        for node in ch:
            if node['exp_kind'] == 'data':
                self.triggers.append(node)
            elif node['exp_kind'] == 'code':
                # call the function immediately
                node['exp_callsite'](element=None)
        # print "string:", ele, attrs
        x = MTNode(meta='root', attrs=attrs, orig_ele=ele, kind='root')
        x['exp_children'] = self.triggers
        x['exp_callsite'] = RootCallSite(x)

        self.build_node_index(attrs, x)
        return x

    @MTBuild(keyword='array', kind='tag')
    def build_array(self, ele, attrs):
        #print "array:", ele, attrs
        ch = []
        for child in py(ele).children():
            for node in self.build_element(child):
                ch.append(node)
        x = MTNode(meta='array', attrs=attrs, orig_ele=ele, kind='data')
        x['exp_children'] = ch
        x['exp_callsite'] = ArrayCallSite(x)

        self.build_node_index(attrs, x)
        return x

    @MTBuild(keyword='map', kind='tag')
    def build_map(self, ele, attrs):
        # print "map:", ele, attrs
        ch = []
        for child in py(ele).children():
            for node in self.build_element(child):
                ch.append(node)
        x = MTNode(meta='map', attrs=attrs, orig_ele=ele, kind='data')
        x['exp_children'] = ch
        x['exp_callsite'] = MapCallSite(x)

        self.build_node_index(attrs, x)
        return x

    @MTBuild(keyword='s', kind='tag')
    def build_string(self, ele, attrs):
        # print "string:", ele, attrs
        x = MTNode(meta='string', attrs=attrs, orig_ele=ele, kind='data')
        x['exp_children'] = []
        x['exp_callsite'] = StringCallSite(x)

        self.build_node_index(attrs, x)
        return x

    @MTBuild(keyword='script', kind='tag')
    def build_script(self, ele, attrs):
        # print "script:", ele, attrs
        ch = py(ele).html()
        x = MTNode(meta='script', attrs=attrs, orig_ele=ele, kind='code')
        x['exp_children'] = ch
        x['exp_callsite'] = ScriptCallSite(x)

        self.build_node_index(attrs, x)
        return x

    @MTBuild(keyword='render', kind='tag')
    def build_render(self, ele, attrs):
        # print "script:", ele, attrs
        ch = py(ele).html()
        ch = ch.strip(os.linesep)  # trim: the front end ended line separators
        x = MTNode(meta='render', attrs=attrs, orig_ele=ele, kind='render')
        x['exp_children'] = ch
        x['exp_callsite'] = RenderCallSite(x)

        self.build_node_index(attrs, x)
        return x

#######################################################
class MTemplateParser:
    def __init__(self, template):
        self.template = template
        
    def parse(self, filename, **options):
        content = _load_file_(filename)
        env = {'template': self.template,
               'mtcontext': MTContext, }
        result = self.template.root(env, content, **options)
        return result

    def parse_content(self, content, **options):
        env = {'template': self.template,
               'mtcontext': MTContext, }
        result = self.template.root(env, content, **options)
        return result
    


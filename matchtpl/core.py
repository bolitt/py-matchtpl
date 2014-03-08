#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pyquery import PyQuery as py

from basic import *
from callsite import *
from _aux_ import _load_file_




class MTemplate:
    """ build abstract syntex tree (AST) based on template """
    def __init__(self):
        self.triggers = []
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
        self.build_root(doc, attrs)

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
        for (tagname, callback) in TARGET_KEYWORDS.iteritems():
            if tagname == ele.tag:
                return callback(self, ele, attrs)

    #@MTBuild(keyword='root', kind='tag')
    def build_root(self, ele, attrs):
        for child in ele.children():
            node = self.build_element(child)
            if node['exp_kind'] == 'data':
                self.triggers.append(node)
            elif node['exp_kind'] == 'code':
                # call the function immediately
                node['exp_callsite'](element=None)
        # print "string:", ele, attrs
        x = {}
        x['exp_meta'] = 'root'
        x['exp_attrs'] = attrs
        x['exp_node'] = ele
        x['exp_children'] = self.triggers
        x['exp_kind'] = 'root'
        self.root = x['exp_callsite'] = RootCallSite(x)
        return x

    @MTBuild(keyword='array', kind='tag')
    def build_array(self, ele, attrs):
        #print "array:", ele, attrs
        ch = []
        for child in py(ele).children():
            ch.append(self.build_element(child))
        x = dict()
        x['exp_meta'] = 'array'
        x['exp_attrs'] = attrs
        x['exp_node'] = ele
        x['exp_children'] = ch
        x['exp_kind'] = 'data'
        x['exp_callsite'] = ArrayCallSite(x)
        return x

    @MTBuild(keyword='map', kind='tag')
    def build_map(self, ele, attrs):
        # print "map:", ele, attrs
        ch = []
        for child in py(ele).children():
            #print child
            ch.append(self.build_element(child))
        x = dict()
        x['exp_meta'] = 'map'
        x['exp_attrs'] = attrs
        x['exp_node'] = ele
        x['exp_children'] = ch
        x['exp_kind'] = 'data'
        x['exp_callsite'] = MapCallSite(x)
        return x

    @MTBuild(keyword='s', kind='tag')
    def build_string(self, ele, attrs):
        # print "string:", ele, attrs
        x = dict()
        x['exp_meta'] = 'string'
        x['exp_attrs'] = attrs
        x['exp_node'] = ele
        x['exp_children'] = []
        x['exp_kind'] = 'data'
        x['exp_callsite'] = StringCallSite(x)
        return x

    @MTBuild(keyword='script', kind='tag')
    def build_script(self, ele, attrs):
        # print "script:", ele, attrs
        ch = py(ele).html()
        x = dict()
        x['exp_meta'] = 'script'
        x['exp_attrs'] = attrs
        x['exp_node'] = ele
        x['exp_children'] = ch
        x['exp_kind'] = 'code'
        x['exp_callsite'] = ScriptCallSite(x)
        return x

#######################################################
class MTemplateParser:
    def __init__(self, template):
        self.template = template
        
    def parse(self, filename, **environment):
        content = _load_file_(filename)
        result = self.template.root(content, **environment)
        return result

    def parse_content(self, content, **environment):
        result = self.template.root(content, **environment)
        return result
    

if __name__ == "__main__":
    pass

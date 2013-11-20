#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, os.path, codecs, re
import json, yaml
from pyquery import PyQuery as py 
from lxml import etree
from pprint import pprint


__all__ = [
    "MTemplateEnv",
    "MTemplate",
    "MTemplateParser",
    "MTCallSite",
    "ArrayCallSite",
    "MapCallSite",
    "StringCallSite",
    "RootCallSite",
]

utf8_parser = etree.HTMLParser(encoding='utf-8')

def _load_file_(path):
    f = codecs.open(path, 'r')
    content = f.read()
    f.close()
    return content

class MTemplateEnv:
    """ default environment of template """
    def __init__(self, template):
        self.parser = etree.XMLParser(encoding='utf-8', remove_comments=True)
        self.template = template
        
    def get_template(self):
        content = _load_file_(self.template)
        content = etree.fromstring(content, parser = self.parser)
        return content
    
class MTemplate:
    """ build abstract syntex tree (AST) based on template """
    def __init__(self):
        self.triggers = []
        self.root_CallSite = None
        
    def build(self, env):
        doc = py(env.get_template())
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
        TARGET_KEYWORDS = ["select", #selection
                        "get",    #get value
                        "eval",   #eval value
                        "key",    #key: for dict
                        "default", #default: default value
                        "as",     #as: type converter
                        ]
        for a in TARGET_KEYWORDS:
            if py(ele).attr(a):
                attrs[a] = py(ele).attr(a)

        #get tag name
        attrs['_TAG_'] = py(ele)[0].tag
        #future: deal with internal property like <a><a.href></a.href></a>
        return attrs

    def build_element(self, ele):
        attrs = self.extract_attrs(ele)
        TARGET_KEYWORDS = {"map": self.build_map,
                          "array": self.build_array,
                          "s": self.build_string,
                          }
        
        # deal with different data type
        for (tagname, callback) in TARGET_KEYWORDS.iteritems():
            if tagname == ele.tag:
                return callback(ele, attrs)

    def build_root(self, ele, attrs):
        for child in ele.children():
            trigger = self.build_element(child)
            self.triggers.append(trigger)
        # print "string:", ele, attrs
        x = dict()
        x['exp_meta'] = 'root'
        x['exp_attrs'] = attrs
        x['exp_node'] = ele
        x['exp_children'] = self.triggers
        self.root = x['exp_callsite'] = RootCallSite(x)
        
       
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
        x['exp_callsite'] = ArrayCallSite(x)
        return x
        
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
        x['exp_callsite'] = MapCallSite(x)
        return x
        
    def build_string(self, ele, attrs):
        # print "string:", ele, attrs
        x = dict()
        x['exp_meta'] = 'string'
        x['exp_attrs'] = attrs
        x['exp_node'] = ele
        x['exp_children'] = []
        x['exp_callsite'] = StringCallSite(x)
        return x

#######################################################
# CallSites: abstract syntex tree(AST) callsite
class MTCallSite:
    def __init__(self, exp):
        self.exp = exp
        self.meta = "CallSite_" + exp['exp_meta']
        self.attrs = exp['exp_attrs']
        self.children = exp['exp_children']
        self.callsite = self
        
    def do(self, context):
        pass

    def has_attr(self, attrName):
        return self.attrs.has_key(attrName)
    
    def select(self, context):
        """ select sub-context and yield generateor """
        if self.attrs.has_key('select'):
            #return py(context).find(self.attrs['select'])
            selector = self.attrs['select']
        else: # no selector is found
            return py(context)
        
        # if find selector
        try:
            return py(context).find(selector)
        except Exception, e:
            # print e
            return py( [ ] ) # return empty pyquery object
    
    def get(self, get_value, context):
        """ get text() or html() """
        if get_value == "text":
            return py(context).text()
        elif get_value == "html":
            return py(context).html()

    def default(self, default_value):
        return default_value

    def eval(self, eval_value, context):
        """ """
        # usage: eval(expression[, globals[, locals]])
        ret = eval("py(context)." + eval_value, {}, {'py': py, 'context': context})
        return ret

    def __str__(self):
        return self.meta

class ArrayCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)
    
    def do(self, element):
        ch = []
        # print "array:", py(element)
        context = self.select(element)
        # print "array:", py(context)
        if self.has_attr("get"):
            get_val = self.attrs["get"]
            context = self.get(get_val, context)
        elif self.has_attr("eval"):
            eval_val = self.attrs["eval"]
            context = self.eval(eval_val, context)
        if len(context) > 0:
            for child_context in context:
                #print "array:", py(child_context)
                for child in self.children:
                    callsite = child['exp_callsite']
                    ch.append(callsite.do(child_context))
        return ch

class MapCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)

    def do(self, element):
        ch = {}
        #print "map:", py(element)
        context = self.select(element)
        if self.has_attr("get"):
            get_val = self.attrs["get"]
            context = self.get(get_val, context)
        elif self.has_attr("eval"):
            eval_val = self.attrs["eval"]
            context = self.eval(eval_val, context)
        if len(context) > 0:
            child_context = context
            #print "map child:", py(child_context)
            for child in self.children:
                callsite = child['exp_callsite']
                if callsite.has_attr('key'):
                    key = callsite.attrs['key']
                    ch[key] = callsite.do(child_context)
        return ch

class StringCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)
    
    def do(self, element):
        child_context = self.select(element)
        ret_val = None
        #print 'string:', py(child_context)
        # deal with:
        # (1) get
        # (2) eval
        # (3) default
        if len(child_context) > 0:
            if self.has_attr("get"):
                get_val = self.attrs["get"]
                ret_val = self.get(get_val, child_context)
            elif self.has_attr("eval"):
                eval_val = self.attrs["eval"]
                ret_val = self.eval(eval_val, child_context)

        if (ret_val is None) and self.has_attr("default"):
            default_val = self.attrs["default"]
            ret_val = self.default(default_val)
        return ret_val

class RootCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)

    def do(self, doc, **environment):
        root_element = py(doc)
        results = []
        for tri in self.children:
            r = tri['exp_callsite'].do(root_element)
            results.append(r)

        # action:
        tag = self.attrs['_TAG_']
        if tag != "root":
            ret = self.call_action(results, action=tag, attrs=self.attrs, **environment)
            return ret
        else:
            # actor as:
            if self.has_attr('as'):
                as_val = self.attrs['as']
                ret = self.call_as(as_val, results)
                return ret
            else:
                return results

    def call_as(self, as_val, results):
        if as_val == "str":
            return str(results)
        elif as_val == "json":
            return json.dumps(results,
                        encoding='utf-8', ensure_ascii=False, indent=4, sort_keys=True, )
        elif as_val == "yaml":
            return yaml.dump(results, 
                        encoding='utf-8', allow_unicode=True, default_flow_style=False,
                        line_break=True, indent=4, )
        raise Exception("[Error] root attributes: %s not recognized" % as_val)

    #def make_instance(self, classname, *args, **kwargs):
    #    try:
    #        return globals()[classname](*args, **kwargs)
    #        # return vars()[classname](*args, **kwargs) # locally
    #    except:
    #        raise NameError("Class %s is not defined" % classname)
        
    def call_action(self, results, action, attrs, **environment):
        func = None
        try:
            func = environment[action]
        except:
            try: func = globals[action]
            except:
                raise NameError("Class/function %s is not defined" % action)
        # now func is not None
        return func(results=results, attrs=attrs)


#######################################################
class MTemplateParser:
    def __init__(self, template):
        self.template = template
        
    def parse(self, filename, **environment):
        content = _load_file_(filename)
        results = self.template.root.do(content, **environment)
        return results


if __name__ == "__main__":
    pass

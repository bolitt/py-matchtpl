#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, os.path, codecs
from pyquery import PyQuery as py 
from lxml import etree
import urllib
from eval import parse_eval, Evaluater
from regexp import Regexp


try:
    import json
except ImportError:
    import warnings
    warnings.warn("Package json not found, so some functions may cause exception. Please install json! ")
    
try:
    import yaml
except ImportError:
    import warnings
    warnings.warn("Package yaml not found, so some functions may cause exception. Please install PyYAML! ")


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
    def __init__(self, template=None, stream=None):
        self.parser = etree.XMLParser(encoding='utf-8', remove_comments=True)
        if file is not None:
            self.template = self.build_env_file(template)
        elif content is not None:
            self.template = self.build_env_content(stream)
        else:
            raise Exception('[Error] Both file and stream are None')
        
    def build_env_file(self, file):
        content = _load_file_(file)
        template = etree.fromstring(content, parser = self.parser)
        return template
    
    def build_env_content(self, content):
        template = etree.fromstring(content, parser = self.parser)
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
# CallSites: abstract syntex tree(AST) callsite
class MTCallSite:
    def __init__(self, exp):
        self.exp = exp
        self.meta = "CallSite_" + exp['exp_meta']
        self.attrs = exp['exp_attrs']
        self.children = exp['exp_children']
        self.callsite = self
        self.evaluator_cache = {}
        
    def __call__(self, context):
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
        key_ctx = Evaluater.CONTEXT
        g = MTContext.globals()
        l = MTContext.locals(**{key_ctx: py(context),})
        # cache the evaluator
        cache = self.evaluator_cache
        if not cache.has_key(eval_value):
            evaluator = Evaluater(eval_value, key_ctx, g, l)
            cache[eval_value] = evaluator
        evaluator = cache[eval_value]
        ret = evaluator()
        return ret

    def __str__(self):
        return self.meta

class ArrayCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)
    
    def __call__(self, element):
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
                    ch.append(callsite(child_context))
        return ch

class MapCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)

    def __call__(self, element):
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
                    ch[key] = callsite(child_context)
        return ch

class StringCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)
    
    def __call__(self, element):
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

class ScriptCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)
    
    def __call__(self, element):
        ret_val = None
        #print 'script:', py(child_context)
        # deal with:
        code = self.children
        #print '===='
        #print code
        #print '===='
        code_AST = compile(code, code, "exec")
        exec(code_AST, MTContext.globals(), MTContext.locals())
        #print MTContext.globals()
        #print MTContext.locals()
        return ret_val

class RootCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)

    def __call__(self, doc, **environment):
        tag = self.attrs['_TAG_']
        # convert encoding
        if tag == "root" and self.has_attr('encoding'):
            encoding = self.attrs['encoding']
            doc = doc.decode(encoding)

        root_element = py(doc)
        
        results = []
        for tri in self.children:
            r = tri['exp_callsite'](root_element)
            results.append(r)

        # action:
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
        result = self.template.root(content, **environment)
        return result

    def parse_content(self, content, **environment):
        result = self.template.root(content, **environment)
        return result
    

if __name__ == "__main__":
    pass

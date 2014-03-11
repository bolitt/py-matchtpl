#!/usr/bin/env python
# -*- coding: utf-8 -*-

from basic import *
from pyquery import PyQuery as py
from eval import Evaluater
from render import render

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

#try:
#    import unicodecsv as csv
#    from cStringIO import StringIO
#except ImportError:
#    import warnings
#    warnings.warn("Package unicodecsv not found, so some functions may cause exception. Please install unicodecsv! ")

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

    def __call__(self, env, context):
        pass

    def has_attr(self, attrName):
        return self.attrs.has_key(attrName)

    def select(self, context):
        """ select sub-context and yield generateor """
        if self.attrs.has_key('select'):
            #return py(context).find(self.attrs['select'])
            selector = self.attrs['select']
        else:
            # no selector is found
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
        """ eval with Evaluater """
        key_ctx = Evaluater.KEYNAME
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

    def __call__(self, env, element):
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
                    ch.append(callsite(env, child_context))
        return ch

class MapCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)

    def __call__(self, env, element):
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
                    ch[key] = callsite(env, child_context)
        return ch

class StringCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)

    def __call__(self, env, element):
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

    def __call__(self, env, element):
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

class RenderCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)

    def __call__(self, env, element, dic={}):
        ret_val = None
        if self.has_attr("type"):
            kind = self.attrs["type"]
        template_str = self.children
        ret_val = render(template_str, dic, kind=kind)
        return ret_val

class DataCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)

    def __call__(self, env, element):
        pass

class RootCallSite(MTCallSite):
    def __init__(self, exp):
        MTCallSite.__init__(self, exp)

    def __call__(self, env, doc, **environment):
        tag = self.attrs['_TAG_']
        # convert encoding
        if tag == "root" and self.has_attr('encoding'):
            encoding = self.attrs['encoding']
            doc = doc.decode(encoding)

        root_element = py(doc)

        results = []
        for tri in self.children:
            r = tri['exp_callsite'](env, root_element)
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
            json_conf = {'encoding': 'utf-8',
                         'ensure_ascii': False,
                         'indent': 4,
                         'sort_keys': True, }
            return json.dumps(results, **json_conf)
                        # json.dumps(results, encoding='utf-8', ensure_ascii=False, indent=4, sort_keys=True, )
        elif as_val == "yaml":
            yaml_conf = {'encoding': 'utf-8',
                         'allow_unicode': True,
                         'default_flow_style': False,
                         'line_break': True,
                         'indent': 4, }
            return yaml.dump(results, **yaml_conf)
                    # yaml.dump(results,
                    #        encoding='utf-8', allow_unicode=True, default_flow_style=False,
                    #        line_break=True, indent=4, )
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

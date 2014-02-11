#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from error import ExpressionError

# perl-like regex
# refer: http://www.troubleshooters.com/codecorn/littperl/perlreg.htm

is_match = re.compile(r'^[m/]')
is_sub = re.compile(r'^s')
get_delimiter = re.compile(r'[ms]*(.)')
is_insensitive = re.compile(r'i')
is_global = re.compile(r'g')

def regexp_parse(regex):
    '''
        Parse regex by perl-like syntax
    '''
    if regex is None or len(regex) <= 2:
        raise ExpressionError(regex, 'invalid regex: regex is none or too short')
    origin = regex
    r1 = '' # pattern 1
    r2 = '' # pattern 2
    kind = '' # search | extract | sub_1 | sub_all
    opts = re.UNICODE # options
    dd = get_delimiter.findall(regex)
    delimiter = dd[0] if dd else '/' # delimiter
    segs = regex.split(delimiter)
    r1 = segs[1]
    if is_match.search(regex):
        if len(segs) == 3:
            kind = 'search'
            optstr = segs[2]
        elif len(segs) == 4:
            kind = 'search_extract'
            r2 = segs[2]
            optstr = segs[3]
        else:
            raise ExpressionError(regex, 'invalid regex (match-format)')
    elif is_sub.search(regex):
        if len(segs) != 4: raise ExpressionError(regex, 'invalid regex (sub-format)')
        r2 = segs[2]
        optstr = segs[3]
        if is_global.search(optstr):
            kind = 'sub_all'
        else:
            kind = 'sub_1'
    else:
        raise ExpressionError(regex, 'invalid regex: could not be recognized')
    
    if is_insensitive.search(optstr):
        opts |= re.IGNORECASE
    
    return (r1, r2, kind, opts, origin)

def regexp_compile(r1, r2, kind, opts):
    '''
        Compile regex to function
    '''
    regex = re.compile(r1, opts)
    if kind == 'search':
        def search(text):
            return 1 if regex.search(text) else 0
        return search
    elif kind == 'search_extract':
        def search_extract(text):
            regex.search(text).expand(r2)
        return search_extract
    elif kind == 'sub_1':
        def sub_1(text):
            return regex.sub(r2, text, count=1)
        return sub_1
    elif kind == 'sub_all':
        def sub_all(text):
            return regex.sub(r2, text)
        return sub_all

class Regexp:
    '''
        Wrapper class of regexp_parse and regex_compile
    '''
    def __init__(self, regex):
        (self.r1, self.r2, self.kind, self.opts, self.origin) = regexp_parse(regex)
        self.regexp = regexp_compile(self.r1, self.r2, self.kind, self.opts)
        
    def __call__(self, text):
        return self.regexp(text)

def test():
    '''
        test suites
    '''
    print is_match.search(u'm/dfaf/i') is not None
    print is_match.search(u'/dfaf/') is not None
    print is_match.search(u'm#dfaf#') is not None

    print is_sub.search(u's/dfaf/dfaf') is not None

    print is_insensitive.search(u'ig') is not None
    print is_insensitive.search(u'') is None

    print is_global.search(u'ig')is not None
    print is_global.search(u'') is None

    print get_delimiter.findall(u's/dfa')[0] == '/'
    print get_delimiter.findall(u'm/dfa')[0] == '/'
    print get_delimiter.findall(u'##')[0] == '#'
    
    print len( u's/1/2/'.split('/') ) == 4
    print len( u'#1#2#'.split('#') ) == 4
    
    print regexp_parse('m/dfaf/ig')
    print regexp_parse('m#dfaf#')
    print regexp_parse('s#^[fda]$#dd#i')
    
    print Regexp(r'm/F/i').kind == 'search'
    print Regexp(r'/F/i').kind == 'search'
    print Regexp(r'm#F#!\1!#i').kind == 'search_extract'
    print Regexp(r's/F/1/i').kind == 'sub_1'
    print Regexp(r's/F/1/gi').kind == 'sub_all'

    print 'search', 'F/i', Regexp(r'm/F/i')('dddfaf fdadf') == True
    print 'search', 'F/', Regexp(r'm/F/')('dddfaf fdadf') == False
    print 'search', 'f/', Regexp(r'm/f/')('dddfaf fdadf') == True
    print 'search_extract', '', Regexp(r'm/(\w+) (\w+)/\2_\1/')('hello world ! ok done !') == 'world_hello'
    
    print 'sub_1', 'D/Z/i', Regexp(r's/D/Z/i')('dddfaf fdadf') == 'Zddfaf fdadf'
    print 'sub_all', 'D/Z/ig', Regexp(r's/D/Z/ig')('dddfaf fdadf') == 'ZZZfaf fZaZf'
    print 'sub_all', 'D/Z/g', Regexp(r's/D/Z/g')('dddfaf fdadf') == 'dddfaf fdadf'
    print 'sub_all', 'D+/Z/ig', Regexp(r's/D+/Z/ig')('dddfaf fdadf')

    
if __name__ == '__main__':
    test()


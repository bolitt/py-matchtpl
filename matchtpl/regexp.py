#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from error import ExpressionError

# perl-like regex
# refer: http://www.troubleshooters.com/codecorn/littperl/perlreg.htm

''' regexg: match mode '''
IS_MATCH_MODE = re.compile(r'^[m/]')
''' regexg: sub mode '''
IS_SUB_MODE = re.compile(r'^s')
''' get regexg: '''
GET_DELIMITER = re.compile(r'[ms]*(.)')
''' regexg: case insensitive '''
IS_INSENSITIVE = re.compile(r'i')
''' regexg: global match '''
IS_GLOBAL = re.compile(r'g')

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
    dd = GET_DELIMITER.findall(regex)
    delimiter = dd[0] if dd else '/' # delimiter
    segs = regex.split(delimiter)
    r1 = segs[1]
    if IS_MATCH_MODE.search(regex):
        if len(segs) == 3:
            kind = 'search'
            optstr = segs[2]
        elif len(segs) == 4:
            kind = 'search_extract'
            r2 = segs[2]
            optstr = segs[3]
        else:
            raise ExpressionError(regex, 'invalid regex (match-format)')
    elif IS_SUB_MODE.search(regex):
        if len(segs) != 4:
            raise ExpressionError(regex, 'invalid regex (sub-format)')
        r2 = segs[2]
        optstr = segs[3]
        if IS_GLOBAL.search(optstr):
            kind = 'sub_all'
        else:
            kind = 'sub_1'
    else:
        raise ExpressionError(regex, 'invalid regex: could not be recognized')
    
    if IS_INSENSITIVE.search(optstr):
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
            return regex.search(text).expand(r2)
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



#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Stack(list):
    def push(self, item):
        self.append(item)
    def peek():
        return self[-1]
    def length():
        return len(self)
    def is_empty(self):
        return len(self) == 0

class MTRuntime():
    def __init__(self, **kwargs):
        self.template = kwargs.get('template')
        self.mtcontext = kwargs.get('mtcontext')
        self._stack = Stack() # running stack
        
    @property
    def template(self):
        return self._template
    @template.setter
    def template(self, val):
        self._template = val

    @property
    def mtcontext(self):
        return self._mtcontext
    @mtcontext.setter
    def mtcontext(self, val):
        self._template = val

    @property
    def stack(self):
        return self._stack


    # running stack
    def push_stack(self, runtime_object):
        self._stack.append(runtime_object)
        
    def pop_stack(self):
        return self._stack.pop()

    def peek_stack(self):
        return self._stack.pop()

    def get_stack_length():
        return len(self._stack)
        

    


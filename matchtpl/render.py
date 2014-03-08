#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from jinja2 import Template
except ImportError:
    import warnings
    warnings.warn("Package jinja2 not found. <template> cannot be rendered with jinja2")


def render(template_str='Hello, {{ name }}!', obj={'name': 'matchtpl'}, kind='jinja2'):
    template = Template(template_str)
    return template.render(obj)

print render()

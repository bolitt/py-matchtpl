#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from jinja2 import Template as JTemplate
    def render_jinja2(template_str, dic):
        template = JTemplate(template_str)
        return template.render(dic)
except ImportError:
    import warnings
    warnings.warn("Package jinja2 not found. <template> cannot be rendered with jinja2")


# django needs settings.py, consider to add it later
#try:
#    from django.template import Template as DTemplate
#    from django.template import Context as DContext
#    def render_django(template_str, dic):
#        template = DTemplate(template_str)
#        context = DContext(dic)
#        return template.render(context)
#except ImportError:
#    import warnings
#    warnings.warn("Package jinja2 not found. <template> cannot be rendered with jinja2")

def render(template_str='Hello, {{ name }}!', dic={'name': 'matchtpl'}, kind='jinja2'):
    kind = kind.strip().lower()
    if kind == 'jinja2':
        return render_jinja2(template_str, dic)
    #elif kind == 'django':
    #    return render_django(template_str, dic)

if __name__ == "__main__":
    print render()

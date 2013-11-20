===========
py-matchtpl
===========

A python library to match and extract xml/html source with pre-defined 
template. It provides a convenient and coding-free way for data 
processing, especially for web page.

Take html as example. Matchtpl provides a easy way to parse your html file
and format output. You might find
it most useful for tasks involving <x> and also <y>. Typical usage
often looks like this::

    #!/usr/bin/env python

    from match import MTemplateEnv, MTemplate, MTemplateParser
	
    if __name__ == '__main__':
        # initialize environment
        env = MTemplateEnv(template = 'tpl_amazon.xml')
        # build template
        tpl = MTemplate()
        tpl.build(env)
        # initialize parser and parse
        parser = MTemplateParser(tpl)
        results = parser.parse('amazon.html')

(Note the double-colon and 4-space indent formatting above.)

Paragraphs are separated by blank lines. *Italics*, **bold**,
and ``monospace`` look like this.


A Section
=========

Lists look like this:

* First

* Second. Can be multiple lines
  but must be indented properly.

A Sub-Section
-------------

Numbered lists look like you'd expect:

1. hi there

2. must be going

Urls are http://like.this and links can be
written `like this <http://www.example.com/foo/bar>`_.


Contributors
============

* v0.1    Tian Lin<bolitt@gmail.com>
  Initialize the project, and alpha release of the library.


*Any contributions are welcome!*


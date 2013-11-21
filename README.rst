======================================
py-matchtpl: xml/html matching library
======================================

A python library to match and extract xml/html source with pre-defined 
template. It provides a convenient and coding-free way for data 
processing, especially for web page.

The features of ``matchtpl`` are summarized as follows:

* **Easy to use**. The goal is to help developer ease their text-data processing job. 
  Only basic knowledge of `jQuery <http://jquery.com>`_ (mostly, *CSSSelector*), one popular javascript
  DOM-manipulation library, is assumed. User only need to provide the XML-template to
  tell how to extract information and what the expected output is, then ``matchtpl`` will 
  finish the rest of the work.

* **User-friendly**. Our toolkit does not require coding in python. If you are to
  do very sophisticated work, py-matchtpl can take over dirty things, such as 
  parse html file, extract useful information, organize data into preferrable
  data structures, or streaming into *string* (plaintext) / `json <http://www.json.org/>`_ / `yaml <http://yaml.org/>`_ / python builtin structures (by default).
  
* **Extensibilty**. Currently, it supports three basic types of data structures: 
  (1) *string*; (2) *array*; (3) *map*. We can utilize their combination to meet the requirements
  in most cases. What's more, user can provide *UDF* (user-defined function) to customize in his/her 
  own way. 

The fundamental philosophy of ``matchtpl`` is:

* **Neat**: keep it clean and hide the dirty things.

* **Simple**: everything looks configurable, declarative and intuitive. (avoid to use complex control flow syntax: ``if``/``for``/``while``.)

* **Extensible**: leave imagination to user, and any ideas can be integrated in a rapid way.

Installation
=====================

You can install the latest package from source (or, download and unzip from github)::

  $ git clone https://github.com/bolitt/py-matchtpl.git
  
  $ python setup.py install


or use python easy_install or pip::

  $ easy_install matchtpl

  # alternatively install by pip

  $ pip install matchtpl



Basic Data Structures
=====================

1. **string**: ``<s></s>``. Typical atom structure, can be post-processed and
   converted into other types, like ``int``, ``float`` and etc.

2. **array**: ``<array></array>``. An ordered list of data, also known as list.
   It can be retrieved by its index: *array[0]*.

3. **map**: ``<map></map>``. A key-value based structure, also known as hash or table.
   It can be retrieved by key-like way: *map['name']* or by property-like way: *map.name*.

We believe most data can be fit into those data structures or their combinations.


Keywords & Elements
-------------------------

Here are typical keywords:

* **select**: select target element(s) from document.
    * selector_string (string): CSS3 Selector to choose target.

* **get**: get internal text | html of target DOM element.
    * type (string): "text" | "html". 

* **eval**: locally evaluate via python syntax. (Often used to call jquery-like API.)
    * script_text (string): script using python syntax.

* **default**: default value if none.
    * value (string): default value.

* **as**: output format in human-readable way.
    * type (string): str | json | yaml. If not provided, will return python builtin data strucutures.

(Keywords are not limited as above.)


And extensible elements are:

* Strucuture element: ``<s></s>``, ``<array></array>``, ``<map></map>`` (see: above).

* Root element: ``<root></root>``. Act as serilization class, and provide multiple formats to output result.

* Customized element: ``<action></action>``, where *action* here can be other non-conflictive tag. *action* is a
  customized action provide by user when calling *parser.parse(..., {'action': some_function})*.


Quick Start
=====================

The example shows how to extract data from html source. 
Matchtpl provides an easy way to parse your html file
and format output. It is a real case to extract products
information from web page of amazon.com.


Python Code
------------------------

In python, typical usage often looks like this::

    #!/usr/bin/env python

    from matchtpl import MTemplateEnv, MTemplate, MTemplateParser
	
    if __name__ == '__main__':
        # initialize environment
        env = MTemplateEnv(template = 'tpl_amazon.xml')
        
        # build template
        tpl = MTemplate()
        tpl.build(env)

        # initialize parser and parse
        parser = MTemplateParser(tpl)
        results = parser.parse('amazon.html')


Configurable Template
------------------------

The pre-defined template is written in xml, which acts as a
config file to indicates the meta information of the target 
(usually another html/xml file or stream). Then,
parser will use the template to guide its processing, and 
output the result::

    <!-- serilize result as json. (other format is also supported) -->
    <root as="json">
        <!-- the collection of entries are started with 'result_*' in their IDs,
             and each entry is a map -->
        <array select="div[id^='result_']" >
	    <map>
                <!-- title: get internal text as result -->
                <s key="title" select="h3 span.lrg" get="text" />
                <s key="info" select="h3 span.med" get="text" />
                <!-- image: get src link in jquery-like way -->
                <s key="image" select="div.image img.productImage" eval="attr('src')" />
                <!-- price: pseudo-class of CSSSelector is used -->
                <s key="price" select="li.newp span:eq(0)" get="text" />
                <!-- review: default value is enabled -->
                <s key="review" select="span.asinReviewsSummary a" eval="attr('alt')" default='0' />
            </map>
        </array>
    </root>


After execution, the output is organized as json::

    [
        [
            {
                "image": "http://ec4.images-amazon.com/images/I/516Vhic-I9L._AA160_.jpg", 
                "info": "刘亚莉 广东省出版集团，广东经济出版社  (2011-05) - Kindle电子书", 
                "price": "￥1.99", 
                "review": "平均4.4 星", 
                "title": "总经理财务一本通"
            }, 
            // up to 25 results: map
        ]
    ]

(At present, json, yaml, plaintext or python builtin structures are allowed. More format will be supported later.)


Future Scenarios
=================

Possible functionalities:

1. Unix-like pipe: ``|``. Just concatenate output|input step by step.

2. Interactive. Interaction with pages: like doing automation/login/testing.

3. Type-casting. convert type into int/float, or direct instantiation of a class.

4. Regex support ``/^abcd/ABCD/g`` and some basic UDFs, like split/trim/toUpper/toLower.

Project Links
==============
**Package Release**: https://pypi.python.org/pypi/matchtpl

**Source Code**: https://github.com/bolitt/py-matchtpl.git 


Contributors
==============

* v0.1    Tian Lin<bolitt@gmail.com>
  Initialize the project, and alpha release of the library.


*Any contributions are welcome!*


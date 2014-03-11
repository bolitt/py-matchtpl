from setuptools import setup, find_packages
from sys import version
import os
if version < '2.6.0':
    raise Exception("This module doesn't support any version less than 2.6")

def read(filename):
    if os.path.isfile(filename):
        fd = open(filename)
        value = fd.read()
        fd.close()
    else:
        value = ''
    return value

long_description = """
%(README)s

See https://pypi.python.org/pypi/matchtpl for the full documentation

News
====

%(CHANGES)s

""" % { 'README': read('README.rst'), 'CHANGES': read('CHANGES.rst') }


classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

TXT_EXTS = ['*.txt', '*.rst']
CONF_EXTS = ['*.conf']
WEB_EXTS = ['*.js', '*.css', '*.html', '*.htm']

setup(
    name = 'matchtpl',
    version = '0.2.0',
    author = 'Tian L.',
    author_email = 'bolitt@gmail.com',
    url = 'https://github.com/bolitt/py-matchtpl.git',
    license = 'BSD license',
    description = 'Matching template to extract data from xml or html',
    keywords = 'match template crawler extract data xml html',
    long_description = long_description,
    classifiers = classifiers,
    packages = find_packages(),
    #    '_': ['matchtpl'],
    #    'etc': ['matchtpl/etc'],
    #    'web': ['matchtpl/web'],
    #    'future': ['matchtpl/future'],
    #},
    include_package_data=True,
    package_data = {
        '': CONF_EXTS + TXT_EXTS + WEB_EXTS,
    },
    install_requires = {
        'pyquery': 'pyquery>=1.2.6',
	'lxml': 'lxml>=2.1',
        'cssselect': 'cssselect',
    },
    extras_require = {
        'yaml': ['PyYAML>=3.10'],
    },
    test_suite = 'matchtpl.tests.test1',
    entry_points="""
      # -*- Entry points: -*-
    """,
)

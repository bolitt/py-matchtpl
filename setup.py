from setuptools import setup
from sys import version
import matchtpl, os
if version < '2.6.0':
    raise Exception("This module doesn't support any version less than 2.6")

def read(*names):
    values = dict()
    for name in names:
        filename = name + ".rst"
        if os.path.isfile(filename):
            fd = open(filename)
            value = fd.read()
            fd.close()
        else:
            value = ''
        values[name] = value
    return values

long_description = """
%(README)s

See https://pypi.python.org/pypi/matchtpl for the full documentation

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')


classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name = 'matchtpl',
    version = matchtpl.__version__,
    author = 'Tian L.',
    author_email = 'bolitt@gmail.com',
    url = 'https://github.com/bolitt/py-matchtpl.git',
    license = 'BSD license',
    description = 'Matching template to extract data from xml or html',
    keywords = 'match template crawler extract data xml html',
    long_description = long_description,
    classifiers = classifiers,
    packages = [
        'matchtpl',
    ],
    install_requires = [
        'pyquery>=1.2.6',
	'lxml>=3.1.2',
        'cssselect>=0.9.1',
    ],
    test_suite = 'matchtpl.tests.test1',
    entry_points="""
      # -*- Entry points: -*-
    """,
)

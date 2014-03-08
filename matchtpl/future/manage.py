#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re
import os
import codecs
from pprint import pprint
import argparse

from matchtpl.fixpath import fixpath, usemodule
fixpath()
# use this for testers

from core import MTemplateEnv, MTemplate, MTemplateParser

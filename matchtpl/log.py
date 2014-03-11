#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.config

''' lib directory '''
LIB_DIR = os.path.dirname(__file__)

''' logging '''
logging.config.fileConfig(os.path.join(LIB_DIR, 'etc', "logging.conf"))
LOGGER = logging.getLogger('root')

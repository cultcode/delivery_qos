#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import os
import sys
import logging
import stat

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from delivery_qos import shell, common
from delivery_qos.common import check_link, clear_dirty, sortdir

def scan():
  config = shell.get_config()
  logging.info("ttt")

if __name__ == '__main__':
  scan()

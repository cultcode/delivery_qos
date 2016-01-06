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

def scan_store():
  config = shell.get_config()
  shell.check_config(config)

  paths = sorted(config["paths"])
  index = paths.index(config['last_path'])
  paths = paths[index:].extend(paths[:index])

  for index,path in enumerate(paths):
    if index == 0:
      filter_cond = lambda e:e[1].st_mtime >= config['last_mtime']
    elif index == len(paths) -1:
      filter_cond = lambda e:e[1].st_mtime <  config['last_mtime']
    else:
      filter_cond = lambda e:e[1].st_mtime <=

    config['last_path'] = path

    filenames = sortdir(path, sort_cond='mtime', filter_cond=filter_cond)

    for filename in filenames:
      config['last_mtime'] = os.stat(filename).st_mtime

      check_link(filename)
      clear_dirty(filename, config['recyle_bin'])

  shell.set_config(config)


def scan_incr():
  config = shell.get_config()

if __name__ == '__main__':
  scan_store()

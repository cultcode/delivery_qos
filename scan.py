#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import os
import sys
import time
import logging
import stat

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from delivery_qos.common import scan_file, sortdir
from delivery_qos import shell
from delivery_qos.shell import get_config, set_config

def scan_store():
  get_config()

  paths = shell.config['paths']
  index = paths.index(shell.config['scan_store_last_path'])
  paths = paths[index:] + paths[:index+1]
  scan_store_mtime_end = time.time() - shell.config["scan_store_mtime_end"]
  scan_store_last_mtime = shell.config['scan_store_last_mtime']

  for index,path in enumerate(paths):
    if index == 0:
      filter_cond = lambda e:e.st_mtime >= scan_store_last_mtime and e.st_mtime < scan_store_mtime_end
    elif index == len(paths) -1:
      filter_cond = lambda e:e.st_mtime <  scan_store_last_mtime and e.st_mtime < scan_store_mtime_end
    else:
      filter_cond = lambda e:e.st_mtime <  scan_store_mtime_end

    shell.config['scan_store_last_path'] = path

    filenames = sortdir(path, sort_cond='mtime', filter_cond=filter_cond)

    for filename in filenames:
      shell.config['scan_store_last_mtime'] = os.stat(filename).st_mtime

      scan_file(filename, shell.config['recyle_bin'])

    logging.info("Scan_store %s completed: %d files in total" %(path,len(filenames)))

  set_config()


def scan_incr():
  get_config()

  paths = shell.config["paths"].sort()
  scan_incr_mtime_start = time.time() - shell.config["scan_incr_mtime_start"]

  for index,path in enumerate(paths):
    filter_cond = lambda e:e[1].st_mtime > scan_incr_mtime_start

    filenames = sortdir(path, sort_cond='mtime', filter_cond=filter_cond)

    for filename in filenames:
      scan_file(filename, shell.config['recyle_bin'])

    logging.info("Scan_incr %s completed: %d files in total" %(path,len(filenames)))


if __name__ == '__main__':
  scan_store()

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import os
import sys
import signal
import stat
import time
import logging
import stat
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from delivery_qos.common import get_paths, sortdir, scan_file, disk_overuse,clear_file
from delivery_qos import shell
from delivery_qos.shell import get_config, set_config

def signal_term_handler(signal, frame):
  logging.warn('got SIGTERM')
  set_config()
  sys.exit(0)

def scan_store():
  logging.info("Scan_store started")

  paths = get_paths(shell.config['paths'],shell.config['subdir_level'])

  if shell.config['scan_store_last_path'] in paths:
    index = paths.index(shell.config['scan_store_last_path'])
  else:
    index = 0
  paths = paths[index:] + paths[:index+1]
  scan_store_mtime_end = time.time() - shell.config["scan_store_mtime_end"]
  scan_store_last_mtime = shell.config['scan_store_last_mtime']

  for index,path in enumerate(paths):
    if index == 0:
      filter_cond = lambda e:not stat.S_ISLNK(e.st_mode) and e.st_mtime >= scan_store_last_mtime and e.st_mtime < scan_store_mtime_end
    elif index == len(paths) -1:
      filter_cond = lambda e:not stat.S_ISLNK(e.st_mode) and e.st_mtime <  scan_store_last_mtime and e.st_mtime < scan_store_mtime_end
    else:
      filter_cond = lambda e:not stat.S_ISLNK(e.st_mode) and e.st_mtime <  scan_store_mtime_end

    shell.config['scan_store_last_path'] = path

    filenames = sortdir(path, sort_cond='mtime', filter_cond=filter_cond)

    for filename in filenames:
      shell.config['scan_store_last_mtime'] = os.stat(filename).st_mtime

      scan_file(filename, shell.config['recyle_bin'])

    logging.info("Scan_store %s completed: %d files in total" %(path,len(filenames)))

  set_config()


def scan_incr():
  logging.info("Scan_incr started")

  paths = get_paths(shell.config['paths'],shell.config['subdir_level'])

  now_year = time.localtime(time.time()).tm_year
  paths = map(lambda path:re.search('/%d/' %now_year, path) and path or None, paths)

  scan_incr_mtime_start = time.time() - shell.config["scan_incr_mtime_start"]

  for index,path in enumerate(paths):
    if not path:
      continue
    filter_cond = lambda e:not stat.S_ISLNK(e.st_mode) and e.st_mtime > scan_incr_mtime_start

    filenames = sortdir(path, sort_cond='mtime', filter_cond=filter_cond)

    for filename in filenames:
      scan_file(filename, shell.config['recyle_bin'])

    logging.info("Scan_incr %s completed: %d files in total" %(path,len(filenames)))


def scan_disk():
  logging.info("Scan_disk started")

  paths = shell.config['paths']
  ret = False

  for index,path in enumerate(paths):
    if disk_overuse(path,shell.config['disk_max_usage']):
      ret = True
      filter_cond = lambda e:not stat.S_ISLNK(e.st_mode)
      filenames = sortdir(path, sort_cond='atime', filter_cond=filter_cond)
      amount = int(len(filenames)*0.01)
      logging.info("%s overused, removing %d files (%d in total)" %(path,amount, len(filenames)))
      for filename in filenames[0:amount]:
        clear_file(filename)

      logging.info("Scan_disk %s completed" %(path))

  return ret


def scan():
  get_config('delivery_scan')
  signal.signal(signal.SIGTERM, signal_term_handler)

  now_hour = time.localtime(time.time()).tm_hour

  if now_hour in range(shell.config['scan_disk_span_start'],shell.config['scan_disk_span_end']):
    if scan_disk():
      return

  if now_hour in range(shell.config['scan_store_span_start'],shell.config['scan_store_span_end']):
    scan_store()

  #if now_hour in range(shell.config['scan_incr_span_start'],shell.config['scan_incr_span_end']):
  #  scan_incr()

if __name__ == '__main__':
  scan()

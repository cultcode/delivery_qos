#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import os
import sys
import stat
import logging
import hashlib

def extract_symlink(filename):
  if not (os.path.isfile(filename) and not os.path.islink(filename)):
    return None

  dirname  = os.path.dirname(filename)
  basename = os.path.basename(filename)

  parts = basename.split('.')

  if parts and (len(parts) >= 2):
    symlinkname = os.path.join(dirname,'.'.join(parts[:2]))
    return symlinkname

  return None


def extract_md5(filename):
  if not (os.path.isfile(filename) and not os.path.islink(filename)):
    return None

  dirname  = os.path.dirname(filename)
  basename = os.path.basename(filename)

  parts = basename.split('.')

  if parts and (len(parts) >= 2) and (len(parts[-2]) == 32):
    return parts[-2]
  else:
    return None


def md5sum(filename):
  try:
    with open(filename,'rb') as f:
      md5obj = hashlib.md5()
      md5obj.update(f.read())
      hash_data = md5obj.hexdigest()
      return hash_data
  except:
    return None


def check_link(filename):
  symlinkname = extract_symlink(filename)

  if not symlinkname or symlinkname == filename:
    return False

  if not (os.path.islink(symlinkname) and os.path.exists(symlinkname) and os.path.samefile(os.readlink(symlinkname), filename)):
    logging.info("repairing symbolic link %s for %s" %(symlinkname,filename))
    os.path.lexists(symlinkname) and os.remove(symlinkname)
    os.symlink(filename,symlinkname)
    return True

  return False

def clear_dirty(filename,recyle_bin):
  symlinkname = extract_symlink(filename)
  md5_name = extract_md5(filename)
  md5_cal  = md5sum(filename)
  dirname  = os.path.dirname(filename)
  basename = os.path.basename(filename)

  if md5_name and md5_cal and cmp(md5_name,md5_cal):
    logging.info("clearing dirty file %s" %(filename))
    if symlinkname:
      os.path.lexists(symlinkname) and os.remove(symlinkname)
    os.rename(filename, os.path.join(recyle_bin,basename))
    

def scan_file(filename, recyle_bin):
  logging.info("Scanning file %s" %(filename))

  basename = os.path.basename(filename)
  ext = basename.split('.')[-1]
  if ext == "ng":
    check_link(filename)
    clear_dirty(filename, recyle_bin)

    
def sortdir(path, sort_cond = 'mtime', filter_cond = None, reverse = False, abspath = True, onlyfn = True):
  '''
  '''
  if sort_cond == "mtime":
    f_sort_cond = lambda e:e[1].st_mtime
  elif sort_cond == "ctime":
    f_sort_cond = lambda e:e[1].st_ctime
  elif sort_cond == "atime":
    f_sort_cond = lambda e:e[1].st_atime
  elif sort_cond == "size":
    f_sort_cond = lambda e:e[1].st_size
  else:
    f_sort_cond = lambda e:e[1].st_mtime

  f_sf = None
  if filter_cond == None or filter_cond == 3:
    f_sf = None
  elif type(filter_cond) == type(lambda x:x):
    f_sf = filter_cond
  else:
    if filter_cond == 1:
      f_sf = lambda e: stat.S_ISDIR(e.st_mode) == 0
    elif filter_cond == 2:
      f_sf = lambda e: stat.S_ISDIR(e.st_mode)
    else:
      f_sf = None

  if onlyfn:
    return map(lambda e:e[0], __sortdir(path, f_sort_cond, f_sf, reverse, abspath))

  return __sortdir(path, f_sort_cond, f_sf, reverse, abspath)


def __sortdir(path, sort_cond, filter_cond, reverse, abspath):
  '''
  '''
  fns = os.listdir(path)

  a_fns = map(lambda f: os.path.join(path,f), fns)
  sts = map(os.stat, a_fns)

  if abspath:
    res = zip(a_fns, sts)
  else:
    res = zip(fns, sts)

  if filter_cond == None:
    return sorted(res, key = sort_cond, reverse = reverse)

  n_res = []
  for e in res:
    if filter_cond(e[1]):
      n_res.append(e)

  return sorted(n_res, key = sort_cond, reverse = reverse)


if __name__ == '__main__':
  print(str(sortdir(sys.argv[1],sort_cond='mtime')))


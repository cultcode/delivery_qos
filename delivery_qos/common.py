#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import os
import sys
import statvfs
import stat
import logging
import hashlib

import scandir

def disk_overuse(path,disk_max_usage):
  vfs=os.statvfs(path)
  available=vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]/(1024*1024*1024)
  capacity=vfs[statvfs.F_BLOCKS]*vfs[statvfs.F_BSIZE]/(1024*1024*1024)  
  if (capacity-available)/capacity >= disk_max_usage:
    logging.info("disk overused %s %dG %dG " %(path, available,capacity))
    return True
  else:
    logging.info("disk not overused %s %dG %dG " %(path, available,capacity))
    return False


def extract_symlink(filename):
  if not (os.path.isfile(filename) and not os.path.islink(filename)):
    return None

  dirname  = os.path.dirname(filename)
  basename = os.path.basename(filename)

  parts = basename.split('.')
  ext = parts and parts[-1] or ''

  if ext == 'ng':
    if (len(parts) >= 2):
      symlinkname = os.path.join(dirname,'.'.join(parts[:2]))
  else:
    return None

  if symlinkname == filename:
    return None

  return symlinkname


def extract_md5(filename):
  if not (os.path.isfile(filename) and not os.path.islink(filename)):
    return None

  dirname  = os.path.dirname(filename)
  basename = os.path.basename(filename)

  parts = basename.split('.')
  ext = parts and parts[-1] or ''

  if ext == 'ng':
    if (len(parts) >= 2) and (len(parts[-2]) == 32):
      return parts[-2]
    else:
      return None
  elif ext == 'mp4' or ext == 'm3u8':
    frags = parts[0].split('_')
    if frags and frags[0] and (len(frags[0]) == 32):
      return frags[0]
    else:
      return None
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

  if not symlinkname:
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
    

def clear_file(filename):
  logging.info("clearing file %s" %(filename))
  symlinkname = extract_symlink(filename)
  if symlinkname:
    os.path.lexists(symlinkname) and os.remove(symlinkname)

  basename = os.path.basename(filename)
  ext = basename.split('.')[-1]
  if ext != "m3u8":
    os.remove(filename)


def scan_file(filename, recyle_bin):
  logging.info("Scanning file %s" %(filename))

  basename = os.path.basename(filename)
  ext = basename.split('.')[-1]
  if ext == "ng":
    check_link(filename)
    clear_dirty(filename, recyle_bin)

    
def sortdir(path, sort_cond = 'mtime', filter_cond = None, reverse = False):
  '''
  '''
  logging.info('scanning filesystem : %s' %path)

  if sort_cond == "mtime":
    _sort_cond = lambda e:e[1].st_mtime
  elif sort_cond == "ctime":
    _sort_cond = lambda e:e[1].st_ctime
  elif sort_cond == "atime":
    _sort_cond = lambda e:e[1].st_atime
  elif sort_cond == "size":
    _sort_cond = lambda e:e[1].st_size
  else:
    _sort_cond = lambda e:e[1].st_mtime

  if filter_cond == None or filter_cond == 3:
    _filter_cond = None
  elif type(filter_cond) == type(lambda x:x):
    _filter_cond = filter_cond
  else:
    if filter_cond == 1:
      _filter_cond = lambda e: stat.S_ISDIR(e.st_mode) == 0
    elif filter_cond == 2:
      _filter_cond = lambda e: stat.S_ISDIR(e.st_mode)
    else:
      _filter_cond = None

  res = list(__sortdir(path, _filter_cond))
  res = sorted(res, key = _sort_cond, reverse = reverse)
  return map(lambda e:e[0], res)


def __sortdir(path, filter_cond):
  '''
  '''
  for entry in scandir.scandir(path):
    if not entry.name.startswith('.'):
      if entry.is_dir(follow_symlinks=False):
        for e in __sortdir(entry.path,filter_cond):
          yield e
      else:
        if filter_cond and not filter_cond(entry.stat(follow_symlinks=False)):
          pass
        else:
          yield (entry.path,entry.stat(follow_symlinks=False))


def get_subdirs(path,level):
  """Yield directory names not starting with '.' under given path."""
  if level < 0:
    return
  elif level == 0:
    yield path
  else:
    for entry in scandir.scandir(path):
      if entry.is_dir():
        for subdir in  get_subdirs(entry.path, level-1):
          yield subdir
      #else:
      #  pass
      #  yield entry.path


def get_paths(paths,level):
  subdirs=[]

  for path in paths:
    for subdir in get_subdirs(path,level):
      subdirs.append(subdir)

  subdirs.sort()
  logging.info("completed:%s" %str(subdirs))

  return subdirs


if __name__ == '__main__':
  #print(str(sortdir(sys.argv[1],sort_cond='mtime')))
  for subdir in get_subdirs('/data/mp4/2015/dianshiju/',1):
    print(subdir)


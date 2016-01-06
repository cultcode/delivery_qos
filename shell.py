from __future__ import absolute_import, division, print_function, \
    with_statement

import os
import sys
import logging

def find_config():
  config_path = 'config.json'
  if os.path.exists(config_path):
    return config_path

  config_path = os.path.join('/etc',(__name__.split('.'))[0]+'.json')
  if os.path.exists(config_path):
    return config_path

  return None

def get_config():
  config = {}
  config_extra = {}
  config_path = find_config()

  if config_path:
    logging.info('loading extra config from %s' % config_path)
    try:
      with open(config_path, 'rb') as f:
        config_extra = json.loads(f.read().decode('utf8'))
    except Exception as e:
      logging.error("Can't file.read %s:%s, give up" %(config_path,e))

  if config_extra:
    config.update(config_extra)

  if not config:
    logging.warn('config not specified')

  config.setdefault('log-file', sys.argv[0]+".log")

  logging.getLogger('').handlers = []
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(filename)s %(funcName)s %(lineno)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=config['log-file'],
    filemode='w'
  )

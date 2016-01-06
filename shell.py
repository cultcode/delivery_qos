from __future__ import absolute_import, division, print_function, \
    with_statement

import os
import sys
import json
import logging

def check_config(config):
  assert(config["recyle_bin"])
  os.path.lexists(config["recyle_bin"]) or os.makedirs(config["recyle_bin"])
  assert(config["paths"])

def set_config(config):
  config_path = config["config_path"]

  if config_path:
    logging.info('dumping config to %s' % config_path)
    try:
      with open(config_path, 'wb') as f:
        f.write(json.dumps(config).encode('utf8'))
    except Exception as e:
      logging.error("Can't file.write %s:%s, give up" %(config_path,e))


def get_config():
  config = {}
  config_path = os.path.join('/etc',(__name__.split('.'))[0]+'.json')

  if os.path.exists(config_path):
    try:
      with open(config_path, 'rb') as f:
        config = json.loads(f.read().decode('utf8'))
    except Exception as e:
      logging.error("Can't file.read %s:%s, give up" %(config_path,e))

  config.setdefault('log-file', os.path.join('/var/log',(__name__.split('.'))[0]+'.log'))
  config.setdefault('config_path',config_path)

  logging.getLogger('').handlers = []
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(filename)s %(funcName)s %(lineno)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=config['log-file'],
    filemode='w'
  )

  logging.info(str(config))

  return config

from __future__ import absolute_import, division, print_function, \
    with_statement

import os
import sys
import json
import logging

config = {}

def check_config():
  global config

  os.path.lexists(config["recyle_bin"]) or os.makedirs(config["recyle_bin"])

def set_config():
  global config

  config_path = config["config_path"]

  if config_path:
    logging.info('dumping config to %s' % config_path)
    try:
      with open(config_path, 'wb') as f:
        f.write(json.dumps(config).encode('utf8'))
    except Exception as e:
      logging.error("Can't file.write %s:%s, give up" %(config_path,e))


def get_config():
  global config
  config = {}

  config_path = os.path.join('/etc',(__name__.split('.'))[0]+'.json')

  if os.path.exists(config_path):
    try:
      with open(config_path, 'rb') as f:
        config = json.loads(f.read().decode('utf8'))
    except Exception as e:
      logging.error("Can't file.read %s:%s, give up" %(config_path,e))
      sys.exit(1)

  config.setdefault('log-file', os.path.join('/var/log',(__name__.split('.'))[0]+'.log'))

  logging.getLogger('').handlers = []
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(filename)s %(funcName)s %(lineno)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    #filename=config['log-file'],
    filemode='a'
  )

  #common parameters
  config.setdefault('config_path',config_path)
  config.setdefault("recyle_bin", os.path.join('/tmp',__name__.split('.')[0]))

  #parameters for scan_store
  config.setdefault('scan_store_mtime_end', 7*24*3600)
  config.setdefault('paths', ['/data/mp4'])
  config.setdefault('scan_store_last_path', config['paths'][0])
  config.setdefault('scan_store_last_mtime', 0)

  #parameters for scan_incr
  config.setdefault('scan_incr_mtime_start', 5*60)

  #parameters for scan_disk
  config.setdefault('disk_max_usage', 0.97)

  #span
  config.setdefault('scan_store_span_start',1)
  config.setdefault('scan_store_span_end',8)
  config.setdefault('scan_incr_span_start',8)
  config.setdefault('scan_incr_span_end',12)
  config.setdefault('scan_disk_span_start',1)
  config.setdefault('scan_disk_span_end',2)

  check_config()

  logging.info(str(config))


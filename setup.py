#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
setup(
  name='delivery_qos',
  version='1.3.2',
  author='rovere',
  author_email='luowei@mgtv.com',
  url = "https://github.com/cultcode/delivery_qos",
  packages=['delivery_qos'],
  data_files=[('/etc/cron.d', ['delivery_qos/data/etc/cron.d/delivery_scan']),
              ('/etc/logrotate.d', ['delivery_qos/data/etc/logrotate.d/delivery_scan']),
              ('/etc', ['delivery_qos/data/etc/delivery_scan.json'])
             ],
  entry_points={
    "console_scripts":[
      '''delivery_scan = delivery_qos.scan:scan''',
    ]
  },
)   


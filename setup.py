#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
setup(
  name='delivery_qos',
  version='1.0.3',
  author='rovere',
  author_email='luowei@mgtv.com',
  url = "https://github.com/cultcode/delivery_qos",
  packages=['delivery_qos'],
  #install_requires=['scandir'],
  data_files=[('/etc/cron.d', ['data/etc/cron.d/delivery_scan']),
              ('/etc', ['data/etc/delivery_scan.json'])
             ],
  entry_points={
    "console_scripts":[
      '''delivery_scan = delivery_qos.scan:scan''',
    ]
  },
)   


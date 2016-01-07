#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
setup(
  name='delivery_qos',
  version='1.0',
  author='rovere',
  author_email='luowei@mgtv.com',
  packages=['delivery_qos'],
  install_requires=[],
  data_files=[('/etc/init.d', ['/root/luowei/delivery_qos/delivery_scan'])
  ],
  entry_points={
    "console_scripts":[
      '''delivery_scan = delivery_qos.scan:scan''',
    ]
  },
)   


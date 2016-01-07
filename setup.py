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
  entry_points={
    "console_scripts":[
      '''delivery_qos = delivery_qos.scan:scan''',
    ]
  }
)   


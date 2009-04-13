#!/usr/bin/env python
''' Installation script for choiceyana package 
'''
from os.path import join
from glob import glob
from distutils.core import setup

setup(name='choiceyana',
      version='0.1a',
      description='Choiceyana package',
      author='Matthew Brett',
      author_email='matthew.brett@gmail.com',
      url='http://imaging.mrc-cbu.cam.ac.uk/svn/choiceyana',
      packages=['choiceyana'],
      scripts=glob('scripts/*.py'),
      )


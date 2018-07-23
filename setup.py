#!/usr/bin/env python3
# from distutils.core import setup
from setuptools import setup, find_packages
from os import path
from io import open
proj_path = path.abspath(path.dirname(__file__))
with open(path.join(proj_path, 'README.md'), encoding='utf-8') as f:
    longdesc = f.read()

setup(
    name='terse',
    version='0.0.2',
    description='a collection of function decorators to handle common procedures done on the entry and exit points.',
    author='Chad Lucas',
    author_email='cjlucas85@gmail.com',
    url='https://github.com/cjlucas85/terse',
    packages=find_packages(),
    long_description=longdesc,
    long_description_content_type='text/markdown',
    # packages=['distutils', 'distutils.command'],
)

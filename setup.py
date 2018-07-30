#!/usr/bin/env python3
from setuptools import setup, find_packages
from os import path
import pypandoc
proj_path = path.abspath(path.dirname(__file__))
md_path = path.join(proj_path, 'README.md')
long_description = pypandoc.convert(md_path, 'rst')

setup(
    author='Chad Lucas',
    author_email='cjlucas85@gmail.com',
    description='a collection of function decorators to handle common procedures done on the entry and exit points.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='terse',
    url='https://github.com/cjlucas85/terse',
    version='0.0.6',
    packages=find_packages(),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ),
)

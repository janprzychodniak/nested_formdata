#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('drf_nested_forms')

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='drf_nested_forms',
    version=version,
    url='http://github.com/emperorDuke/nested_formdata',
    download_url='http://github.com/emperorDuke/nested_formdata/archive/v1.1.7.tar.gz',
    license='MIT',
    description='A library that parses nested json or form data to python object',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['drf', 'nested form', 'html_forms' 'drf_nested_forms', 'restframework', 'nested json'],
    author='Duke Effiom',
    author_email='effiomduke@gmail.com',
    packages=['drf_nested_forms'],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
    ], 
    test_suite='tests',
    tests_require=[
        'djangorestframework',
        'django'
    ]
)

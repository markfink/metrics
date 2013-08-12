#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
    have_setuptools = True
except ImportError:
    from distutils.core import setup
    def find_packages():
        return [
            'korg',
        ]
    have_setuptools = False
from metrics import __version__

setup(
    author = 'Mark Fink',
    author_email = 'mark@mark-fink.de',
    description = 'metrics produces metrics for C, C++, Javascript, and Python programs',
    long_description=open('README.md').read(),
    url = 'https://github.com/metrics/',
    download_url='http://pypi.python.org/pypi/metrics',
    name='metrics',
    version=__version__,
    packages = find_packages(),
    include_package_data=True,
    install_requires = ['Pygments>=0.8',],
    license='MIT License',
    extras_require = {'test': ['nose', 'coverage'],},
    entry_points={
        'console_scripts': ['metrics = metrics.metrics:main',],
        },
    test_suite='nose.collector',
    #test_requires=['nose', 'coverage'],
    platforms = 'any',
    zip_safe = False,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Natural Language :: English',
    ],
)

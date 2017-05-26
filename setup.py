#! /usr/bin/env python3

# Dependency
import setuptools
# Project
import metrics

setuptools.setup(
    author="Mark Fink",
    author_email="mark@mark-fink.de",
    description="Metrics produces metrics for C, C++, Python and more",
    long_description=open("README.rst").read(),
    url="https://github.com/markfink/metrics",
    name="metrics",
    version=metrics.__version__,
    packages=["metrics"],
    include_package_data=True,
    license="MIT License",
    entry_points={
        'console_scripts': ["metrics = metrics.main:main", ],
    },
    platforms="any",
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Natural Language :: English",
    ],
)

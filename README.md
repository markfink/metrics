[![License](http://img.shields.io/badge/license-MIT-yellowgreen.svg)](MIT_LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/finklabs/metrics.svg?maxAge=2592000)](https://github.com/finklabs/metrics/issues)


# metrics

The original idea of metrics was a platform that can be extended with many different metrics. At the time I will focus only on SLOC and McCabe complexity metrics. *metrics* is build in a way to support many, many languages [supported languages](http://pygments.org/languages/). Currently we test support for Python, C, C++, Go and JavaScript.

The SLOC metric counts the lines but excludes empty lines and comments. This is sometimes referred to as the *source lines of code* (SLOC). In literature this is often also referred as physical lines of code. I simplified it to something which to my understanding is the common denominator for the metric packages I looked into  (CCCC, SLOCCount, PyMetrics, Eclipse-Metrics, Ohcount). 


# installation

**metrics** is released as a Python package so you can apply the std. Python 
mechanism for installation:

``` bash
$ pip install metrics
```

Some plugins are available to collect information from a typical development environment.
If you have a similar environment you can install them as well in one go:

``` bash
$ pip install metrics metrics.bumpversion metrics.gitinfo metrics.pylint metrics.pytest-cov
```


# Sample use

Get an overview on a package (number of files, used languages, and metrics):

``` bash
$ metrics **/*
Metrics Summary:
Files                       Language        SLOC Comment McCabe 
----- ------------------------------ ----------- ------- ------ 
    6                              C          14       3      0 
    3                            C++        1114     236    108 
    1                            INI           5       0      0 
    2                           Java          27       8      1 
    3                     JavaScript        1453      54    169 
    1                       markdown           7       0      0 
   18                         Python        1038     425    238 
   11                      Text only           0       0      0 
----- ------------------------------ ----------- ------- ------ 
   45                          Total        3658     726    516 
```

Note how you can use glob file pattern or a list of files...


Usage help:

``` bash
$ metrics --help
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -f IN_FILE_LIST, --files=IN_FILE_LIST
                        File containing list of path names to modules for
                        analysis.
  -q, --quiet           suppress normal summary output to stdout. (Default is
                        False)
  --format=OUTPUT_FORMAT_STR
                        Choose an output format for a parser to read. Valid
                        choices: xml, csv, json
```


Get a detailed report:

``` bash
$ metrics -q --format=csv metrics/metrics.py
filename,sloc,comments,ratio_comment_to_code,mccabe,language
metrics/metrics.py,21,14,0.67,1,Python
```


Same detailed report but output to csv file:

``` bash
$ metrics -q --format=csv metrics/metrics.py > output.csv
```


# Plugins for metrics

Some plugins are available to collect information from a typical development environment.
Please visit the plugin page for details:

* [version from .bumpversion.cfg](https://github.com/markfink/metrics.bumpversion)
* [Git changes, commiters, ...](https://github.com/markfink/metrics.gitinfo)
* [Pylint lint score](https://github.com/markfink/metrics.pylint)
* [test coverage](https://github.com/markfink/metrics.pytest-cov)


# Acknowledgements

* codebase originally based on grop.py by Jurgen Hermann (2001)
* also based on PyMetrics by Reg. Charney to do Python complexity measurements (2007)
* we use some sample programming language files for the test cases from Ohcount and Firefox


# License

Copyright (c) 2017, 2018 Fink Labs GmbH and others.
metrics is released under the MIT License (see MIT_LICENSE).

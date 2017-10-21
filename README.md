[![License](http://img.shields.io/badge/license-MIT-yellowgreen.svg)](MIT_LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/finklabs/metrics.svg?maxAge=2592000)](https://github.com/finklabs/metrics/issues)


# metrics

The original idea of metrics was a platform that can be extended with many different metrics. At the time I will focus only on SLOC and McCabe complexity metrics but keep its extensibility. *metrics* is build in a way to support many, many languages [supported languages](http://pygments.org/languages/). Currently we test support for C, C++, JavaScript, and Python.

The SLOC metric counts the lines but excludes empty lines and comments. This is sometimes referred to as the *source lines of code* (SLOC). In literature this is often also referred as physical lines of code. I simplified it to something which to my understanding is the common denominator for the metric packages I looked into  (CCCC, SLOCCount, PyMetrics, Eclipse-Metrics, Ohcount). 

Another thing I wanted to mention is that I borrowed the sample programming language files for the test cases from Ohcount and Firefox.


## Sample use

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
  -i INCLUDE_METRICS_STR, --include=INCLUDE_METRICS_STR
                        list of metrics to include in run. This is a comma
                        separated list of metric module names with no
                        whitespace. Optionally, you can specify the class name
                        of the metric by following the module name with a
                        colon (:) and the metric class name. (Default metrics
                        are 'mccabe:McCabeMetric,sloc:SLOCMetric'. Default
                        metric class name for metric module 'wxYz' is
                        'WxYzMetric' when only module name given -- note
                        capitalized metric class name.)
  -l LIB_NAME, --library=LIB_NAME
                        user-defined name applied to collection of modules
                        (Default is '')
  -q, --quiet           suppress normal summary output to stdout. (Default is
                        False)
  --format=OUTPUT_FORMAT_STR
                        Choose an output format for a parser to read. Valid
                        choices: xml, csv
```


Get a detailed report:

``` bash
$ metrics -q --format=csv metrics/metrics.py
filename,mccabe,ratio_comment_to_code,language,comments,sloc
metrics/metrics.py,24,0.39,Python,55,140
```


Same detailed report but output to csv file:

``` bash
$ metrics -q --format=csv metrics/metrics.py > output.csv
```


## License

Copyright (c) 2017 Fink Labs GmbH and others.
metrics is released under the MIT License (see MIT_LICENSE).

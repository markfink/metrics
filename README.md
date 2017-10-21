[![License](http://img.shields.io/badge/license-MIT-yellowgreen.svg)](MIT_LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/finklabs/metrics.svg?maxAge=2592000)](https://github.com/finklabs/metrics/issues)


# metrics

The original idea of metrics was a platform that can be extended with many different metrics. At the time I will focus only on SLOC and McCabe complexity metrics but keep its extensibility. *metrics* is build in a way to support many, many languages [supported languages](http://pygments.org/languages/). Currently we test support for C, C++, JavaScript, and Python.

The SLOC metric counts the lines but excludes empty lines and comments. This is sometimes referred to as the *source lines of code* (SLOC). In literature this is often also referred as physical lines of code. I simplified it to something which to my understanding is the common denominator for the metric packages I looked into  (CCCC, SLOCCount, PyMetrics, Eclipse-Metrics, Ohcount). 

Another thing I wanted to mention is that I borrowed the sample programming language files for the test cases from Ohcount and Firefox.


## Sample use

Get an overview on a package (number of files, used languages, and metrics)

``` bash
$ metrics **/*
Metrics Summary:
Files                       Language        SLOC Comment McCabe 
----- ------------------------------ ----------- ------- ------ 
    6                              C          14       3      0 
    1         JavaScript+Genshi Text           6       7      0 
    2                           Java          27       8      1 
   21                         Python        1082     488    231 
    2                     JavaScript        1447      47    169 
    3                            C++        1114     236    108 
    1                       markdown           5       0      0 
   12                      Text only           0       0      0 
    1                            INI           5       0      0 
----- ------------------------------ ----------- ------- ------ 
   49                          Total        3700     789    509
```

Get a detailed report (pipe to file using > output.csv)

``` bash
$ metrics -q --format=csv metrics/metrics.py
filename,mccabe,ratio_comment_to_code,language,comments,sloc
metrics/metrics.py,24,0.39,Python,55,140
```

Same detailed report but output to csv file)

``` bash
$ metrics -q --format=csv metrics/metrics.py > output.csv
```


## License

Copyright (c) 2017 Fink Labs GmbH and others.
metrics is released under the MIT License (see MIT_LICENSE).

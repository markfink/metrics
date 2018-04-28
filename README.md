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


Sample ".metrics" file results (with plugins installed)

``` json
{
    "build": {
        "active_branch": "master",
        "committed_datetime": "2018-04-28T11:52:37+02:00",
        "committed_ts": 1524909157,
        "committers": [
            "mark"
        ],
        "origin": "git@github.com:markfink/metrics.gitinfo.git",
        "sha": "f7ba6f27ee8c34991acd3cd6ef14c8bd6ed9c34e",
        "sha_start": "7d04ffd8c2acbbfa24977dc6c7b51f34636e34de",
        "summary": "Bump version: 0.0.3 \u2192 0.0.4",
        "version": "0.0.4"
    },
    "files": {
        "metrics_gitinfo/__init__.py": {
            "age_days": 25.80023148148148,
            "block_positions": [],
            "change_frequency": 5,
            "comments": 1,
            "committers_count": 1,
            "language": "Python",
            "lines_added": [
                3
            ],
            "lines_deleted": [
                3
            ],
            "mccabe": 0,
            "pylint_score": 5.0,
            "ratio_comment_to_code": 0.5,
            "sloc": 2
        },
        "metrics_gitinfo/file_info.py": {
            "age_days": 0.0008333333333333334,
            "block_positions": [
                {
                    "end": 17,
                    "name": "get_file_info",
                    "start": 5,
                    "type": "Function"
                }
            ],
            "change_frequency": 1,
            "comments": 4,
            "committers_count": 1,
            "language": "Python",
            "mccabe": 1,
            "pylint_score": 10.0,
            "ratio_comment_to_code": 0.44,
            "sloc": 9
        },
        "metrics_gitinfo/git_diff_muncher.py": {
            "age_days": 24.042083333333334,
            "block_positions": [
                {
                    "end": 17,
                    "name": "GitDiffError",
                    "start": 10,
                    "type": "Class"
                },
                {
                    "end": 81,
                    "name": "parse_diff_lines",
                    "start": 18,
                    "type": "Function"
                },
                {
                    "end": 111,
                    "name": "_parse_hunk_line",
                    "start": 82,
                    "type": "Function"
                }
            ],
            "change_frequency": 1,
            "comments": 50,
            "committers_count": 1,
            "language": "Python",
            "mccabe": 15,
            "pylint_score": 9.56,
            "ratio_comment_to_code": 1.02,
            "sloc": 49
        },
        "metrics_gitinfo/gitinfo.py": {
            "age_days": 25.80023148148148,
            "block_positions": [
                {
                    "end": 17,
                    "name": "get_file_processors",
                    "start": 13,
                    "type": "Function"
                },
                {
                    "end": 22,
                    "name": "get_build_processors",
                    "start": 18,
                    "type": "Function"
                },
                {
                    "end": 113,
                    "methods": [
                        {
                            "end": 35,
                            "name": "_get_commits_contained",
                            "start": 31,
                            "type": "Function"
                        },
                        {
                            "end": 41,
                            "name": "_get_source_target",
                            "start": 36,
                            "type": "Function"
                        },
                        {
                            "end": 56,
                            "name": "_extract_info",
                            "start": 52,
                            "type": "Function"
                        },
                        {
                            "end": 88,
                            "name": "reset",
                            "start": 84,
                            "type": "Function"
                        },
                        {
                            "end": 105,
                            "name": "process_file",
                            "start": 89,
                            "type": "Function"
                        },
                        {
                            "end": 108,
                            "name": "get_metrics",
                            "start": 106,
                            "type": "Function"
                        },
                        {
                            "end": 113,
                            "name": "get_build_metrics",
                            "start": 109,
                            "type": "Function"
                        }
                    ],
                    "name": "GitMetric",
                    "start": 23,
                    "type": "Class"
                }
            ],
            "change_frequency": 6,
            "comments": 9,
            "committers_count": 1,
            "language": "Python",
            "lines_added": [
                88,
                89,
                90,
                91
            ],
            "lines_deleted": [
                10,
                64,
                88,
                89,
                90,
                91,
                92,
                93,
                94,
                95,
                96,
                97,
                98,
                99,
                100
            ],
            "mccabe": 8,
            "pylint_score": 9.06,
            "ratio_comment_to_code": 0.11,
            "sloc": 83
        },
        "tests/__init__.py": {
            "age_days": 24.08150462962963,
            "block_positions": [
                {
                    "end": 10,
                    "name": "here",
                    "start": 9,
                    "type": "Function"
                }
            ],
            "change_frequency": 1,
            "comments": 1,
            "committers_count": 1,
            "language": "Python",
            "mccabe": 0,
            "pylint_score": 3.33,
            "ratio_comment_to_code": 0.17,
            "sloc": 6
        },
        "tests/test_metrics_gitinfo.py": {
            "age_days": 22.07342592592593,
            "block_positions": [
                {
                    "end": 19,
                    "name": "tempfolder",
                    "start": 11,
                    "type": "Function"
                },
                {
                    "end": 29,
                    "name": "test_metrics_gitinfo_no_git_repo",
                    "start": 20,
                    "type": "Function"
                },
                {
                    "end": 39,
                    "name": "test_metrics_gitinfo",
                    "start": 30,
                    "type": "Function"
                },
                {
                    "end": 47,
                    "name": "test_metrics_gitinfo_no_lastrun",
                    "start": 40,
                    "type": "Function"
                }
            ],
            "change_frequency": 1,
            "comments": 2,
            "committers_count": 1,
            "language": "Python",
            "mccabe": 6,
            "pylint_score": 4.64,
            "ratio_comment_to_code": 0.07,
            "sloc": 29
        }
    }
}
```


# Acknowledgements

* codebase originally based on grop.py by Jurgen Hermann (2001)
* also based on PyMetrics by Reg. Charney to do Python complexity measurements (2007)
* we use some sample programming language files for the test cases from Ohcount and Firefox


# License

Copyright (c) 2017, 2018 Fink Labs GmbH and others.
metrics is released under the MIT License (see MIT_LICENSE).

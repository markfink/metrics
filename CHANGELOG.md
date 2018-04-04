# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

### [0.3.0] - 2018-08-08
#### Added
- positions of functions and classes per file for JS, Go, Python, C++
- new JSON output 
- improved plugin mechanism (now manage plugins via pip)
- saves metrics to .metrics file by default (in JSON format)
- load info from last run to context so plugins can use it
#### Changed
- XML output: moved "files" -element and new "build" -element under "metrics" 
#### Removed
- we got rid of the incomplete plugin mechanism and related CLI options

### [0.2.8] - 2017-10-21
#### Added
- Python3 support

### [0.2.0] - 2013-08-12
#### Added
- bug fixes

### [0.1a] - 2010-05-08
#### Added
- initial version


# -*- coding: utf-8 -*-
"""metrics package for source code.

    Originally based on grop.py by Jurgen Hermann.
    PyMetrics by Reg. Charney to do Python complexity measurements.
    Simplified and reduced functionality by Mark Fink

    Copyright (c) 2017 by Fink Labs GmbH
    Copyright (c) 2010 by Mark Fink
    Copyright (c) 2007 by Reg. Charney <charney@charneyday.com>
    Copyright (c) 2001 by Jurgen Hermann <jh@web.de>

    All rights reserved, see LICENSE for details.
"""
from __future__ import unicode_literals, print_function
import sys
import os

from .processargs import ProcessArgs, ProcessArgsError
from .metrics_utils import process, format


PYTHON_VERSION = sys.version[:3]


def main():
    try:
        pa = ProcessArgs()
        context = {}
        context['root_dir'] = os.getcwd()
        context['in_file_names'] = pa.in_file_names
        context['quiet'] = pa.quiet
        context['verbose'] = pa.verbose
        context['output_format'] = pa.output_format_str
        metrics = process(context)

        if context['output_format'] is not None:
            print(format(metrics, context['output_format']))
    except ProcessArgsError as e:
        sys.stderr.writelines(str(e))
    sys.exit(0)

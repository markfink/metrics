# -*- coding: utf-8 -*-
"""metrics package for source code.

    Originally based on grop.py by Jurgen Hermann.
    PyMetrics by Reg. Charney to do Python complexity measurements.
    Simplified and reduced functionality by Mark Fink

    Copyright (c) 2018 by Mark Fink
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
from .metrics_utils import process_file_metrics, process_build_metrics, summary, \
    format, load_metrics_from_file
from .sloc import SLOCMetric
from .mccabe import McCabeMetric
from .position import PosMetric
from .plugins import load_plugins
from . import METRICS_FILENAME


def main():
    try:
        pa = ProcessArgs()
        context = {}
        context['root_dir'] = os.getcwd()
        context['in_file_names'] = pa.in_file_names
        context['quiet'] = pa.quiet
        context['verbose'] = pa.verbose
        context['output_format'] = pa.output_format_str
        context['last_metrics'] = load_metrics_from_file(METRICS_FILENAME)

        file_processors, build_processors = load_plugins()
        file_processors = \
            [SLOCMetric(context), McCabeMetric(context), PosMetric(context)] + \
            [p(context) for p in file_processors]
        build_processors = [p(context) for p in build_processors]

        file_metrics = process_file_metrics(context, file_processors)
        # build_metrics are not exactly metrics but hopefully useful
        build_metrics = process_build_metrics(context, build_processors)

        if not context['quiet']:
            summary(file_processors, file_metrics, context)

        if context['output_format'] is not None:
            print(format(file_metrics, build_metrics, context['output_format']))

        # save to .metrics file
        with open(METRICS_FILENAME, 'w') as ofile:
            ofile.write(format(file_metrics, build_metrics, 'json'))
    except ProcessArgsError as e:
        sys.stderr.writelines(str(e))
    sys.exit(0)

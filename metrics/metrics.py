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
from collections import OrderedDict

from pygments.lexers import guess_lexer_for_filename

from .processargs import ProcessArgs, ProcessArgsError
from .compute import ComputeMetrics
from .metrics_utils import glob_files

PYTHON_VERSION = sys.version[:3]


def __import_output_formatter(output_format):
    """Import the output formatter module that matches the output_format
    specified in the parameter.

    output_format is a string specifying the output format writer to import.
    If an Import error occurs, the program will fails.
    """
    try:
        filename = "outputformat_" + output_format
        mod = __import_module(filename, filename)
    except ImportError:
        # should not happen as we already specified valid output format module
        # in the options.
        sys.stderr.write(
            "Unable to import output format module %s --" % output_format +
            "ignored.\n\n")
        # won't be catched.
        raise

    return mod


def __import_metric_modules(include_metrics):
    """Import the modules specified in the parameter list.

    includeMetrics is a list of (metricModuleName, metricClassName)
    pairs. This function defines a dictionary containing only valid
    module/class names. When an error is found, the invalid
    module/class pair is removed from the included list of metrics.
    """
    i = 0
    metric_modules = OrderedDict()
    for metric_name, _ in include_metrics:
        try:
            mod = __import_module(metric_name, metric_name)
            metric_modules[metric_name] = mod
            i += 1
        except ImportError:
            sys.stderr.write(
                "Unable to import metric module %s -- ignored.\n\n" % metric_name)
            # remove the erroneous metric module/class tuple
            del include_metrics[i]


    return metric_modules


def __import_module(module_name, filename):
    """Import a module from the metrics package, taking care of the Python
    version. Raises ImportError on failure."""

    if PYTHON_VERSION < '2.5':
        # fix for python2.4
        mod = __import__(module_name, globals(), locals(), [filename])
    else:
        mod = __import__('metrics.' + module_name, fromlist=[filename])

    return mod


def __instantiate_metric(metric_modules, context):
    """Instantiate all user specified metric classes.

    The code works by finding the desired metric class in a metric module and
    instantiating the class. It does this by assuming that the metric
    class is in the dictionary of the metric module.
    """
    metric_instance = {}
    incl_indx = -1
    for m, n in context['include_metrics']:
        incl_indx += 1
        try:
            metric_instance[m] = None  # default if metric class does not exist.
            metric_instance[m] = metric_modules[m].__dict__[n](context)
        except KeyError:
            sys.stderr.write('Module %s does not contain metric class %s' % (m, n) +
                ' -- metric %s ignored.\n\n' % m)
            del(metric_instance[m])
            del(context['include_metrics'][incl_indx])

    return metric_instance


def main():
    try:
        pa = ProcessArgs()
        context = {}
        context['root_dir'] = os.getcwd()
        context['in_file_names'] = pa.in_file_names
        context['include_metrics'] = pa.include_metrics
        context['quiet'] = pa.quiet
        context['verbose'] = pa.verbose
        context['output_format'] = pa.output_format_str
        metrics = process(context)

        if context['output_format'] is not None:
            print(format(metrics, context['output_format']))
    except ProcessArgsError as e:
        sys.stderr.writelines(str(e))
    sys.exit(0)


def format(metrics, format):
    formatter = __import_output_formatter(format.lower())
    return formatter.format(metrics)


def process(context):
    """Main routine for metrics."""
    metrics = OrderedDict()

    # import all the needed metric modules
    metric_modules = __import_metric_modules(context['include_metrics'])

    # instantiate all the desired metric classes
    metric_instance = __instantiate_metric(metric_modules, context)

    cm = ComputeMetrics(metric_instance, context)

    # TODO make available the includes and excludes feature
    in_files = glob_files(context['root_dir'], context['in_file_names'])
    # main loop
    for in_file, key in in_files:
        # print 'file %i: %s' % (i, in_file)
        try:
            cm.reset()
            with open(in_file, 'rb') as ifile:
                code = ifile.read()
            # lookup lexographical scanner to use for this run
            try:
                lex = guess_lexer_for_filename(in_file, code, encoding='guess')
                # encoding is 'guess', chardet', 'utf-8'
            except:
                pass
            else:
                token_list = lex.get_tokens(code)  # parse code

                metrics[key] = OrderedDict()
                metrics[key].update(cm(token_list))
                metrics[key]['language'] = lex.name

        except IOError as e:
            sys.stderr.writelines(str(e) + " -- Skipping input file.\n\n")

    if not context['quiet']:
        summary(metric_instance, metrics, context)

    return metrics


def summary(metric_instance, metrics, context):
    """Print the summary"""
    # display agregated metric values on language level
    def display_header(context, metric_instance, before='', after=''):
        """Display the header for the summary results."""
        print(before, end=' ')
        for m, n in context['include_metrics']: # display in the order of apperance
            metric_instance[m].display_header()
        print(after)

    def display_separator(context, metric_instance, before='', after=''):
        """Display the header for the summary results."""
        print(before, end=' ')
        for m, n in context['include_metrics']:
            metric_instance[m].display_separator()
        print(after)

    def display_metrics(context, metric_instance, before='', after='', metrics=[]):
        """Display the header for the summary results."""
        print(before, end=' ')
        for m, n in context['include_metrics']:
            metric_instance[m].display_metrics(metrics)
        print(after)

    summary = {}
    for m in metrics:
        lang = metrics[m]['language']
        has_key = lang in summary
        if not has_key:
            summary[lang] = {'file_count': 0, 'language': lang}
        summary[lang]['file_count'] += 1
        for i in metrics[m]:
            if i == 'language':
                continue
            if not has_key:
                summary[lang][i] = 0
            summary[lang][i] += metrics[m][i]

    total = {'language': 'Total'}
    for m in summary:
        for i in summary[m]:
            if i == 'language':
                continue
            if i not in total:
                total[i] = 0
            total[i] += summary[m][i]

    print('Metrics Summary:')

    display_header(context, metric_instance, 'Files', '')
    display_separator(context, metric_instance, '-'*5, '')
    for k in sorted(summary.keys(), key=str.lower):
        display_metrics(context, metric_instance, '%5d' % 
            summary[k]['file_count'], '', summary[k])
    display_separator(context, metric_instance, '-'*5, '')
    display_metrics(context, metric_instance, '%5d' % total['file_count'],
        '', total)

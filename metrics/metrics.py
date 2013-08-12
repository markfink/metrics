#! /usr/bin/env python
"""metrics package for source code.

    Orignally based on grop.py by Jurgen Hermann.
    PyMetrics by Reg. Charney to do Python complexity measurements.
    Simplified and reduced functionality by Mark Fink

    Copyright (c) 2001 by Jurgen Hermann <jh@web.de>
    Copyright (c) 2007 by Reg. Charney <charney@charneyday.com>
    Copyright (c) 2010 by Mark Fink <mark@mark-fink.de>

    All rights reserved, see LICENSE for details.
"""

import sys
import os
from pygments.lexers import guess_lexer_for_filename
from processargs import ProcessArgs, ProcessArgsError
from compute import ComputeMetrics

PYTHON_VERSION = sys.version[:3]


def __import_output_formatter(output_format):
    """Import the output formatter module that matches the output_format
    specified in the parameter.

    output_format is a string specifying the output format writer to import.
    If an Import error occurs, the program will fails.
    """
    try:
        filename = "outputformat" + output_format
        mod = __import_module(filename, filename)
    except ImportError:
        # should not happen as we already specified valid output format module
        # in the options.
        sys.stderr.write("Unable to import output format module %s --"\
                "ignored.\n\n" % output_format)
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
    metric_modules = {}
    for metric_name, _ in include_metrics:
        try:
            mod = __import_module(metric_name, metric_name)
            metric_modules[metric_name] = mod
            i += 1
        except ImportError:
            sys.stderr.write(
                "Unable to import metric module %s -- ignored.\n\n" % mm)
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
    inclIndx = -1
    for m, n in context['include_metrics']:
        inclIndx += 1
        try:
            metric_instance[m] = None # default if metric class does not exist.
            metric_instance[m] = metric_modules[m].__dict__[n](context)
        except KeyError:
            sys.stderr.write('Module %s does not contain metric class %s' + \
                ' -- metric %s ignored.\n\n' % (m, n, m))
            del(metric_instance[m])
            del(context['include_metrics'][inclIndx])

    return metric_instance


def main():
    try:
        pa = ProcessArgs()
        context = {}
        context['base'] = ''
        context['in_file_names'] = pa.in_file_names
        context['include_metrics'] = pa.include_metrics
        context['quiet'] = pa.quiet
        context['verbose'] = pa.verbose
        context['output_format'] = pa.output_format_str
        metrics = process(context)

        if context['output_format'] is not None:
            print format(metrics, context['output_format'])

    except ProcessArgsError, e:
        sys.stderr.writelines(str(e))
    sys.exit(0)


def format(metrics, format):
    formatter = __import_output_formatter(format.upper())
    return formatter.format(metrics)


def process(context):
    """Main routine for metrics."""
    metrics = {}

    # import all the needed metric modules
    metric_modules = __import_metric_modules(context['include_metrics'])

    # instantiate all the desired metric classes
    metric_instance = __instantiate_metric(metric_modules, context)

    cm = ComputeMetrics(metric_instance, context)

    # main loop
    for i, in_file in enumerate(context['in_file_names']):
        # print 'file %i: %s' % (i, in_file)
        try:
            cm.reset()
            fin = open(os.path.join(context['base'], in_file), 'r')
            code = ''.join(fin.readlines())
            fin.close()
            # define lexographical scanner to use for this run
            try:
                lex = guess_lexer_for_filename(in_file, code, encoding='guess')
                # encoding is 'guess', chardet', 'utf-8'
            except:
                pass
            else:
                token_list = lex.get_tokens(code) # parse code

                metrics[in_file] = {}
                metrics[in_file].update(cm(token_list))
                metrics[in_file]['language'] = lex.name # provide language

        except IOError, e:
            sys.stderr.writelines(str(e) + " -- Skipping input file.\n\n")

    if not context['quiet']:
        summary(metric_instance, metrics, context)

    return metrics


def summary(metric_instance, metrics, context):
    """Print the summary"""
    # display agregated metric values on language level
    def display_header(context, metric_instance, before='', after=''):
        """Display the header for the summary results."""
        print before,
        for m, n in context['include_metrics']: # display in the order of apperance
            metric_instance[m].display_header()
        print after


    def display_separator(context, metric_instance, before='', after=''):
        """Display the header for the summary results."""
        print before,
        for m, n in context['include_metrics']:
            metric_instance[m].display_separator()
        print after


    def display_metrics(context, metric_instance, before='', after='', metrics=[]):
        """Display the header for the summary results."""
        print before,
        for m, n in context['include_metrics']:
            metric_instance[m].display_metrics(metrics)
        print after

    summary = {}
    for m in metrics:
        lang = metrics[m]['language']
        has_key = summary.has_key(lang)
        if not has_key:
            summary[lang] = {'file_count': 0, 'language': lang}
        summary[lang]['file_count'] += 1
        for i in metrics[m]:
            if i == 'language':
                continue
            if not has_key:
                summary[lang][i] = 0
            summary[lang][i] += metrics[m][i]

    total ={'language': 'Total'}
    for m in summary:
        for i in summary[m]:
            if i == 'language':
                continue
            if not total.has_key(i):
                total[i] = 0
            total[i] += summary[m][i]

    print 'Metrics Summary:'

    display_header(context, metric_instance, 'Files', '')
    display_separator(context, metric_instance, '-'*5, '')
    for m in summary:
        display_metrics(context, metric_instance, '%5d' % 
            summary[m]['file_count'], '', summary[m])
    display_separator(context, metric_instance, '-'*5, '')
    display_metrics(context, metric_instance, '%5d' % total['file_count'],
        '', total)


if __name__ == "__main__":
    # process command line args
    main()

"""
Metrics - A Tool For Calculating SLOC

Orignally based on grop.py by Jurgen Hermann.
PyMetrics by Reg. Charney to do Python complexity measurements.
Simplified and reduced functionality by Mark Fink.
Ported to Python 3 and made more Pythonic by Ted Moseley.

Copyright (c) 2001 by Jurgen Hermann <jh@web.de>
Copyright (c) 2007 by Reg. Charney <charney@charneyday.com>
Copyright (c) 2010 by Mark Fink <mark@mark-fink.de>

All rights reserved, see LICENSE.txt for details.
"""

# Standard
import collections
import functools
import importlib
import inspect
import sys
# Dependency
import click
import pygments
import pygments.lexers
# Project
import metrics
from metrics import compute, output_formats


def _read_includes_string(metrics_string):
    """
    """
    included_metrics = collections.OrderedDict()

    try:
        for metric_module in metrics_string.split(','):
            # Split the module class from the package
            metric_module_name, metric_class_name = metric_module.split(':')
            if metric_module_name not in included_metrics:
                included_metrics[metric_module_name] = []
            included_metrics[metric_module_name].append(metric_class_name)
    except AttributeError:
        error_string = "Invalid list of metric names: {}".format(metrics_string)
        click.echo(error_string, err=True)

    return included_metrics


def _import_metric_modules(metric_name_dict):
    """
    Import the modules specified in the includes string.

    includeMetrics is a list of (metricModuleName, metricClassName)
    pairs. This function defines a dictionary containing only valid
    module/class names. When an error is found, the invalid
    module/class pair is removed from the included list of metrics.
    """
    imported_metrics = collections.OrderedDict()
    for metric_name in metric_name_dict:
        try:
            imported_metrics[metric_name] = importlib.import_module(metric_name)
        except ImportError:
            error_string = "Unable to import metric \'{}\'. Ignored.\n\n"
            click.echo(error_string.format(metric_name), err=True)

    return imported_metrics


def _instantiate_metrics(metric_name_dict, metric_modules_dict, context):
    """
    Instantiate all user specified metric classes.

    The code works by finding the desired metric class in a metric module and
    instantiating the class. It does this by assuming that the metric
    class is in the dictionary of the metric module.
    """
    metric_instances = {}

    for metric_module_name in metric_name_dict:
        # Get the name of the class we want
        for metric_class_name in metric_name_dict[metric_module_name]:
            try:
                # Get the module that holds the class we want
                metric_module = metric_modules_dict[metric_module_name]
                # Get a list of classes within the module we found above
                metric_module_classes = dict(inspect.getmembers(metric_module,
                                                                inspect.isclass))
                # Get the class we want
                metric_class = metric_module_classes[metric_class_name]
                metric_instances[metric_class.name] = metric_class(context)
            except KeyError:
                error_string = "Module \'{}\' does not contain metric class\' {}\'. Ignored."
                click.echo(error_string.format(metric_module_name,
                                               metric_class_name),
                           err=True)

    return metric_instances


STOCK_METRICS = (
    "metrics.stock_metrics:SLOCMetric",
    "metrics.stock_metrics:CommentMetric",
    "metrics.stock_metrics:McCabeMetric"
)


@click.command()
@click.option("--format", "output_format",
              type=click.Choice(["csv", "json", "table", "xml"]),
              default="table",
              help="Choose a format to output")
@click.option("--type", "output_type",
              type=click.Choice(["file", "language"]),
              default="file",
              help="Choose a table type to output")
@click.option("--include",
              default=','.join(STOCK_METRICS),
              help="Comma separate list of metrics to run")
@click.option("--verbose", is_flag=True,
              help="Increase verbosity of output")
@click.version_option(metrics.__version__)
@click.argument("filenames", nargs=-1)
def main(filenames, output_format, output_type, include, verbose):
    """
    A Tool For Calculating SLOC and More
    """

    context = {
        'in_files': filenames,
        'include_metrics': _read_includes_string(include),
        'verbose': verbose,
        'output_format': output_format,
        'output_type': output_type
    }

    # Check if any files were input as arguments
    if not context['in_files']:
        click.echo("No file arguments given!", err=True)
        sys.exit(0)

    # Import all the needed metric modules
    metric_modules = _import_metric_modules(context['include_metrics'])

    # Instantiate all the desired metric classes
    metric_instances = _instantiate_metrics(context['include_metrics'],
                                            metric_modules,
                                            context)
    # Instantiate the processor for metrics
    processor = compute.ResultProcessor(metric_instances, context)

    for a_string in filenames:
        a_file = a_string
        try:
            processor.process_file(a_file)
        except IsADirectoryError:
            warning_string = "The path \'{}\' is a directory. Skipped."
            if verbose:
                click.echo(warning_string.format(a_file), err=True)
            continue
        except UnicodeDecodeError:
            error_string = "The file \'{}\' couldn't be decoded. Skipped."
            if verbose:
                click.echo(error_string.format(a_file), err=True)
            continue
        except pygments.util.ClassNotFound:
            warning_string = "The file \'{}\' does not have a lexer. Skipped."
            if verbose:
                click.echo(warning_string.format(a_file), err=True)
            continue

    if output_type == "file":
        metric_dict = processor.get_file_results()
    elif output_type == "language":
        metric_dict = processor.get_language_results()

    if output_format == "table":
        formatter = output_formats.format_table
        click.echo("\nMetrics Summary:\n")
    elif output_format == "csv":
        formatter = output_formats.format_csv
    elif output_format == "json":
        formatter = output_formats.format_json
    elif output_format == "xml":
        if output_type == "file":
            config = {
                'item_offset': 2,
                'item_name': "file",
                'item_attrs': {
                    'name': 0,
                    'language': 1,
                },
                'root_name': "files",
            }
        elif output_type == "language":
            config = {
                'item_offset': 1,
                'item_name': "language",
                'item_attrs': {
                    'name': 0,
                },
                'root_name': "languages",
            }

        formatter = functools.partial(output_formats.format_xml, config)

    output_string = formatter(metric_dict)

    click.echo(output_string)

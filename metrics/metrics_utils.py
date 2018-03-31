# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import logging
from collections import OrderedDict

import pathspec
from pathlib2 import PurePath, Path
from pygments.lexers import guess_lexer_for_filename

from .compute import compute_metrics
from .sloc import SLOCMetric
from .mccabe import McCabeMetric
from . import outputformat_csv
from . import outputformat_xml


PYTHON_VERSION = sys.version[:3]
log = logging.getLogger(__name__)


# based on: https://github.com/finklabs/botodeploy/blob/master/botodeploy/utils_static.py
def glob_files(root_dir, includes=None, excludes=None, gitignore=None):
    """Powerful and flexible utility to search and tag files using patterns.
    :param root_dir: directory where we start the search
    :param includes: list or iterator of include pattern tuples (pattern, tag)
    :param excludes: list or iterator of exclude patterns
    :param gitignore: list of ignore patterns (gitwildcard format)
    :return: iterator of (absolute_path, relative_path)
    """
    # docu here: https://docs.python.org/3/library/pathlib.html
    if not includes:
        includes = ['**']
    else:
        # we need to iterate multiple times (iterator safeguard)
        includes = list(includes)

    if excludes:
        # we need to iterate multiple times (iterator safeguard)
        excludes = list(excludes)

    if gitignore:
        spec = pathspec.PathSpec.from_lines('gitwildmatch', gitignore)
        log.debug('gitignore patterns: %s', gitignore)

    while includes:
        pattern = includes.pop(0)
        # for compatibility with std. python Lib/glop.py:
        # >>>If recursive is true, the pattern '**' will match any files and
        #    zero or more directories and subdirectories.<<<
        if pattern.endswith('**'):
            pattern += '/*'
        matches = list(Path(root_dir).glob(pattern))

        for m in matches:
            if m.is_dir():
                continue

            # some discussion on how to convert a pattern into regex:
            # http://stackoverflow.com/questions/27726545/python-glob-but-against-a-list-of-strings-rather-than-the-filesystem
            pp = PurePath(m)

            # check if m is contained in remaining include patterns
            # (last one wins)
            if includes and any(map(lambda p: pp.match(p), includes)):
                continue

            # check if m is contained in exclude pattern
            if excludes and any(map(lambda p: pp.match(p), excludes)):
                continue

            # check if m is contained in finkignore
            if gitignore and spec.match_file(str(m)):
                log.debug('Skipped file \'%s\' due to gitignore pattern',
                          str(m.relative_to(root_dir)))
                continue

            yield (str(m), str(m.relative_to(root_dir)))


def format(metrics, format):
    if format.lower() == 'xml':
        formatter = outputformat_xml
    elif format.lower() == 'csv':
        formatter = outputformat_csv
    else:
        raise ValueError('unknown format: %s', format)

    return formatter.format(metrics)


def process(context):
    """Main routine for metrics."""
    metrics = OrderedDict()
    processors = [SLOCMetric(context), McCabeMetric(context)]

    # TODO make available the includes and excludes feature
    in_files = glob_files(context['root_dir'], context['in_file_names'])
    # main loop
    for in_file, key in in_files:
        # print 'file %i: %s' % (i, in_file)
        try:
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
                metrics[key].update(compute_metrics(processors, token_list))
                metrics[key]['language'] = lex.name

        except IOError as e:
            sys.stderr.writelines(str(e) + " -- Skipping input file.\n\n")

    if not context['quiet']:
        summary(processors, metrics, context)

    return metrics


def summary(processors, metrics, context):
    """Print the summary"""
    # display aggregated metric values on language level
    def display_header(processor, before='', after=''):
        """Display the header for the summary results."""
        print(before, end=' ')
        for processor in processors:
            processor.display_header()
        print(after)

    def display_separator(processor, before='', after=''):
        """Display the header for the summary results."""
        print(before, end=' ')
        for processor in processors:
            processor.display_separator()
        print(after)

    def display_metrics(processor, before='', after='', metrics=[]):
        """Display the header for the summary results."""
        print(before, end=' ')
        for processor in processors:
            processor.display_metrics(metrics)
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

    display_header(processors, 'Files', '')
    display_separator(processors, '-'*5, '')
    for k in sorted(summary.keys(), key=str.lower):
        display_metrics(processors, '%5d' %
                        summary[k]['file_count'], '', summary[k])
    display_separator(processors, '-'*5, '')
    display_metrics(processors, '%5d' % total['file_count'],
                    '', total)

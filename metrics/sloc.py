# -*- coding: utf-8 -*-
"""Source Lines of Code (SLOC)
    This type of metric counts the lines but excludes empty lines and comments.
    In literature this is also referred as physical lines of code.
"""
from __future__ import unicode_literals, print_function
from collections import OrderedDict

from .metricbase import MetricBase


token_types = [
    'Keyword',
    'Name',
    'Punctuation',
    'Operator',
    'Literal']


class SLOCMetric(MetricBase):
    """Compute the SLOC Metric for the whole source file."""

    def __init__(self, context):
        self.name = 'sloc'
        self.context = context
        self.reset()

    def reset(self):
        """Reset metric counter."""
        self.sloc = 0
        self.comments = 0
        self.contains_code = False  # does the current line contain code

    def process_token(self, tok):
        """count comments and non-empty lines that contain code"""
        if(tok[0].__str__() in ('Token.Comment.Multiline', 'Token.Comment',
                'Token.Literal.String.Doc')):
            self.comments += tok[1].count('\n')+1
        elif(tok[0].__str__() in ('Token.Comment.Single')):
            self.comments += 1
        elif(self.contains_code and tok[0].__str__().startswith('Token.Text')
                and tok[1].count(u'\n')):
            # start new line
            self.contains_code = False
            self.sloc += 1
        # for c style includes
        elif(tok[0].__str__() == 'Token.Comment.Preproc' and
                tok[1].count(u'\n')):
            # start new line
            self.contains_code = False
            self.sloc += 1
        elif(tok[0][0] in token_types):
            self.contains_code = True

    def display_header(self):
        """Display header for SLOC metric"""
        print('%30s %11s %7s' % ('Language', 'SLOC', 'Comment'), end=' ')

    def display_separator(self):
        """Display separator for SLOC metric"""
        print('%s %s %s' % ('-'*30, '-'*11, '-'*7), end=' ')

    def display_metrics(self, metrics):
        """Display Source Lines of Code metric (SLOC) """
        print('%30s %11d %7d' % (metrics['language'], metrics['sloc'],
            metrics['comments']), end=' ')

    def get_metrics(self):
        """Calculate ratio_comment_to_code and return with the other values"""
        if(self.sloc == 0):
            if(self.comments == 0):
                ratio_comment_to_code = 0.00
            else:
                ratio_comment_to_code = 1.00
        else:
            ratio_comment_to_code = float(self.comments) / self.sloc
        metrics = OrderedDict([('sloc', self.sloc), ('comments', self.comments),
                               ('ratio_comment_to_code', round(ratio_comment_to_code, 2))])
        return metrics

    metrics = property(get_metrics)

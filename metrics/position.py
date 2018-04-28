# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys

from pygments.token import Token

from .metricbase import MetricBase


# pygments does not provide the scope detection we need out of the box
# so we have to code some specifics
class BaseDetector:
    def __init__(self, metric):
        self.metric = metric

    def process(self, tok):
        return False


class PythonDetector(BaseDetector):
    """detector for Python"""
    def process(self, tok):
        if tok[0] != Token.Text:
            pass
        elif tok[1].count('\n'):
            self.metric._scope = 0
        elif tok[1] == '    ':
            self.metric._scope = 1
        elif tok[1] == '        ':
            self.metric._scope = 2
        elif not tok[1].startswith(' '):
            if self.metric._curr is not None:
                self.metric._curr['end'] = self.metric._line - 1 # close last scope
                self.metric._curr = None
        return False


class JavascriptDetector(BaseDetector):
    """detector for Javascript"""
    def process(self, tok):
        if tok[0] == Token.Keyword.Reserved and self.metric._scope == 0 and \
                        tok[1] == 'class':
            self.found_javascript_class = True
        elif tok[0] == Token.Name.Other and self.found_javascript_class:
            self.metric.add_scope('Class', tok[1], self.metric._line)
            self.found_javascript_class = False
        return False


class GoDetector(BaseDetector):
    """detector for go"""
    def __init__(self, metric):
        super(GoDetector, self).__init__(metric)
        self.reset()

    def reset(self):
        self._declaration = None
        self._name = None
        self._start = None

    def process(self, tok):
        # see test for samples on Interface, Struct, and Function
        if tok[0] == Token.Keyword.Declaration and tok[1] in ['type', 'func']:
            self._declaration = tok[1]
            self._start = self.metric._line
            self._name = None
        elif tok[0] == Token.Keyword.Declaration and tok[1] in \
                ['interface', 'struct'] and self._declaration and self._name:
            self.metric.add_scope(tok[1].capitalize(), self._name, self._start)
            self.reset()
        elif tok[0] == Token.Name.Other:
            self._name = tok[1]  # we are looking for the last Token.Name.Other
        elif tok[0] == Token.Punctuation and tok[1] == '(' and self._start and \
                self._name:
            self.metric.add_scope('Function', self._name, self._start)
            self.reset()
        return False


class PosMetric(MetricBase):
    """Compute the position of functions and methods for the whole source file."""
    def __init__(self, context):
        self.name = 'sloc'
        self._context = context
        self.reset()

    def reset(self):
        """Reset metric counter."""
        self._positions = []
        self._line = 1
        self._curr = None  # current scope we are analyzing
        self._scope = 0
        self.language = None

    def add_scope(self, scope_type, scope_name, scope_start, is_method=False):
        """we identified a scope and add it to positions."""
        if self._curr is not None:
            self._curr['end'] = scope_start - 1  # close last scope
        self._curr = {
            'type': scope_type, 'name': scope_name,
            'start': scope_start, 'end': scope_start
        }

        if is_method and self._positions:
            last = self._positions[-1]
            if not 'methods' in last:
                last['methods'] = []
            last['methods'].append(self._curr)
        else:
            self._positions.append(self._curr)

    def process_token(self, tok):
        """count lines and track position of classes and functions"""
        if tok[0] == Token.Text:
            count = tok[1].count('\n')
            if count:
                self._line += count  # adjust linecount

        if self._detector.process(tok):
            pass  # works been completed in the detector
        elif tok[0] == Token.Punctuation:
            if tok[0] == Token.Punctuation and tok[1] == '{':
                self._scope += 1
            if tok[0] == Token.Punctuation and tok[1] == '}':
                self._scope += -1
                if self._scope == 0 and self._curr is not None:
                    self._curr['end'] = self._line  # close last scope
                    self._curr = None
        elif tok[0] == Token.Name.Class and self._scope == 0:
            self.add_scope('Class', tok[1], self._line)
        elif tok[0] == Token.Name.Function and self._scope in [0, 1]:
            self.add_scope('Function', tok[1], self._line, self._scope == 1)

    def get_metrics(self):
        if self._curr is not None:
            self._curr['end'] = self._line -1
        for p in self._positions:
            if 'methods' in p:
                for m in p['methods']:
                    if m['end'] > p['end']:
                        p['end'] = m['end']
        return {'block_positions': self._positions}

    metrics = property(get_metrics)

    def get_language(self):
        return self._language

    def set_language(self, value):
        self._language = value
        detector = getattr(sys.modules[__name__], '%sDetector' % value, None)
        if detector:
            self._detector = detector(self)
        else:
            self._detector = BaseDetector(self)

    language = property(get_language, set_language)

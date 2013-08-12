"""Compute McCabe's Cyclomatic Metric.

    This routine computes McCabe's Cyclomatic metric for the whole file.

"""

from metricbase import MetricBase

mccabe_keywords = [
    'assert',
    'break',
    'continue',
    'elif',
    'else',
    'for',
    'if',
    'while']


class McCabeMetric(MetricBase):
    """Compute McCabe's Cyclomatic Metric for the whole source file."""

    def __init__(self, context):
        self.name = 'mccabe'
        self.context = context
        self.reset()

    def reset(self):
        """Reset metric counter."""
        self.metrics = {'mccabe': 0}

    def process_token(self, tok):
        """Increment number of decision points in function."""
        #if tok and tok.text in mccabe_keywords:
        if (tok[0][0] == 'Keyword') and tok[1] in mccabe_keywords:
            self.metrics['mccabe'] += 1

    def display_header(self):
        """Display header for McCabe Cyclomatic Complexity """
        print 'McCabe',

    def display_separator(self):
        """Display separator for McCabe Cyclomatic Complexity """
        print '------',

    def display_metrics(self, metrics):
        """Display McCabe Cyclomatic Complexity """
        print '%6d' % metrics['mccabe'],

    def get_metrics(self):
        return self.metrics


"""
metric_base.py

A Metric base class for simplifying the process of creating new
user-defined metrics.

All rights reserved, see LICENSE.txt for details.
"""


class MetricBase(object):
    """
    This is a base class for a metric counter. Each metric needs at
    least one attributes:

        * 'name' which is a string that gives the metric instance a
          name to go by.
    """

    _count = 0

    def __init__(self, context):
        """
        """
        pass

    def reset(self):
        """ Reset the counters to zero. """
        self._count = 0

    def process_token(self, token):
        """ Take in a single token named tuple and process it. """
        pass

    def get_metrics(self):
        """
        Return a dictionary of the results calculated by process_token
        up to this point by the instance.
        """
        return self._count

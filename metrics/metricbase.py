# -*- coding: utf-8 -*-
"""Metric base class for new user-defined metrics."""
from __future__ import unicode_literals


class MetricBase(object):
    """Metric template class."""
    _language = None

    def __init__( self, *args, **kwds ):
        pass

    def process_token(self, token):
        """Handle processing for each token."""
        pass

    def display_header(self):
        """Display the metric header for the processed file."""
        pass

    def display_metrics(self, metrics):
        """Display the metric for the processed file."""
        pass

    def display_separator(self):
        """Display the metric separator for the processed file."""
        pass

    def get_metrics(self):
        """Return the current metrics as a dict"""
        pass

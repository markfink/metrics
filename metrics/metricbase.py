# -*- coding: utf-8 -*-
"""Metric base class for new user-defined metrics."""
from __future__ import unicode_literals


class MetricBase(object):
    """Metric template class."""
    _language = None
    _metrics = None

    def __init__(self, *args, **kwds ):
        pass

    def reset(self):
        """
        Reset the processor.

        Implement this in case you need to reset the processor for each key.
        """
        pass

    def process_token(self, token):
        """Handle processing for each token."""
        pass

    def process_file(self, language, key, token_list):
        """
        Initiate processing for each token.

        Override this if you want tt control the processing of the tokens yourself.
        """
        self.language = language
        for tok in token_list:
            self.process_token(tok)

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
        pass

"""Metric base class for new user-defined metrics."""

class MetricBase(object):
    """Metric template class."""
    def __init__( self, *args, **kwds ):
        pass

    def process_token(self, token):
        """Handle processing for each token."""
        pass

    def display(self):
        """Display the metric for the processed file."""
        pass

    def get_metrics(self):
        """Return the current metrics as a dict"""
        pass


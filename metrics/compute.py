# -*- coding: utf-8 -*-
"""Main computational modules for metrics."""
from __future__ import unicode_literals
from collections import OrderedDict


def compute_metrics(processors, token_list):
    """use processors to compute the various metrics.
    """
    metrics = OrderedDict()

    # reset all processors
    for p in processors:
        p.reset()

    # process all tokens
    for tok in token_list:
        for p in processors:
            p.process_token(tok)

    # collect metrics from all processors
    for p in processors:
        metrics.update(p.metrics)

    return metrics

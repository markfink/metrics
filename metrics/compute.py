# -*- coding: utf-8 -*-
"""Main computational modules for metrics."""
from __future__ import unicode_literals
import itertools
from collections import OrderedDict


def compute_file_metrics(processors, language, key, token_list):
    """use processors to compute file metrics."""
    # multiply iterator
    tli = itertools.tee(token_list, len(processors))
    metrics = OrderedDict()

    # reset all processors
    for p in processors:
        p.reset()

    # process all tokens
    for p, tl in zip(processors, tli):
        p.process_file(language, key, tl)

    # collect metrics from all processors
    for p in processors:
        metrics.update(p.metrics)

    return metrics

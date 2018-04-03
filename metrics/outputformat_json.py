# -*- coding: utf-8 -*-
"""output in JSON format.
    All rights reserved, see LICENSE for details.
"""
from __future__ import unicode_literals
import json


def format(file_metrics, build_metrics):
    """compute output in JSON format."""
    metrics = {'files': file_metrics}
    if build_metrics:
        metrics['build'] = build_metrics
    body = json.dumps(metrics, sort_keys=True, indent=4) + '\n'
    return body
# -*- coding: utf-8 -*-
"""output in JSON format.
    All rights reserved, see LICENSE for details.
"""
from __future__ import unicode_literals
import sys
import json


PY3 = sys.version_info[0] >= 3


def format(metrics):
    """compute output in XML format."""
    body = json.dumps(metrics, sort_keys=True, indent=4) + '\n'
    return body
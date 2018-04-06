# -*- coding: utf-8 -*-
"""output in XML format.

    initial version 2010 by djcoin (https://bitbucket.org/djcoin)
    All rights reserved, see LICENSE for details.
"""
from __future__ import unicode_literals
import sys

import xml.etree.ElementTree as ET


PY3 = sys.version_info[0] >= 3


def format(file_metrics, build_metrics):
    """compute output in XML format."""
    def indent(elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    root = ET.Element('metrics')

    # file_metrics
    files = ET.Element('files')
    root.append(files)

    for key in file_metrics.keys():
        tmp_file = ET.SubElement(files, "file",
                                 {'name': key, 'language': file_metrics[key]['language']})
        for name in file_metrics[key].keys():
            if name == 'language':
                continue
            tmp_metric = ET.SubElement(tmp_file, "metric",
                                       {'name': name, 'value': str(file_metrics[key][name])})

    # build_metrics
    if build_metrics:
        build = ET.Element('build')
        root.append(build)
        # TODO

    indent(root)
    if PY3:
        body = ET.tostring(root, encoding='unicode')
    else:
        body = ET.tostring(root)
    return body
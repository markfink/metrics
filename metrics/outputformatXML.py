"""output in XML format.

    initial version 2010 by djcoin (https://bitbucket.org/djcoin)
    All rights reserved, see LICENSE for details.
"""
import xml.etree.ElementTree as ET

def format(metrics):
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

    root = ET.Element('files')

    for key in metrics.keys():
        tmp_file = ET.SubElement(root, "file",
            {'name': key, 'language': metrics[key]['language']})
        for name in metrics[key].keys():
            if name == 'language':
                continue
            tmp_metric = ET.SubElement(tmp_file, "metric",
                {'name': name, 'value': str(metrics[key][name])})

    indent(root)
    return ET.tostring(root)

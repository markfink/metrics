"""
A series of functions for outputting metrics into a series of
machine-readable formats, as well as human readable tables.

Initial version of XML formatter by djcoin
(https://bitbucket.org/djcoin)

All rights reserved, see LICENSE for details.
"""

# Standard
import collections
import json
import xml.etree.ElementTree as ET


def _results_list_to_dict(header_list, results_list):
    """ Convert a list of results into an ordered dictionary. """
    results_dict = collections.OrderedDict()

    for result in results_list:
        results_dict[result[0]] = collections.OrderedDict()
        for index, value in enumerate(result[1:]):
            results_dict[result[0]][header_list[index + 1]] = value

    return results_dict


def format_csv(metric_dict):
    """ Format results data into CSV format. """
    output_list = []
    # Add a column descriptions line using the headers
    output_list.append(','.join(metric_dict['headers']))

    for result in metric_dict['results']:
        output_list.append(','.join(str(x) for x in result))

    return '\n'.join(output_list)


def format_json(metric_dict):
    """ Format results data into JSON format. """
    return json.dumps(_results_list_to_dict(metric_dict['headers'],
                                            metric_dict['results']),
                      indent=2
                     )


def format_table(metric_dict):
    """ Format results data into a human readable text table. """
    header_list = metric_dict['headers']
    result_list = metric_dict['results']
    # Create a list of the length of headers for initial column widths
    row_items = []
    divider_items = []
    for index, header_name in enumerate(header_list):
        column_width = len(header_name)
        for result in result_list:
            result_width = len(str(result[index]))
            if result_width > column_width:
                column_width = result_width
        row_items.append("{{x[{}]:<{}}}".format(index, column_width))
        divider_items.append('-' * (column_width + 1))

    row_string = "  ".join(row_items)
    divider_string = ' '.join(divider_items)

    output_list = [
        row_string.format(x=header_list),
        divider_string,
        divider_string,
        row_string.format(x=metric_dict['totals'])
    ]
    # Insert the result items using string slicing for compatability
    output_list[2:2] = [row_string.format(x=result) for result in result_list]

    return '\n'.join(output_list)


def format_xml(config_dict, metric_dict):
    """ Format results data into XML format. """

    def indent_tree(element, level=0):
        """ A makeshift function for indenting an XML tree. """
        indent = "\n{}".format(level * "  ")
        if element:
            if not element.text or not element.text.strip():
                element.text = indent + "  "
            if not element.tail or not element.tail.strip():
                element.tail = indent
            for element in element:
                indent_tree(element, level + 1)
            if not element.tail or not element.tail.strip():
                element.tail = indent
        else:
            if level and (not element.tail or not element.tail.strip()):
                element.tail = indent

    root = ET.Element(config_dict['root_name'])

    for result in metric_dict['results']:
        item_attrs = {key: result[value] for key, value in config_dict['item_attrs'].items()}
        tmp_file = ET.SubElement(root, config_dict['item_name'], item_attrs)
        offset = config_dict['item_offset']
        for index, _ in enumerate(result[offset:]):
            ET.SubElement(tmp_file, "metric",
                          {'name': metric_dict['headers'][index + offset],
                           'value': str(result[index + offset])
                          })

    indent_tree(root)

    return ET.tostring(root)

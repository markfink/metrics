# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

import pytest

from metrics.metrics import process, format


@pytest.mark.parametrize('in_file, fmt, sloc, comments, ratio, mccabe, language', [
    ('tests/resources/code_samples/js1.js', 'csv', 1446, 46, 0.03, 169, 'JavaScript'),
    ('tests/resources/code_samples/js1.js', 'xml', 1446, 46, 0.03, 169, 'JavaScript'),
    ('tests/resources/code_samples/js1.js', 'json', 1446, 46, 0.03, 169, 'JavaScript'),
])
def test_code_sample(in_file, fmt, sloc, comments, ratio, mccabe, language):
    """Process file put the results into the metrics dictionary."""
    context = dict()  # context
    # moved the metrics list into context dict
    context['quiet'] = True
    context['verbose'] = False
    context['root_dir'] = os.getcwd()
    context['in_file_names'] = [in_file]
    context['output_format'] = fmt

    result = process(context)

    if fmt == 'csv':
        expected = \
            'filename,sloc,comments,ratio_comment_to_code,mccabe,language\n' + \
            '%s,%d,%d,%s,%d,%s\n' % (in_file, sloc, comments, ratio, mccabe, language)

    elif fmt == 'xml':
        expected = (
            '<files>\n' +
            '  <file language="%s" name="%s">\n' % (language, in_file) +
            '    <metric name="sloc" value="%d" />\n' % sloc +
            '    <metric name="comments" value="%d" />\n' % comments +
            '    <metric name="ratio_comment_to_code" value="%s" />\n' % ratio +
            '    <metric name="mccabe" value="%d" />\n' % mccabe +
            '    <metric name="positions" value="[]" />\n' +
            '  </file>\n'
            '</files>\n')

    elif fmt == 'json':
        expected = (
            '{\n' +
            '    "tests/resources/code_samples/js1.js": {\n' +
            '        "comments": 46,\n' +
            '        "language": "JavaScript",\n' +
            '        "mccabe": 169,\n' +
            '        "positions": [],\n' +
            '        "ratio_comment_to_code": 0.03,\n' +
            '        "sloc": 1446\n' +
            '    }\n' +
            '}\n')

    print(format(result, fmt))
    assert format(result, fmt) == expected

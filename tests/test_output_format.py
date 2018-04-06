# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

import pytest

from metrics.metrics_utils import process_file_metrics, format
from metrics.sloc import SLOCMetric
from metrics.mccabe import McCabeMetric
from metrics.position import PosMetric
from metrics import outputformat_json


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

    file_processors = [SLOCMetric(context), McCabeMetric(context), PosMetric(context)]
    result = process_file_metrics(context, file_processors)

    if fmt == 'csv':
        expected = \
            'filename,sloc,comments,ratio_comment_to_code,mccabe,language\n' + \
            '%s,%d,%d,%s,%d,%s\n' % (in_file, sloc, comments, ratio, mccabe, language)

    elif fmt == 'xml':
        expected = (
           '<metrics>\n' +
           '  <files>\n' +
           '    <file language="JavaScript" name="tests/resources/code_samples/js1.js">\n' +
           '      <metric name="sloc" value="1446" />\n' +
           '      <metric name="comments" value="46" />\n' +
           '      <metric name="ratio_comment_to_code" value="0.03" />\n' +
           '      <metric name="mccabe" value="169" />\n' +
           '      <metric name="positions" value="[]" />\n' +
           '    </file>\n' +
           '  </files>\n' +
           '</metrics>\n')

    elif fmt == 'json':
        expected = (
            '{\n' +
            '    "files": {\n' +
            '        "tests/resources/code_samples/js1.js": {\n' +
            '            "comments": 46,\n' +
            '            "language": "JavaScript",\n' +
            '            "mccabe": 169,\n' +
            '            "positions": [],\n' +
            '            "ratio_comment_to_code": 0.03,\n' +
            '            "sloc": 1446\n' +
            '        }\n' +
            '    }\n' +
            '}\n')

    print(format(result, {}, fmt))
    assert format(result, {}, fmt) == expected


def test_output_format_json():
    metrics = outputformat_json.format({'file': 'metrics'}, {'build': 'metrics'})

    assert metrics == (
        '{\n' +
        '    "build": {\n' +
        '        "build": "metrics"\n' +
        '    },\n' +
        '    "files": {\n' +
        '        "file": "metrics"\n' +
        '    }\n' +
        '}\n'
    )

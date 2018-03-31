# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

import pytest

from metrics.metrics import process


@pytest.mark.parametrize('in_file, sloc, comments, ratio, mccabe, language', [
    ('tests/resources/code_samples/nsAccessibleWrap.cpp', 1089, 196, 0.18, 107, 'C++'),
    ('tests/resources/code_samples/js1.js', 1446, 46, 0.03, 169, 'JavaScript'),
    ('tests/resources/code_samples/python_sample.py', 391, 193, 0.49, 125, 'Python'),
])
def test_code_sample(in_file, sloc, comments, ratio, mccabe, language):
    """Process file put the results into the metrics dictionary."""
    context = dict()  # context
    # moved the metrics list into context dict
    #context['include_metrics'] = [('mccabe', 'McCabeMetric'), ('sloc',
    #    'SLOCMetric')]
    context['quiet'] = True
    context['verbose'] = False
    context['root_dir'] = os.getcwd()
    context['in_file_names'] = [in_file]
    context['output_format'] = None

    result = process(context)
    first_key = list(result.keys())[0]
    first_value = list(result.values())[0]
    assert first_key == in_file

    assert first_value['sloc'] == sloc

    assert first_value['comments'] == comments

    assert first_value['ratio_comment_to_code'] == pytest.approx(ratio, 0.1)

    assert first_value['mccabe'] == mccabe

    assert first_value['language'] == language

# Standard
import collections
# Dependency
import pygments.lexers
# Project
from metrics import compute, stock_metrics
# Test
import file_utils

METRICS = collections.OrderedDict([
    ("sloc", stock_metrics.SLOCMetric({})),
    ("comment", stock_metrics.CommentMetric({})),
    ("mccabe", stock_metrics.McCabeMetric({})),
])

PROCESSOR = compute.ResultProcessor(METRICS, {})


def test_result_processor():
    file_expects_dict = {
        'sample_c_files': {
            'sample_1.c': [13, 5, 1],
        },
        'sample_cpp_files': {
            'sample_1.cpp': [11, 4, 1],
            'sample_2.cpp': [22, 37, 1],
        },
        'sample_java_files': {
            'sample_1.java': [27, 6, 1],
            'multiline_comment.java': [0, 1, 0],
        },
        'sample_js_files': {
            'sample_2.js': [1, 1, 0],
        },
        'sample_python_files': {
            'sample_1.py': [18, 7, 0],
        },
        'sample_ruby_files': {
            'sample_1.rb': [10, 8, 0],
            'sample_2.rb': [34, 11, 0],
        },
    }

    for directory in file_expects_dict:
        for a_file in file_expects_dict[directory]:
            contents = file_utils.get_test_file_contents((directory, a_file))
            lexer = pygments.lexers.get_lexer_for_filename(a_file)
            real_result = PROCESSOR.process_string(contents, lexer)
            expected_result = file_expects_dict[directory][a_file]

            assert real_result == expected_result

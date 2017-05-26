"""
Test the reading of Python docstrings, single line comments, and
multiline comments as well.
"""
# Dependency
import pygments.lexers.python as plp
# Local
import file_utils
import metric_utils


def test_single_lines():
    """ Test how single line comments are counted. """

    test_files = [
        ("sample_python_files", "single_comment.py"),
        ("sample_python_files", "multi_single_comment.py")
    ]

    results_list = [1, 3]

    for index, string in enumerate(test_files):
        file_contents = file_utils.get_test_file_contents(test_files[index])
        result = metric_utils.process_comments(file_contents, plp.Python3Lexer)

        assert result == results_list[index]


def test_proper_docstring():
    """
    Test how a docstring with triple quotes on separate lines is
    counted.
    """
    file_contents = file_utils.get_test_file_contents(("sample_python_files",
                                                       "docstring.py"))
    results = metric_utils.process_comments(file_contents, plp.Python3Lexer)

    print(results)
    assert results == 3

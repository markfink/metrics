""" This script tests the importing of metric modules. """

# Dependency
import pytest
# Project
from metrics import main


def test_passing_includes_string():

    test_strings = [
        "metrics.stock_metrics:SLOCMetric",
        "metrics.stock_metrics:SLOCMetric,metrics.stock_metrics:McCabeMetric",
    ]

    expected_results = [
            {'metrics.stock_metrics': ["SLOCMetric"]},
            {'metrics.stock_metrics': ["SLOCMetric", "McCabeMetric"]}
    ]

    for index, a_string in enumerate(test_strings):
        results = main._read_includes_string(a_string)
        for an_item in results:
            assert results[an_item] == expected_results[index][an_item]


@pytest.mark.xfail(raises=ValueError, strict=True)
def test_includes_string_fail():
    """
    This test will try to unpack a split string into two variables,
    but since the items are incorrectly formatted, it will fail. As
    it should.
    """
    test_string = "SLOCMetric,McCabeMetric"

    main._read_includes_string(test_string)

import os
import unittest
from metrics.metrics import process
from metrics.outputformatXML import format


class OutputXmlTest(unittest.TestCase):

    def setUp(self):
        """Create metrics for test file."""
        context = {}    # context in which token was used
        # moved the metrics list into context dict
        context['include_metrics'] = [('mccabe', 'McCabeMetric'),
            ('sloc', 'SLOCMetric')]
        context['quiet'] = True
        context['verbose'] = False
        context['base'] = ''
        self.in_file = os.path.abspath('tests/code_samples/js1.js')
        context['in_file_names'] = [self.in_file]
        context['output_format'] = None

        self.metrics = process(context)

    def test_output(self):

        expected = '''<files>\n  <file language="JavaScript+Lasso" name="/home/mark/devel/metrics/tests/code_samples/js1.js">\n    <metric name="mccabe" value="169" />\n    <metric name="ratio_comment_to_code" value="0.03" />\n    <metric name="comments" value="47" />\n    <metric name="sloc" value="1446" />\n  </file>\n</files>\n'''
        self.assertEqual(format(self.metrics), expected)

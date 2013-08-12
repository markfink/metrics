import os
import unittest
from metrics.metrics import process
from metrics.outputformatCSV import format


class OutputCsvTest(unittest.TestCase):

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
        context['output_format'] = 'csv'

        self.metrics = process(context)

    def test_output(self):

        expected = '''filename,mccabe,ratio_comment_to_code,language,comments,sloc\n/home/mark/devel/metrics/tests/code_samples/js1.js,169,0.03,JavaScript+Lasso,47,1446\n'''
        self.assertEqual(format(self.metrics), expected)

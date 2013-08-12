import os
import unittest
from metrics.metrics import process


class JavascriptFileTest(unittest.TestCase):

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

    def test_sloc(self):
        self.assertEqual(self.metrics[self.in_file]['sloc'], 1446)

    def test_comments(self):
        self.assertEqual(self.metrics[self.in_file]['comments'], 47)

    def test_ratio_comment_to_code(self):
        self.assertAlmostEqual(
            self.metrics[self.in_file]['ratio_comment_to_code'], 0.03)

    def test_mccabe(self):
        self.assertEqual(self.metrics[self.in_file]['mccabe'], 169)

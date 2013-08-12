import os
import unittest
from metrics.metrics import process


class CppFileTest(unittest.TestCase):

    def setUp(self):
        """Process file put the results into hte metrics dicitionary."""
        context = {}    # context in which token was used
        # moved the metrics list into context dict
        context['include_metrics'] = [('mccabe', 'McCabeMetric'), ('sloc',
            'SLOCMetric')]
        context['quiet'] = True
        context['verbose'] = False
        context['base'] = ''
        self.in_file = os.path.abspath(
            'tests/code_samples/nsAccessibleWrap.cpp')
        context['in_file_names'] = [self.in_file]
        context['output_format'] = None

        self.metrics = process(context)

    def test_sloc(self):
        self.assertEqual(self.metrics[self.in_file]['sloc'], 1089)

    def test_comments(self):
        self.assertEqual(self.metrics[self.in_file]['comments'], 196)

    def test_ratio_comment_to_code(self):
        self.assertAlmostEqual(
            self.metrics[self.in_file]['ratio_comment_to_code'], 0.18)

    def test_mccabe(self):
        self.assertEqual(self.metrics[self.in_file]['mccabe'], 107)

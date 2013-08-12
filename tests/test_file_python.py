import unittest
from metrics.metrics import process


class PythonFileTest(unittest.TestCase):

    def setUp(self):
        """Create metrics for test file."""
        context = {}    # context in which token was used
        # moved the metrics list into context dict
        context['include_metrics'] = [('mccabe', 'McCabeMetric'),
            ('sloc', 'SLOCMetric')]
        context['quiet'] = True
        context['verbose'] = True
        context['base'] = ''
        self.in_file = '/home/mark/devel/metrics/tests/code_samples/python_sample.py'
        context['in_file_names'] = [self.in_file]
        context['output_format'] = None

        self.metrics = process(context)

    def test_language(self):
        self.assertEqual(self.metrics[self.in_file]['language'], 'Python')

    def test_sloc(self):
        self.assertEqual(self.metrics[self.in_file]['sloc'], 391)

    def test_comments(self):
        self.assertEqual(self.metrics[self.in_file]['comments'], 193)

    def test_ratio_comments_to_code(self):
        self.assertAlmostEqual(
            self.metrics[self.in_file]['ratio_comment_to_code'], 0.49)

    def test_mccabe(self):
        self.assertEqual(self.metrics[self.in_file]['mccabe'], 125)

"""
compute.py

Computational wrapper classes for metrics.

All rights reserved, see LICENSE.txt for details.
"""

# Standard
import collections
import os
# Dependency
import pygments.lexers

TOKEN_TUPLE = collections.namedtuple('TokenTuple', ("type", "short_type", "value"))


def _token_to_token_tuple(token):
    """
    Return a namedtuple specifying the different parts of a Pygments
    token object in a more readable fashion.
    """
    return TOKEN_TUPLE(type=str(token[0]), short_type=token[0][0], value=token[1])


def _dict_to_list_list(a_dict):
    """
    Return a list of lists containing the dictionary item's key as
    the first item in the new list, and the values within the
    dictionary item's value (which should be a list) following.

    For example ``{"string": ["This is", " a test"]}`` would become
    ``[["string", "This is", "a test"]]``.
    """
    output_list = []
    for key, value in a_dict.items():
        result_list = value
        result_list.insert(0, key)
        output_list.append(result_list)
    return output_list


class MetricComputer():
    """ A wrapper class which handles the metrics. """

    def __init__(self, metric_instances):
        self.instances = metric_instances.values()

    def compute(self, token_list):
        """ Loop over the token list using each metric instance. """
        for token in token_list:
            token_tuple = _token_to_token_tuple(token)
            for metric in self.instances:
                metric.process_token(token_tuple)

    def reset(self):
        """ Reset all metric instances. """
        for metric in self.instances:
            metric.reset()

    def get_metric_list(self):
        """
        Return all metric results from each metric instances in the
        form of a list.
        """
        metric_list = []
        for metric_instance in self.instances:
            metric_list.append(metric_instance.get_metrics())

        return metric_list


class ResultProcessor():
    """
    A wrapper class for processing metrics for files and obtaining
    results in suitable data types.
    """

    def __init__(self, metric_instances, context):
        self.metric_instances = metric_instances
        self.computer = MetricComputer(metric_instances)
        self.context = context
        # Define the headers defining different results
        self.metric_names = [self.metric_instances[metric].name for metric in self.metric_instances]
        # Define containers for file results
        self.results_list = []
        self.total_results_list = []

    def _get_headers(self, default_headers):
        """ Add metric headers to default headers. """
        header_list = default_headers
        header_list.extend(self.metric_names)
        return header_list

    def _get_language_totals(self):
        """
        Return totals for each programming language that was found.
        """
        language_dict = collections.OrderedDict()
        for result in self.results_list:
            language = result[1]
            if language not in language_dict:
                language_dict[language] = [0 for metric in self.metric_names]
            for index, metric_value in enumerate(result[2:]):
                language_dict[language][index] += metric_value

        return _dict_to_list_list(language_dict)

    def _get_totals(self, index_offset):
        """
        Return the totals for all file results offset properly by an
        index to make printing easier.
        """
        # Offset the list with empty strings for non-number headers
        total_list = ['' for index in range(index_offset)]
        for index, _ in enumerate(self.metric_names):
            # Increase index by 2 to go past the filename and language strings
            value_list = [metric_list[index + 2] for metric_list in self.results_list]
            total_list.append(sum(value_list))

        return total_list

    def _get_raw_results(self):
        """ Return the raw results dictionary. """
        return self.results_list

    def get_file_results(self):
        """
        Return a dictionary for interpretting results for individual
        files that were specified.
        """
        return {
            'headers': self._get_headers(["Filename", "Language"]),
            'results': self._get_raw_results(),
            'totals': self._get_totals(2)
        }

    def get_language_results(self):
        """
        Return a dictionary for interpretting results for each
        programming present within the files specified.
        """
        return {
            'headers': self._get_headers(["Language"]),
            'results': self._get_language_totals(),
            'totals': self._get_totals(1)
        }

    def process_string(self, a_string, lexer):
        """
        Return a list containing the results of each metric that was
        run upon the string in integer form.
        """
        token_list = lexer.get_tokens(a_string)
        self.computer.compute(token_list)
        computed_list = self.computer.get_metric_list()
        # Reset all of the metric counters
        self.computer.reset()

        return computed_list

    def process_file(self, file_path):
        """
        Open the specified file path if the path is valid, find the
        correct lexographical scanner for the file, and finally add
        the results to the processor's result_list attribute.
        """
        # Guard for directory paths
        if os.path.isdir(file_path):
            # Raise the appropiate error
            raise IsADirectoryError

        # Open the file and read it
        with open(file_path, 'r') as file_object:
            # This may cause a UnicodeDecodeError, so be sure to deal
            # with that error
            contents = file_object.read()

        # Find the lexographical scanner to use
        lex = pygments.lexers.guess_lexer_for_filename(file_path,
                                                       contents,
                                                       encoding="guess")

        # Add in the basic fields
        file_results = [file_path, lex.name]
        # Compute metrics upon a file
        metric_results = self.process_string(contents, lex)
        # Append the computed metrics to lists
        # total_metrics_list.append(metric_results)
        file_results.extend(metric_results)
        self.results_list.append(file_results)

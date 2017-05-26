"""
stock_metrics.py

A module containing common metric classes.

All rights reserved, see LICENSE.txt for details.
"""

# Project
from metrics import metric_base


class CommentMetric(metric_base.MetricBase):
    """ Count the number of comments present in a file. """

    name = "Comments"

    def process_token(self, token):
        """ Incriment the counter for single and multiline comments. """

        long_comment_types = (
            "Token.Comment.Multiline",
            "Token.Comment",
            "Token.Literal.String.Doc"
        )

        if token.type in long_comment_types:
            # This means we have a docstring, or a multiline comment
            line_count = token.value.count('\n')
            if line_count == 0:
                self._count += 1
            else:
                self._count += line_count
        elif token.type in "Token.Comment.Single":
            # Just a single line comment
            self._count += 1


class McCabeMetric(metric_base.MetricBase):
    """ Compute McCabe's Cyclomatic metric for a file. """

    name = "McCabe"

    def process_token(self, token):
        """ Increment for each decision point in a function. """
        mccabe_keywords = (
            "assert",
            "break",
            "continue",
            "elif",
            "else",
            "for",
            "if",
            "while"
        )
        # If token and token.text in mccabe_keywords
        if token.short_type == 'Keyword' and token.value in mccabe_keywords:
            self._count += 1


class SLOCMetric(metric_base.MetricBase):
    """
    Compute the Standard Lines of Code for a file yielding results
    similar to that of SLOCCount.
    """

    name = "SLOC"
    _contains_code = False

    def process_token(self, token):
        """ Incriment non-empty lines containing code. """

        token_types = (
            'Keyword',
            'Name',
            'Punctuation',
            'Operator',
            'Literal'
        )

        if self._contains_code and token.value[0] == '\n':
            self._count += 1
            self._contains_code = False
        # Count C-style include statements as code too
        elif token.short_type in token_types or token.type == "Token.Comment.Preproc":
            self._contains_code = True

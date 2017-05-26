# Dependency
import pygments
import pygments.lexers.python
# Project
from metrics import compute, stock_metrics

PYTHON3_LEXER = pygments.lexers.python.Python3Lexer


def process_tokens(a_string, lexer, metric):
    """ Process tokens using the SLOC metric. """
    token_list = pygments.lex(a_string, lexer())

    for token in token_list:
        metric.process_token(compute._token_to_token_tuple(token))

    results = metric.get_metrics()
    metric.reset()

    return results


def process_comments(a_string, lexer):
    return process_tokens(a_string, lexer,
                          stock_metrics.CommentMetric({}))


def process_sloc(a_string, lexer):
    return process_tokens(a_string, lexer, stock_metrics.SLOCMetric({}))

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pygments.token import Token

from metrics.sloc import SLOCMetric


def test_with_python_class():
    #class MyClass:
    #    """Definitely first class!"""
    #    variable = "blah"
    #
    #    def my_func(self):
    #        """Work the incredible magic."""
    #        print("This is a message.")

    tokens = [
        (Token.Keyword, u'class'), (Token.Text, u' '),
        (Token.Name.Class, u'MyClass'), (Token.Punctuation, u':'),
        (Token.Text, u'\n'), (Token.Text, u'    '),
        (Token.Literal.String.Doc, u'"""Definitely first class!"""'),
        (Token.Text, u'\n'), (Token.Text, u'    '),
        (Token.Name, u'variable'), (Token.Text, u' '),
        (Token.Operator, u'='), (Token.Text, u' '),
        (Token.Literal.String.Double, u'"'),
        (Token.Literal.String.Double, u'blah'),
        (Token.Literal.String.Double, u'"'), (Token.Text, u'\n'),
        (Token.Text, u'\n'), (Token.Text, u'    '),
        (Token.Keyword, u'def'), (Token.Text, u' '),
        (Token.Name.Function, u'my_func'), (Token.Punctuation, u'('),
        (Token.Name.Builtin.Pseudo, u'self'), (Token.Punctuation, u')'),
        (Token.Punctuation, u':'), (Token.Text, u'\n'),
        (Token.Text, u'        '),
        (Token.Literal.String.Doc, u'"""Work the incredible magic."""'),
        (Token.Text, u'\n'), (Token.Text, u'        '),
        (Token.Keyword, u'print'), (Token.Punctuation, u'('),
        (Token.Literal.String.Double, u'"'),
        (Token.Literal.String.Double, u'This is a message.'),
        (Token.Literal.String.Double, u'"'), (Token.Punctuation, u')'),
        (Token.Text, u'\n')
    ]

    sloc = SLOCMetric(context={})
    for t in tokens:
        sloc.process_token(t)
    assert sloc.metrics == {'sloc': 4, 'comments': 2, 'ratio_comment_to_code': 0.5}

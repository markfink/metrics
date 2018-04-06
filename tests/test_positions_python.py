# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pygments.token import Token

from metrics.position import PosMetric


def test_with_python_global_code():
    # """ Increment number of decision points in function."""
    ##if tok and tok.text in McCabeKeywords:
    # if (tok[0][0] == b'Keyword') and tok[1] in McCabeKeywords:
    #    self.metrics['mccabe'] += 1
    tokens = [
        (Token.Literal.String.Doc,
         u'""" Increment number of decision points in function."""'),
        (Token.Text, u'\n'), (
            Token.Comment.Single,
            u'#if tok and tok.text in McCabeKeywords:'),
        (Token.Text, u'\n'), (Token.Keyword, u'if'), (Token.Text, u' '),
        (Token.Punctuation, u'('), (Token.Name, u'tok'),
        (Token.Punctuation, u'['), (Token.Literal.Number.Integer, u'0'),
        (Token.Punctuation, u']'), (Token.Punctuation, u'['),
        (Token.Literal.Number.Integer, u'0'), (Token.Punctuation, u']'),
        (Token.Text, u' '), (Token.Operator, u'=='), (Token.Text, u' '),
        (Token.Literal.String.Affix, u'b'),
        (Token.Literal.String.Single, u"'"),
        (Token.Literal.String.Single, u'Keyword'),
        (Token.Literal.String.Single, u"'"), (Token.Punctuation, u')'),
        (Token.Text, u' '), (Token.Operator.Word, u'and'),
        (Token.Text, u' '), (Token.Name, u'tok'),
        (Token.Punctuation, u'['), (Token.Literal.Number.Integer, u'1'),
        (Token.Punctuation, u']'), (Token.Text, u' '),
        (Token.Operator.Word, u'in'), (Token.Text, u' '),
        (Token.Name, u'McCabeKeywords'), (Token.Punctuation, u':'),
        (Token.Text, u'\n'), (Token.Name.Builtin.Pseudo, u'self'),
        (Token.Operator, u'.'), (Token.Name, u'metrics'),
        (Token.Punctuation, u'['), (Token.Literal.String.Single, u"'"),
        (Token.Literal.String.Single, u'mccabe'),
        (Token.Literal.String.Single, u"'"), (Token.Punctuation, u']'),
        (Token.Text, u' '), (Token.Operator, u'+'),
        (Token.Operator, u'='), (Token.Text, u' '),
        (Token.Literal.Number.Integer, u'1'), (Token.Text, u'\n')]

    positions = PosMetric(context={})
    positions.language = 'Python'
    for t in tokens:
        positions.process_token(t)
    assert positions.metrics == {'positions': []}


def test_with_python_function():
    # def my_func(p1, p2):
    #     """Work the incredible magic."""
    #     return p1 + p2
    tokens = [
        (Token.Keyword, u'def'), (Token.Text, u' '),
        (Token.Name.Function, u'my_func'), (Token.Punctuation, u'('),
        (Token.Name, u'p1'), (Token.Punctuation, u','), (Token.Text, u' '),
        (Token.Name, u'p2'), (Token.Punctuation, u')'),
        (Token.Punctuation, u':'), (Token.Text, u'\n'),
        (Token.Text, u'    '),
        (Token.Literal.String.Doc, u'"""Work the incredible magic."""'),
        (Token.Text, u'\n'),
        (Token.Text, u'    '), (Token.Keyword, u'return'), (Token.Text, u' '),
        (Token.Name, u'p1'), (Token.Text, u' '), (Token.Operator, u'+'),
        (Token.Text, u' '), (Token.Name, u'p2'), (Token.Text, u'\n')
    ]

    positions = PosMetric(context={})
    positions.language = 'Python'
    for t in tokens:
        positions.process_token(t)
    assert positions.metrics == \
        {'positions': [{'type': 'Function', 'name': 'my_func', 'start': 1, 'end': 3}]}


def test_with_python_class():
    # class MyClass:
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

    positions = PosMetric(context={})
    positions.language = 'Python'
    for t in tokens:
        positions.process_token(t)
    assert positions.metrics == {'positions': [
        {
        'type': 'Class',
        'name': 'MyClass',
        'start': 1,
        'end': 7,
        'methods': [
            {'type': 'Function', 'name': 'my_func', 'start': 5, 'end': 7}
        ],
    }]}

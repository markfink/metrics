# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import textwrap

from pygments.lexers import PythonLexer
from pygments.token import Token


def test_lexer_on_python_global_code():
    code = textwrap.dedent('''
        """ Increment number of decision points in function."""
        #if tok and tok.text in McCabeKeywords:
        if (tok[0][0] == b'Keyword') and tok[1] in McCabeKeywords:
        self.metrics['mccabe'] += 1
        ''')
    result = [(Token.Literal.String.Doc, u'""" Increment number of decision points in function."""'), (Token.Text, u'\n'), (Token.Comment.Single, u'#if tok and tok.text in McCabeKeywords:'), (Token.Text, u'\n'), (Token.Keyword, u'if'), (Token.Text, u' '), (Token.Punctuation, u'('), (Token.Name, u'tok'), (Token.Punctuation, u'['), (Token.Literal.Number.Integer, u'0'), (Token.Punctuation, u']'), (Token.Punctuation, u'['), (Token.Literal.Number.Integer, u'0'), (Token.Punctuation, u']'), (Token.Text, u' '), (Token.Operator, u'=='), (Token.Text, u' '), (Token.Literal.String.Affix, u'b'), (Token.Literal.String.Single, u"'"), (Token.Literal.String.Single, u'Keyword'), (Token.Literal.String.Single, u"'"), (Token.Punctuation, u')'), (Token.Text, u' '), (Token.Operator.Word, u'and'), (Token.Text, u' '), (Token.Name, u'tok'), (Token.Punctuation, u'['), (Token.Literal.Number.Integer, u'1'), (Token.Punctuation, u']'), (Token.Text, u' '), (Token.Operator.Word, u'in'), (Token.Text, u' '), (Token.Name, u'McCabeKeywords'), (Token.Punctuation, u':'), (Token.Text, u'\n'), (Token.Name.Builtin.Pseudo, u'self'), (Token.Operator, u'.'), (Token.Name, u'metrics'), (Token.Punctuation, u'['), (Token.Literal.String.Single, u"'"), (Token.Literal.String.Single, u'mccabe'), (Token.Literal.String.Single, u"'"), (Token.Punctuation, u']'), (Token.Text, u' '), (Token.Operator, u'+'), (Token.Operator, u'='), (Token.Text, u' '), (Token.Literal.Number.Integer, u'1'), (Token.Text, u'\n')]

    lex = PythonLexer()
    tokenList = lex.get_tokens(code)
    #print(list(tokenList))
    assert list(tokenList) == result


def test_lexer_on_python_function():
    code = textwrap.dedent('''
        def my_func(p1, p2):
            """Work the incredible magic."""
            return p1 + p2
        ''')
    result = [
        (Token.Keyword, u'def'), (Token.Text, u' '), (Token.Name.Function, u'my_func'), (Token.Punctuation, u'('), (Token.Name, u'p1'), (Token.Punctuation, u','), (Token.Text, u' '), (Token.Name, u'p2'), (Token.Punctuation, u')'), (Token.Punctuation, u':'), (Token.Text, u'\n'),
        (Token.Text, u'    '), (Token.Literal.String.Doc, u'"""Work the incredible magic."""'), (Token.Text, u'\n'),
        (Token.Text, u'    '), (Token.Keyword, u'return'), (Token.Text, u' '), (Token.Name, u'p1'), (Token.Text, u' '), (Token.Operator, u'+'), (Token.Text, u' '), (Token.Name, u'p2'), (Token.Text, u'\n')
    ]

    lex = PythonLexer()
    tokenList = lex.get_tokens(code)
    #print(list(tokenList))
    assert list(tokenList) == result


def test_lexer_on_python_class():
    code = textwrap.dedent('''
        class MyClass:
            """Definitely first class!"""
            variable = "blah"

            def my_func(self):
                """Work the incredible magic."""
                print("This is a message.")
        ''')
    result = [(Token.Keyword, u'class'), (Token.Text, u' '), (Token.Name.Class, u'MyClass'), (Token.Punctuation, u':'), (Token.Text, u'\n'), (Token.Text, u'    '), (Token.Literal.String.Doc, u'"""Definitely first class!"""'), (Token.Text, u'\n'), (Token.Text, u'    '), (Token.Name, u'variable'), (Token.Text, u' '), (Token.Operator, u'='), (Token.Text, u' '), (Token.Literal.String.Double, u'"'), (Token.Literal.String.Double, u'blah'), (Token.Literal.String.Double, u'"'), (Token.Text, u'\n'), (Token.Text, u'\n'), (Token.Text, u'    '), (Token.Keyword, u'def'), (Token.Text, u' '), (Token.Name.Function, u'my_func'), (Token.Punctuation, u'('), (Token.Name.Builtin.Pseudo, u'self'), (Token.Punctuation, u')'), (Token.Punctuation, u':'), (Token.Text, u'\n'), (Token.Text, u'        '), (Token.Literal.String.Doc, u'"""Work the incredible magic."""'), (Token.Text, u'\n'), (Token.Text, u'        '), (Token.Keyword, u'print'), (Token.Punctuation, u'('), (Token.Literal.String.Double, u'"'), (Token.Literal.String.Double, u'This is a message.'), (Token.Literal.String.Double, u'"'), (Token.Punctuation, u')'), (Token.Text, u'\n')]

    lex = PythonLexer()
    tokenList = lex.get_tokens(code)
    #print(list(tokenList))
    assert list(tokenList) == result
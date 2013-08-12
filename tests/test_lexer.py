from unittest import TestCase
from pygments.lexers import PythonLexer
from pygments.token import Token
import sys
import os

class LexerTest(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def testWorksAsExpected(self):
        code = '''
        """ Increment number of decision points in function."""
        #if tok and tok.text in McCabeKeywords:
        if (tok[0][0] == b'Keyword') and tok[1] in McCabeKeywords:
            self.metrics['mccabe'] += 1
        '''
        result = [(Token.Text, u'        '), (Token.Literal.String.Doc, u'""" Increment number of decision points in function."""'), (Token.Text, u'\n'), (Token.Text, u'        '), (Token.Comment, u'#if tok and tok.text in McCabeKeywords:'), (Token.Text, u'\n'), (Token.Text, u'        '), (Token.Keyword, u'if'), (Token.Text, u' '), (Token.Punctuation, u'('), (Token.Name, u'tok'), (Token.Punctuation, u'['), (Token.Literal.Number.Integer, u'0'), (Token.Punctuation, u']'), (Token.Punctuation, u'['), (Token.Literal.Number.Integer, u'0'), (Token.Punctuation, u']'), (Token.Text, u' '), (Token.Operator, u'=='), (Token.Text, u' '), (Token.Name, u'b'), (Token.Literal.String, u"'"), (Token.Literal.String, u'Keyword'), (Token.Literal.String, u"'"), (Token.Punctuation, u')'), (Token.Text, u' '), (Token.Operator.Word, u'and'), (Token.Text, u' '), (Token.Name, u'tok'), (Token.Punctuation, u'['), (Token.Literal.Number.Integer, u'1'), (Token.Punctuation, u']'), (Token.Text, u' '), (Token.Operator.Word, u'in'), (Token.Text, u' '), (Token.Name, u'McCabeKeywords'), (Token.Punctuation, u':'), (Token.Text, u'\n'), (Token.Text, u'            '), (Token.Name.Builtin.Pseudo, u'self'), (Token.Operator, u'.'), (Token.Name, u'metrics'), (Token.Punctuation, u'['), (Token.Literal.String, u"'"), (Token.Literal.String, u'mccabe'), (Token.Literal.String, u"'"), (Token.Punctuation, u']'), (Token.Text, u' '), (Token.Operator, u'+'), (Token.Operator, u'='), (Token.Text, u' '), (Token.Literal.Number.Integer, u'1'), (Token.Text, u'\n'), (Token.Text, u'        '), (Token.Text, u'\n')]

        lex = PythonLexer()
        tokenList = lex.get_tokens(code)
        self.assertEqual(list(tokenList), result)


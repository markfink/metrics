# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import textwrap

from pygments.lexers.web import JavascriptLexer
from pygments.token import Token


def test_lexer_on_javascript_class():
    code = textwrap.dedent('''
        class User {
          constructor(name) {
            this.name = name;
          }
        
          sayHi() {
            alert(this.name);
          }
        
        }
        
        let user = new User("John");
        user.sayHi();
        ''')
    result = [
        (Token.Keyword.Reserved, 'class'),  # <--
        (Token.Text, ' '),
        (Token.Name.Other, 'User'),
        (Token.Text, ' '),
        (Token.Punctuation, '{'),
        (Token.Text, '\n  '),
        (Token.Name.Other, 'constructor'),
        (Token.Punctuation, '('),
        (Token.Name.Other, 'name'),
        (Token.Punctuation, ')'),
        (Token.Text, ' '),
        (Token.Punctuation, '{'),
        (Token.Text, '\n    '),
        (Token.Keyword, 'this'),
        (Token.Punctuation, '.'),
        (Token.Name.Other, 'name'),
        (Token.Text, ' '),
        (Token.Operator, '='),
        (Token.Text, ' '),
        (Token.Name.Other, 'name'),
        (Token.Punctuation, ';'),
        (Token.Text, '\n  '),
        (Token.Punctuation, '}'),
        (Token.Text, '\n\n  '),
        (Token.Name.Other, 'sayHi'),
        (Token.Punctuation, '('),
        (Token.Punctuation, ')'),
        (Token.Text, ' '),
        (Token.Punctuation, '{'),
        (Token.Text, '\n    '),
        (Token.Name.Other, 'alert'),
        (Token.Punctuation, '('),
        (Token.Keyword, 'this'),
        (Token.Punctuation, '.'),
        (Token.Name.Other, 'name'),
        (Token.Punctuation, ')'),
        (Token.Punctuation, ';'),
        (Token.Text, '\n  '),
        (Token.Punctuation, '}'),
        (Token.Text, '\n\n'),
        (Token.Punctuation, '}'),
        (Token.Text, '\n\n'),
        (Token.Keyword.Declaration, 'let'),
        (Token.Text, ' '),
        (Token.Name.Other, 'user'),
        (Token.Text, ' '),
        (Token.Operator, '='),
        (Token.Text, ' '),
        (Token.Keyword, 'new'),
        (Token.Text, ' '),
        (Token.Name.Other, 'User'),
        (Token.Punctuation, '('),
        (Token.Literal.String.Double, '"John"'),
        (Token.Punctuation, ')'),
        (Token.Punctuation, ';'),
        (Token.Text, '\n'),
        (Token.Name.Other, 'user'),
        (Token.Punctuation, '.'),
        (Token.Name.Other, 'sayHi'),
        (Token.Punctuation, '('),
        (Token.Punctuation, ')'),
        (Token.Punctuation, ';'),
        (Token.Text, '\n')
    ]

    lex = JavascriptLexer()
    tokenList = lex.get_tokens(code)
    # print(list(tokenList))
    assert list(tokenList) == result

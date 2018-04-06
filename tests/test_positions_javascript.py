# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import textwrap

from pygments.token import Token

from metrics.position import PosMetric


def test_with_javascript_class():
    #class User {
    #  constructor(name) {
    #    this.name = name;
    #  }
    #
    #  sayHi() {
    #    alert(this.name);
    #  }
    #
    #}
    #
    #let user = new User("John");
    #user.sayHi();
    tokens = [
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

    positions = PosMetric(context={})
    positions.language = 'Javascript'
    for t in tokens:
        positions.process_token(t)
    assert positions.metrics == {'positions': [
        {'type': 'Class', 'name': 'User', 'start': 1, 'end': 10}
    ]}

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pygments.token import Token
from metrics.position import PosMetric


def test_lexer_on_go_code():
    # type Animal interface {
    #  Name() string
    # }
    #
    # type Dog struct {}
    #
    # func (d *Dog) Name() string {
    #  return “Dog”
    # }
    #
    # func (d *Dog) Bark() {
    #  fmt.Println(“Woof!”)
    # }
    tokens = [
        (Token.Keyword.Declaration, 'type'),  # <--
        (Token.Text, ' '),
        (Token.Name.Other, 'Animal'),
        (Token.Text, ' '),
        (Token.Keyword.Declaration, 'interface'),  # <--
        (Token.Text, ' '),
        (Token.Punctuation, '{'),
        (Token.Text, '\n'),
        (Token.Text, '  '),
        (Token.Name.Other, 'Name'),
        (Token.Punctuation, '('),
        (Token.Punctuation, ')'),
        (Token.Text, ' '),
        (Token.Keyword.Type, 'string'),
        (Token.Text, '\n'),
        (Token.Punctuation, '}'),
        (Token.Text, '\n'),
        (Token.Text, '\n'),
        (Token.Keyword.Declaration, 'type'),
        (Token.Text, ' '),
        (Token.Name.Other, 'Dog'),
        (Token.Text, ' '),
        (Token.Keyword.Declaration, 'struct'),  # <--
        (Token.Text, ' '),
        (Token.Punctuation, '{'),
        (Token.Punctuation, '}'),
        (Token.Text, '\n'),
        (Token.Text, '\n'),
        (Token.Keyword.Declaration, 'func'),  # <--
        (Token.Text, ' '),
        (Token.Punctuation, '('),
        (Token.Name.Other, 'd'),
        (Token.Text, ' '),
        (Token.Operator, '*'),
        (Token.Name.Other, 'Dog'),
        (Token.Punctuation, ')'),
        (Token.Text, ' '),
        (Token.Name.Other, 'Name'),
        (Token.Punctuation, '('),
        (Token.Punctuation, ')'),
        (Token.Text, ' '),
        (Token.Keyword.Type, 'string'),
        (Token.Text, ' '),
        (Token.Punctuation, '{'),
        (Token.Text, '\n'),
        (Token.Text, '  '),
        (Token.Keyword, 'return'),
        (Token.Text, ' '),
        (Token.Error, '“'),
        (Token.Name.Other, 'Dog'),
        (Token.Error, '”'),
        (Token.Text, '\n'),
        (Token.Punctuation, '}'),
        (Token.Text, '\n'),
        (Token.Text, '\n'),
        (Token.Keyword.Declaration, 'func'),  # <--
        (Token.Text, ' '),
        (Token.Punctuation, '('),
        (Token.Name.Other, 'd'),
        (Token.Text, ' '),
        (Token.Operator, '*'),
        (Token.Name.Other, 'Dog'),
        (Token.Punctuation, ')'),
        (Token.Text, ' '),
        (Token.Name.Other, 'Bark'),
        (Token.Punctuation, '('),
        (Token.Punctuation, ')'),
        (Token.Text, ' '),
        (Token.Punctuation, '{'),
        (Token.Text, '\n'),
        (Token.Text, '  '),
        (Token.Name.Other, 'fmt'),
        (Token.Punctuation, '.'),
        (Token.Name.Other, 'Println'),
        (Token.Punctuation, '('),
        (Token.Error, '“'),
        (Token.Name.Other, 'Woof'),
        (Token.Punctuation, '!'),
        (Token.Error, '”'),
        (Token.Punctuation, ')'),
        (Token.Text, '\n'),
        (Token.Punctuation, '}'),
        (Token.Text, '\n')]

    positions = PosMetric(context={})
    positions.language = 'Go'
    for t in tokens:
        positions.process_token(t)
    assert positions.metrics == {'positions': [
        {'type': 'Interface', 'name': 'Animal', 'start': 1, 'end': 3},
        {'type': 'Struct', 'name': 'Dog', 'start': 5, 'end': 5},
        {'type': 'Function', 'name': 'Name', 'start': 7, 'end': 9},
        {'type': 'Function', 'name': 'Bark', 'start': 11, 'end': 13}
    ]}

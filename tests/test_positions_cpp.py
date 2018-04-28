# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pygments.token import Token
from metrics.position import PosMetric


def test_lexer_on_cpp_class():
    ##include <iostream>
    # using namespace std;
    #
    # class Rectangle {
    #    int width, height;
    #  public:
    #    void set_values (int,int);
    #    int area() {return width*height;}
    # };
    tokens = [
        (Token.Comment.Preproc, '#'),
        (Token.Comment.Preproc, 'include'),
        (Token.Text, ' '),
        (Token.Comment.PreprocFile, '<iostream>'),
        (Token.Comment.Preproc, '\n'),
        (Token.Keyword, 'using'),
        (Token.Text, ' '),
        (Token.Keyword, 'namespace'),
        (Token.Text, ' '),
        (Token.Name, 'std'),
        (Token.Punctuation, ';'),
        (Token.Text, '\n'),
        (Token.Text, '\n'),
        (Token.Keyword, 'class'),
        (Token.Text, ' '),
        (Token.Name.Class, 'Rectangle'),  # <--
        (Token.Text, ' '),
        (Token.Punctuation, '{'),
        (Token.Text, '\n'),
        (Token.Text, '    '),
        (Token.Keyword.Type, 'int'),
        (Token.Text, ' '),
        (Token.Name, 'width'),
        (Token.Punctuation, ','),
        (Token.Text, ' '),
        (Token.Name, 'height'),
        (Token.Punctuation, ';'),
        (Token.Text, '\n'),
        (Token.Text, '  '),
        (Token.Keyword, 'public'),
        (Token.Operator, ':'),
        (Token.Text, '\n'),
        (Token.Text, '    '),
        (Token.Keyword.Type, 'void'),
        (Token.Text, ' '),
        (Token.Name, 'set_values'),
        (Token.Text, ' '),
        (Token.Punctuation, '('),
        (Token.Keyword.Type, 'int'),
        (Token.Punctuation, ','),
        (Token.Keyword.Type, 'int'),
        (Token.Punctuation, ')'),
        (Token.Punctuation, ';'),
        (Token.Text, '\n'),
        (Token.Text, '    '),
        (Token.Keyword.Type, 'int'),
        (Token.Text, ' '),
        (Token.Name.Function, 'area'),  # <--
        (Token.Punctuation, '('),
        (Token.Punctuation, ')'),
        (Token.Text, ' '),
        (Token.Punctuation, '{'),
        (Token.Keyword, 'return'),
        (Token.Text, ' '),
        (Token.Name, 'width'),
        (Token.Operator, '*'),
        (Token.Name, 'height'),
        (Token.Punctuation, ';'),
        (Token.Punctuation, '}'),
        (Token.Text, '\n'),
        (Token.Punctuation, '}'),
        (Token.Punctuation, ';'),
        (Token.Text, '\n')
    ]

    positions = PosMetric(context={})
    positions.language = 'C++'
    for t in tokens:
        positions.process_token(t)
    assert positions.metrics == {'block_positions': [{
        'type': 'Class',
        'name': 'Rectangle',
        'start': 3,
        'end': 8,
        'methods': [{'type': 'Function', 'name': 'area', 'start': 7, 'end': 8}],
    }]}

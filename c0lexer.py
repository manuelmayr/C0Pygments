# -*- coding: utf-8 -*-
"""
    C0Lexer
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for Language C0

    :copyright: Copyright 2012 by Manuel Mayr
    :license: BSD, see LICENSE for details.
"""

import re
from string import Template

from pygments.lexer import Lexer, RegexLexer, include, bygroups, using, this
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
                           Number, Punctuation, Error, Literal

class C0Lexer(RegexLexer):
    """
    For C0 source code
    """
    name = 'C0' 
    aliases = ['c0']
    filename = ['*.c0', '*.h0']
    mimetypes = ['text/x-c0hdr', 'text/x-c0src']

    #: optional Comment or Whitespace
    _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'

    tokens = {
        'root': [
            include('whitespace'),
            # functions
            (r'((?:[a-zA-Z0-9_*\s])+?(?:\s|[*]))'    # return arguments
             r'([a-zA-Z_][a-zA-Z0-9_]*)'             # method name
             r'(\s*\([^;]*?\))'                      # signature
             r'(' + _ws + r')({)',
             bygroups(using(this), Name.Function, using(this), using(this),
                      Punctuation),
             'function'),
            # function declarations
            (r'((?:[a-zA-Z0-9_*\s])+?(?:\s|[*]))'    # return arguments
             r'([a-zA-Z_][a-zA-Z0-9_]*)'             # method name
             r'(\s*\([^;]*?\))'                      # signature
             r'(' + _ws + r')(;)',
             bygroups(using(this), Name.Function, using(this), using(this),
                      Punctuation)),
            ('', Text, 'statement'),
        ],
        'whitespace': [
            # preprocessor directives: without whitespace
            ('^#', Comment.Preproc, 'macro'),
            (r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*:(?!:))',
             bygroups(Text, Name.Label)),
            (r'\n', Text),
            (r'\s+', Text),
            (r'\\\n', Text), # line continuation
            (r'(//)(@)', bygroups(Comment.Single, Comment.Special),
                          'singlecontracts'),
            (r'//(\n|(.|\n)*?[^\\]\n)', Comment.Single),
            (r'//', Comment.Single),
            (r'(/\*)(@)', bygroups(Comment.Multiline, Comment.Special),
                          ('comments', 'contracts')),
            (r'/\*', Comment.Multiline, 'comments'),
        ],
        'contractkeys': [
          (r'(assert|requires|ensures|loop_invariant)', Comment.Special),
        ],
        'singlecontracts': [
            (r'(\w+)(\s+)([^@]+?)(\s*\n)',
             bygroups(using(this, state = 'contractkeys'),Text,using(this, state = 'statement'),Text), '#pop')
        ],
        'contracts': [
            (r'(\w+)(\s+)([^@]+?)(\s*)(@)',
             bygroups(using(this, state = 'contractkeys'),Text,using(this, state = 'statement'),Text,Comment.Special), '#pop'),
        ],
        'comments': [
            (r'[^*/]', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline),
        ],
        'statements': [
            (r'"', String, 'string'),
            (r"'(\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])'", String.Char),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'\d+', Number.Integer),
            (r'\*/', Error),
            (r'[~!%^&*+=|?:<>/-]', Operator),
            (r'[()\[\],.]', Punctuation),
            (r'(for|while|if|else|break|continue|'
             r'return|alloc_array|struct|typedef|while)\b', Keyword),
            (r'(\\result|\\length)\b', Keyword),
            (r'(void|int|char|bool|string|image_t|rand_t)\b', Keyword.Type),
            (r'(true|false|NULL)\b', Name.Builtin),
            ('[a-zA-Z_][a-zA-Z0-9_]*', Name),
        ],
        'statement' : [
            include('whitespace'),
            include('statements'),
            ('[{}]', Punctuation),
            (';', Punctuation, '#pop'),
        ],
        'function': [
            include('whitespace'),
            include('statements'),
            (';', Punctuation),
            ('{', Punctuation, '#push'),
            ('}', Punctuation, '#pop'),
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String), # all other characters
            (r'\\\n', String), # line continuation
            (r'\\', String), # stray backslash
        ],
        'macro': [
            (r'[^/\n]+', Comment.Preproc),
            (r'/[*](.|\n)*?[*]/', Comment.Multiline),
            (r'//.*?\n', Comment.Single, '#pop'),
            (r'/', Comment.Preproc),
            (r'(?<=\\)\n', Comment.Preproc),
            (r'\n', Comment.Preproc, '#pop'),
        ],
    }

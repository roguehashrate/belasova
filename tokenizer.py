import re

token_specification = [
    ('FN', r'fn'),
    ('COLON2', r'::'),
    ('ARROW2', r'->>'),
    ('ARROW', r'->'),
    ('EQUAL', r'='),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'\/'),
    ('PUTS', r'puts'),
    ('INT_TYPE', r'Int'),
    ('NUMBER', r'\d+'),
    ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('STRING', r'"[^"]*"'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.')
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex).match

def tokenize(code):
    pos = 0
    tokens = []
    while pos < len(code):
        m = get_token(code, pos)
        if m:
            kind = m.lastgroup
            value = m.group(kind)
            if kind == 'NEWLINE' or kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character: {value}')
            else:
                tokens.append((kind, value))
            pos = m.end()
        else:
            raise RuntimeError(f'Unexpected character at position {pos}')
    tokens.append(('EOF', ''))
    return tokens

import re

token_specification = [
    ('FN', r'fn'),
    ('LET', r'let'),
    ('IF', r'if'),
    ('THEN', r'then'),
    ('ELSE', r'else'),
    ('END', r'end'),
    ('CHECK', r'check'),    # Added 'check' keyword
    ('WHEN', r'when'),      # Added 'when' keyword
    ('COLON2', r'::'),
    ('ARROW2', r'->>'),
    ('ARROW', r'->'),
    ('EQEQ', r'=='),  # Added before EQUAL to ensure == is tokenized correctly
    ('ASSIGN_INPUT', r'<-'), # For Inputs
    ('CONCAT', r'\+\+'),
    ('EQUAL', r'='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
    ('COLON', r':'),
    ('PUTS', r'puts'),
    ('INT_TYPE', r'Int'),
    ('STRING_TYPE', r'String'),  # Added to support String type
    ('DOUBLE_TYPE', r'Double'),
    ('NUMBER', r'\d+(\.\d+)?'),
    ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('STRING', r'"[^"]*"'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('MISMATCH', r'.'),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex).match

def tokenize(code):
    lines = []
    for line in code.splitlines():
        if '--' in line:
            line = line.split('--')[0]
        lines.append(line)
    code = '\n'.join(lines)

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

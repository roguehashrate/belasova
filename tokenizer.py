import re

token_specification = [
    ('FN', r'fn'),
    ('LET', r'let'),
    ('IF', r'if'),
    ('ELSEIF', r'elseif'),
    ('ELSE', r'else'),
    ('THEN', r'then'),
    ('END', r'end'),
    ('CHECK', r'check'),
    ('WHEN', r'when'),
    ('NOT', r'not'),
    ('AND', r'and'),
    ('OR', r'or'),
    ('LOOP', r'loop'),
    ('TIMES', r'times'),
    ('UNTIL', r'until'),
    ('INFINITE', r'infinite'),
    ('BREAK', r'break'),
    ('CONTINUE', r'continue'),
    ('RETURN', r'return'),
    ('TRUE', r'true'),
    ('FALSE', r'false'),
    ('COLON2', r'::'),
    ('ARROW2', r'->>'),
    ('ARROW', r'->'),
    ('EQEQ', r'=='),
    ('NOTEQ', r'!=|<>'),
    ('LTE', r'<='),
    ('GTE', r'>='),
    ('LT', r'<'),
    ('GT', r'>'),
    ('ASSIGN_INPUT', r'<-'),
    ('ASSIGN', r'='),
    ('COMMENT', r'--.*'),
    ('CONCAT', r'\+\+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
    ('COLON', r':'),
    ('PUTS', r'puts'),
    ('INT_TYPE', r'Int'),
    ('STRING_TYPE', r'String'),
    ('DOUBLE_TYPE', r'Double'),
    ('BOOL_TYPE', r'Bool'),
    ('NUMBER', r'\d+(\.\d+)?'),
    ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('STRING', r'"[^"]*"'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('MISMATCH', r'.'),
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).match

def tokenize(code):
    pos = 0
    tokens = []
    line_num = 1
    
    while pos < len(code):
        m = get_token(code, pos)
        if m:
            kind = m.lastgroup
            value = m.group(kind)
            if kind in ('NEWLINE', 'SKIP', 'COMMENT'):
                if kind == 'NEWLINE':
                    line_num += 1
                pos = m.end()
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character: {value} at line {line_num}')
            else:
                tokens.append((kind, value, line_num))
            pos = m.end()
        else:
            raise RuntimeError(f'Unexpected character at position {pos}, line {line_num}')
    
    tokens.append(('EOF', '', line_num))
    return tokens
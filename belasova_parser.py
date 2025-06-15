from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '')

    def eat(self, kind):
        token = self.current()
        if token[0] == kind:
            self.pos += 1
            return token
        raise RuntimeError(f"Expected token {kind} but got {token}")

    def parse(self):
        ast = []
        while self.current()[0] != 'EOF':
            if self.current()[0] == 'FN':
                ast.append(self.parse_function_signature())
            elif self.current()[0] == 'LET':
                ast.append(self.parse_variable_assignment())
            elif self.current()[0] == 'PUTS':
                ast.append(self.parse_puts())
            elif self.current()[0] == 'IDENT':
                ast.append(self.parse_function_definition())
            else:
                raise RuntimeError(f"Unexpected token: {self.current()}")
        return ast

    def parse_function_signature(self):
        self.eat('FN')
        name = self.eat('IDENT')[1]
        self.eat('COLON2')
        param_types = []
        while True:
            tok = self.current()
            if tok[0] == 'INT_TYPE':
                param_types.append(tok[1])
                self.eat('INT_TYPE')
            else:
                raise RuntimeError(f"Expected type, got {tok}")
            if self.current()[0] == 'ARROW':
                self.eat('ARROW')
            elif self.current()[0] == 'ARROW2':
                self.eat('ARROW2')
                break
            else:
                raise RuntimeError(f"Expected arrow, got {self.current()}")
        return_type = self.eat('INT_TYPE')[1]
        return FunctionSignature(name, param_types, return_type)

    def parse_function_definition(self):
        name = self.eat('IDENT')[1]
        params = []
        while self.current()[0] == 'IDENT':
            params.append(self.eat('IDENT')[1])
        self.eat('EQUAL')
        body = self.parse_expression()
        return FunctionDefinition(name, params, body)

    def parse_variable_assignment(self):
        self.eat('LET')
        name = self.eat('IDENT')[1]
        type_annotation = None
        if self.current()[0] == 'COLON2':
            self.eat('COLON2')
            type_annotation = self.eat('INT_TYPE')[1]
        self.eat('EQUAL')
        value = self.parse_expression()
        return VariableAssignment(name, type_annotation, value)

    def parse_puts(self):
        self.eat('PUTS')
        expr = self.parse_expression()
        return PutsStatement(expr)

    def parse_expression(self):
        left = self.parse_term()
        while self.current()[0] in ('PLUS', 'MINUS'):
            op = self.eat(self.current()[0])[1]
            right = self.parse_term()
            left = BinaryOp(left, op, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current()[0] in ('MULTIPLY', 'DIVIDE'):
            op = self.eat(self.current()[0])[1]
            right = self.parse_factor()
            left = BinaryOp(left, op, right)
        return left

    def parse_factor(self):
        tok = self.current()
        if tok[0] == 'IDENT':
            name = self.eat('IDENT')[1]
            args = []
            while self.current()[0] in ('IDENT', 'NUMBER'):
                if self.current()[0] == 'IDENT':
                    args.append(Identifier(self.eat('IDENT')[1]))
                elif self.current()[0] == 'NUMBER':
                    args.append(int(self.eat('NUMBER')[1]))
            if args:
                return FunctionCall(name, args)
            else:
                return Identifier(name)
        elif tok[0] == 'NUMBER':
            return int(self.eat('NUMBER')[1])
        elif tok[0] == 'STRING':
            return self.eat('STRING')[1]
        else:
            raise RuntimeError(f"Unexpected token in factor: {tok}")

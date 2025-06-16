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
                ast.extend(self.parse_function())
            elif self.current()[0] == 'LET':
                ast.append(self.parse_variable_assignment())
            elif self.current()[0] == 'PUTS':
                ast.append(self.parse_puts())
            elif self.current()[0] == 'IF':
                ast.append(self.parse_if_chain())
            else:
                raise RuntimeError(f"Unexpected token: {self.current()}")
        return ast

    def parse_function(self):
        self.eat('FN')
        name = self.eat('IDENT')[1]
        self.eat('COLON2')
        param_types = []
        while self.current()[0] in ('INT_TYPE', 'STRING_TYPE'):
            param_types.append(self.eat(self.current()[0])[1])
            if self.current()[0] == 'ARROW':
                self.eat('ARROW')
            elif self.current()[0] == 'ARROW2':
                self.eat('ARROW2')
                break
            else:
                raise RuntimeError(f"Expected arrow, got {self.current()}")
        return_type = self.eat(self.current()[0])[1]  # Support both Int and String
        signature = FunctionSignature(name, param_types, return_type)
        
        # Parse function definition, excluding the function name from params
        self.eat('IDENT')  # Skip the function name (e.g., 'add')
        params = []
        while self.current()[0] == 'IDENT':
            params.append(self.eat('IDENT')[1])
        self.eat('EQUAL')
        body = self.parse_expression()
        definition = FunctionDefinition(name, params, body)
        return [signature, definition]

    def parse_variable_assignment(self):
        self.eat('LET')
        name = self.eat('IDENT')[1]
        type_annotation = None
        if self.current()[0] == 'COLON2':
            self.eat('COLON2')
            if self.current()[0] in ('INT_TYPE', 'STRING_TYPE', 'DOUBLE_TYPE'):
                type_annotation = self.eat(self.current()[0])[1]
            else:
                raise RuntimeError(f"Expected type, got {self.current()}")
        self.eat('EQUAL')
        value = self.parse_expression()
        return VariableAssignment(name, type_annotation, value)

    def parse_puts(self):
        self.eat('PUTS')
        expr = self.parse_expression()
        return PutsStatement(expr)

    def parse_if_chain(self):
        branches = []

        while self.current()[0] == 'IF':
            self.eat('IF')
            condition = self.parse_expression()
            self.eat('THEN')
            self.eat('COLON')

            then_block = []
            while self.current()[0] not in ('IF', 'ELSE', 'END', 'EOF'):
                if self.current()[0] == 'PUTS':
                    then_block.append(self.parse_puts())
                else:
                    raise RuntimeError(f"Unexpected token in then block: {self.current()}")

            branches.append((condition, then_block))

        else_block = []
        if self.current()[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('COLON')
            while self.current()[0] not in ('END', 'EOF'):
                if self.current()[0] == 'PUTS':
                    else_block.append(self.parse_puts())
                else:
                    raise RuntimeError(f"Unexpected token in else block: {self.current()}")

        if self.current()[0] == 'END':
            self.eat('END')
        else:
            raise RuntimeError(f"Expected 'END' token to close if-chain block but got {self.current()}")

        return IfChain(branches, else_block)


    def parse_expression(self):
        left = self.parse_term()
        while self.current()[0] in ('PLUS', 'MINUS', 'EQEQ'):
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
                    value_str = self.eat('NUMBER')[1]
                    if '.' in value_str:
                        args.append(float(value_str))
                    else:
                        args.append(int(value_str))
            if args:
                return FunctionCall(name, args)
            else:
                return Identifier(name)
        elif tok[0] == 'NUMBER':
            value_str = self.eat('NUMBER')[1]
            if '.' in value_str:
                return float(value_str)
            else:
                return int(value_str)
        elif tok[0] == 'STRING':
            return self.eat('STRING')[1]
        else:
            raise RuntimeError(f"Unexpected token in factor: {tok}")
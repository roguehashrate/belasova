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
            token_type = self.current()[0]
            if token_type == 'FN':
                ast.extend(self.parse_function())
            elif token_type == 'LET':
                ast.append(self.parse_variable_assignment())
            elif token_type == 'PUTS':
                ast.append(self.parse_puts())
            elif token_type == 'IF':
                ast.append(self.parse_if_chain())
            elif token_type == 'CHECK':
                ast.append(self.parse_check_statement())
            else:
                # Allow expression statements (e.g. function calls without let)
                ast.append(self.parse_expression())
        return ast

    def parse_function(self):
        self.eat('FN')
        name = self.eat('IDENT')[1]

        # Parse parameter names (identifiers)
        params = []
        while self.current()[0] == 'IDENT':
            params.append(self.eat('IDENT')[1])

        self.eat('COLON2')

        # Parse parameter types and return type
        param_types = []
        while True:
            tok = self.current()
            if tok[0] in ('INT_TYPE', 'STRING_TYPE', 'DOUBLE_TYPE'):
                param_types.append(self.eat(tok[0])[1])
                if self.current()[0] == 'ARROW':
                    self.eat('ARROW')
                elif self.current()[0] == 'ARROW2':
                    self.eat('ARROW2')
                    break
                else:
                    raise RuntimeError(f"Expected '->' or '->>' after type, got {self.current()}")
            else:
                raise RuntimeError(f"Expected type token, got {tok}")

        # Explicitly require return type token here:
        if self.current()[0] not in ('INT_TYPE', 'STRING_TYPE', 'DOUBLE_TYPE'):
            raise RuntimeError(f"Expected return type token, got {self.current()}")
        return_type = self.eat(self.current()[0])[1]

        signature = FunctionSignature(name, param_types, return_type)

        # Parse function definition line: function name and params again
        def_name = self.eat('IDENT')[1]
        if def_name != name:
            raise RuntimeError(f"Function name mismatch: expected {name} but got {def_name}")

        def_params = []
        while self.current()[0] == 'IDENT':
            def_params.append(self.eat('IDENT')[1])

        self.eat('EQUAL')

        body = self.parse_block()
        definition = FunctionDefinition(name, def_params, body)

        return [signature, definition]

    def parse_block(self):
        stmts = []
        while self.current()[0] not in ('END', 'EOF'):
            tok = self.current()
            if tok[0] == 'PUTS':
                stmts.append(self.parse_puts())
            elif tok[0] == 'LET':
                stmts.append(self.parse_variable_assignment())
            elif tok[0] == 'IF':
                stmts.append(self.parse_if_chain())
            elif tok[0] == 'CHECK':
                stmts.append(self.parse_check_statement())
            else:
                # Allow expressions as statements inside blocks (e.g. function calls)
                stmts.append(self.parse_expression())
        self.eat('END')
        return stmts

    def parse_variable_assignment(self):
        self.eat('LET')
        name = self.eat('IDENT')[1]

        type_annotation = None
        if self.current()[0] == 'COLON2':
            self.eat('COLON2')
            if self.current()[0] in ('INT_TYPE', 'STRING_TYPE', 'DOUBLE_TYPE'):
                type_annotation = self.eat(self.current()[0])[1]
            else:
                raise RuntimeError(f"Expected type token after '::', got {self.current()}")

        if self.current()[0] == 'EQUAL':
            self.eat('EQUAL')
            value = self.parse_expression()
        elif self.current()[0] == 'ASSIGN_INPUT':
            self.eat('ASSIGN_INPUT')
            if self.current()[0] == 'IDENT' and self.current()[1] == 'getLine':
                self.eat('IDENT')
                value = InputCall()
            else:
                raise RuntimeError(f"Expected 'getLine' after '<-', got {self.current()}")
        else:
            raise RuntimeError(f"Expected '=' or '<-' after let statement, got {self.current()}")

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
            while self.current()[0] not in ('ELSE', 'END', 'EOF'):
                tok = self.current()
                if tok[0] == 'PUTS':
                    then_block.append(self.parse_puts())
                elif tok[0] == 'LET':
                    then_block.append(self.parse_variable_assignment())
                elif tok[0] == 'IF':
                    then_block.append(self.parse_if_chain())
                elif tok[0] == 'CHECK':
                    then_block.append(self.parse_check_statement())
                else:
                    then_block.append(self.parse_expression())

            branches.append((condition, then_block))

        else_block = []
        if self.current()[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('COLON')
            while self.current()[0] not in ('END', 'EOF'):
                tok = self.current()
                if tok[0] == 'PUTS':
                    else_block.append(self.parse_puts())
                elif tok[0] == 'LET':
                    else_block.append(self.parse_variable_assignment())
                elif tok[0] == 'IF':
                    else_block.append(self.parse_if_chain())
                elif tok[0] == 'CHECK':
                    else_block.append(self.parse_check_statement())
                else:
                    else_block.append(self.parse_expression())

        self.eat('END')
        return IfChain(branches, else_block)

    def parse_check_statement(self):
        self.eat('CHECK')
        subject_expr = self.parse_expression()
        self.eat('COLON')

        when_branches = []
        while self.current()[0] == 'WHEN':
            self.eat('WHEN')
            pattern_expr = self.parse_expression()
            self.eat('COLON')

            exprs = []
            while self.current()[0] not in ('WHEN', 'ELSE', 'END', 'EOF'):
                tok = self.current()
                if tok[0] == 'PUTS':
                    exprs.append(self.parse_puts())
                elif tok[0] == 'LET':
                    exprs.append(self.parse_variable_assignment())
                elif tok[0] == 'IF':
                    exprs.append(self.parse_if_chain())
                elif tok[0] == 'CHECK':
                    exprs.append(self.parse_check_statement())
                else:
                    exprs.append(self.parse_expression())

            when_branches.append((pattern_expr, exprs))

        else_block = None
        if self.current()[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('COLON')
            else_block = []
            while self.current()[0] not in ('END', 'EOF'):
                tok = self.current()
                if tok[0] == 'PUTS':
                    else_block.append(self.parse_puts())
                elif tok[0] == 'LET':
                    else_block.append(self.parse_variable_assignment())
                elif tok[0] == 'IF':
                    else_block.append(self.parse_if_chain())
                elif tok[0] == 'CHECK':
                    else_block.append(self.parse_check_statement())
                else:
                    else_block.append(self.parse_expression())

        self.eat('END')
        return CheckStatement(subject_expr, when_branches, else_block)

    def parse_primary(self):
        tok = self.current()
        if tok[0] == 'IDENT':
            name = self.eat('IDENT')[1]
            return Identifier(name)
        elif tok[0] == 'NUMBER':
            value_str = self.eat('NUMBER')[1]
            if '.' in value_str:
                return NumberLiteral(float(value_str))
            else:
                return NumberLiteral(int(value_str))
        elif tok[0] == 'STRING':
            value = self.eat('STRING')[1]
            return StringLiteral(value)
        elif tok[0] == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expression()
            self.eat('RPAREN')
            return expr
        else:
            raise RuntimeError(f"Unexpected token in primary: {tok}")

    def parse_factor(self):
        expr = self.parse_primary()

        # Check if this is a function call: identifier followed by zero or more args
        if isinstance(expr, Identifier):
            args = []
            # Only accept valid primary tokens as args
            while self.current()[0] in ('IDENT', 'NUMBER', 'STRING', 'LPAREN'):
                arg = self.parse_primary()
                args.append(arg)
            if args:
                return FunctionCall(expr.name, args)

        return expr

    def parse_term(self):
        left = self.parse_factor()
        while self.current()[0] in ('MULTIPLY', 'DIVIDE'):
            op = self.eat(self.current()[0])[1]
            right = self.parse_factor()
            left = BinaryOp(left, op, right)
        return left

    def parse_expression(self):
        left = self.parse_term()
        while self.current()[0] in ('PLUS', 'MINUS', 'EQEQ', 'CONCAT'):
            op_token = self.eat(self.current()[0])
            op = op_token[1]
            right = self.parse_term()
            left = BinaryOp(left, op, right)
        return left

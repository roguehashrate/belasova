from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '', -1)
    
    def peek_next_token(self):
        next_index = self.pos + 1
        if next_index < len(self.tokens):
            return self.tokens[next_index]
        else:
            return ('EOF', '', -1)

    def eat(self, kind):
        token = self.current()
        if token[0] == kind:
            self.pos += 1
            return token
        line_info = f" at line {token[2]}" if len(token) > 2 else ""
        raise RuntimeError(f"Expected token {kind} but got {token[0]}{line_info}")

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
            elif token_type == 'LOOP':
                ast.append(self.parse_loop())
            elif token_type == 'RETURN':
                ast.append(self.parse_return())
            elif token_type == 'BREAK':
                self.eat('BREAK')
                ast.append(BreakStatement())
            elif token_type == 'CONTINUE':
                self.eat('CONTINUE')
                ast.append(ContinueStatement())
            else:
                ast.append(self.parse_expression())
        return ast

    def parse_function(self):
        self.eat('FN')
        name = self.eat('IDENT')[1]

        # Parse parameter names
        params = []
        while self.current()[0] == 'IDENT':
            params.append(self.eat('IDENT')[1])

        self.eat('COLON2')

        # Parse parameter types and return type
        param_types = []
        while True:
            tok = self.current()
            if tok[0] in ('INT_TYPE', 'STRING_TYPE', 'DOUBLE_TYPE', 'BOOL_TYPE'):
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

        # Return type
        if self.current()[0] not in ('INT_TYPE', 'STRING_TYPE', 'DOUBLE_TYPE', 'BOOL_TYPE'):
            raise RuntimeError(f"Expected return type token, got {self.current()}")
        return_type = self.eat(self.current()[0])[1]

        # Validate parameter count matches
        if len(params) != len(param_types):
            raise RuntimeError(f"Parameter count mismatch in function {name}: {len(params)} names vs {len(param_types)} types")

        signature = FunctionSignature(name, param_types, return_type)

        # Parse function definition line: name and params again
        def_name = self.eat('IDENT')[1]
        if def_name != name:
            raise RuntimeError(f"Function name mismatch: expected {name} but got {def_name}")

        def_params = []
        while self.current()[0] == 'IDENT':
            def_params.append(self.eat('IDENT')[1])

        # Validate parameter names match
        if params != def_params:
            raise RuntimeError(f"Parameter names don't match between signature and definition in function {name}")

        self.eat('ASSIGN')

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
            elif tok[0] == 'LOOP':
                stmts.append(self.parse_loop())
            elif tok[0] == 'RETURN':
                stmts.append(self.parse_return())
            elif tok[0] == 'BREAK':
                self.eat('BREAK')
                stmts.append(BreakStatement())
            elif tok[0] == 'CONTINUE':
                self.eat('CONTINUE')
                stmts.append(ContinueStatement())
            else:
                stmts.append(self.parse_expression())
        self.eat('END')
        return stmts

    def parse_loop(self):
        self.eat('LOOP')
        
        if self.current()[0] == 'INFINITE':
            self.eat('INFINITE')
            self.eat('COLON')
            body = []
            while self.current()[0] not in ('END', 'EOF'):
                body.append(self.parse_statement())
            self.eat('END')
            return LoopNode('infinite', None, body)
        
        elif self.current()[0] == 'UNTIL':
            self.eat('UNTIL')  # eat UNTIL token correctly
            condition = self.parse_expression()
            self.eat('COLON')
            body = []
            while self.current()[0] not in ('END', 'EOF'):
                body.append(self.parse_statement())
            self.eat('END')
            return LoopNode('until', condition, body)
        
        else:
            count_expr = self.parse_expression()
            self.eat('TIMES')
            self.eat('COLON')
            body = []
            while self.current()[0] not in ('END', 'EOF'):
                body.append(self.parse_statement())
            self.eat('END')
            return LoopNode('times', count_expr, body)


    def parse_statement(self):
        tok = self.current()
        if tok[0] == 'PUTS':
            return self.parse_puts()
        elif tok[0] == 'LET':
            return self.parse_variable_assignment()
        elif tok[0] == 'IF':
            return self.parse_if_chain()
        elif tok[0] == 'CHECK':
            return self.parse_check_statement()
        elif tok[0] == 'LOOP':
            return self.parse_loop()
        elif tok[0] == 'RETURN':
            return self.parse_return()
        elif tok[0] == 'BREAK':
            self.eat('BREAK')
            return BreakStatement()
        elif tok[0] == 'CONTINUE':
            self.eat('CONTINUE')
            return ContinueStatement()
        else:
            return self.parse_expression()

    def parse_return(self):
        self.eat('RETURN')
        expr = self.parse_expression()
        return ReturnStatement(expr)

    def parse_variable_assignment(self):
        self.eat('LET')
        name = self.eat('IDENT')[1]

        type_annotation = None
        if self.current()[0] == 'COLON2':
            self.eat('COLON2')
            if self.current()[0] in ('INT_TYPE', 'STRING_TYPE', 'DOUBLE_TYPE', 'BOOL_TYPE'):
                type_annotation = self.eat(self.current()[0])[1]
            else:
                raise RuntimeError(f"Expected type token after '::', got {self.current()}")

        # Check for '=' or '<-'
        if self.current()[0] == 'ASSIGN':
            self.eat('ASSIGN')
        elif self.current()[0] == 'LT' and self.peek_next_token()[0] == 'MINUS':
            self.eat('LT')
            self.eat('MINUS')
        else:
            raise RuntimeError(f"Expected assignment operator after let statement, got {self.current()}")

        # Now parse the value
        if self.current()[0] == 'IDENT' and self.current()[1] == 'getLine':
            self.eat('IDENT')
            value = InputCall()
        else:
            value = self.parse_expression()

        return VariableAssignment(name, value, type_annotation, is_declaration=True)

    def parse_puts(self):
        self.eat('PUTS')
        expr = self.parse_expression()
        return PutsStatement(expr)

    def parse_if_chain(self):
        branches = []

        # Handle first if
        self.eat('IF')
        condition = self.parse_expression()
        self.eat('THEN')
        self.eat('COLON')

        then_block = []
        while self.current()[0] not in ('ELSEIF', 'ELSE', 'END', 'EOF'):
            then_block.append(self.parse_statement())

        branches.append((condition, then_block))

        # Handle elseif branches
        while self.current()[0] == 'ELSEIF':
            self.eat('ELSEIF')
            condition = self.parse_expression()
            self.eat('THEN')
            self.eat('COLON')
            
            then_block = []
            while self.current()[0] not in ('ELSEIF', 'ELSE', 'END', 'EOF'):
                then_block.append(self.parse_statement())
            
            branches.append((condition, then_block))

        # Handle else
        else_block = []
        if self.current()[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('COLON')
            while self.current()[0] not in ('END', 'EOF'):
                else_block.append(self.parse_statement())

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
                exprs.append(self.parse_statement())

            when_branches.append((pattern_expr, exprs))

        else_block = None
        if self.current()[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('COLON')
            else_block = []
            while self.current()[0] not in ('END', 'EOF'):
                else_block.append(self.parse_statement())

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
        elif tok[0] == 'TRUE':
            self.eat('TRUE')
            return BooleanLiteral(True)
        elif tok[0] == 'FALSE':
            self.eat('FALSE')
            return BooleanLiteral(False)
        elif tok[0] == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expression()
            self.eat('RPAREN')
            return expr
        else:
            raise RuntimeError(f"Unexpected token in primary: {tok}")

    def parse_factor(self):
        # For unary NOT support
        if self.current()[0] == 'NOT':
            self.eat('NOT')
            expr = self.parse_factor()
            return UnaryOp('not', expr)

        expr = self.parse_primary()

        # Function call: identifier followed by zero or more args
        if isinstance(expr, Identifier):
            args = []
            while self.current()[0] in ('IDENT', 'NUMBER', 'STRING', 'TRUE', 'FALSE', 'LPAREN'):
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

    def parse_arithmetic_expr(self):
        left = self.parse_term()
        while self.current()[0] in ('PLUS', 'MINUS', 'CONCAT'):
            op = self.eat(self.current()[0])[1]
            right = self.parse_term()
            left = BinaryOp(left, op, right)
        return left

    def parse_comparison_expr(self):
        left = self.parse_arithmetic_expr()
        while self.current()[0] in ('EQEQ', 'NOTEQ', 'LT', 'GT', 'LTE', 'GTE'):
            op = self.eat(self.current()[0])[1]
            right = self.parse_arithmetic_expr()
            left = BinaryOp(left, op, right)
        return left

    def parse_logical_expr(self):
        left = self.parse_comparison_expr()
        while self.current()[0] in ('AND', 'OR'):
            op = self.eat(self.current()[0])[1]
            right = self.parse_comparison_expr()
            left = BinaryOp(left, op, right)
        return left

    def parse_expression(self):
        # Logical expressions are top level
        return self.parse_logical_expr()
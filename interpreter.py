# interpreter.py
from ast_nodes import *

class Environment:
    def __init__(self):
        self.functions = {}
        self.variables = {}

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.env = Environment()

    def interpret(self):
        for node in self.ast:
            if isinstance(node, list):
                for subnode in node:
                    self.eval_node(subnode)
            else:
                self.eval_node(node)

    def eval_node(self, node):
        if isinstance(node, NumberLiteral):
            return node.value
        elif isinstance(node, StringLiteral):
            return node.value.strip('"')
        elif isinstance(node, BooleanLiteral):
            return node.value
        elif isinstance(node, PutsStatement):
            result = self.eval_node(node.expr)
            print(result)
            return None
        elif isinstance(node, FunctionSignature):
            # Signatures are metadata; ignore at runtime
            return None
        elif isinstance(node, FunctionDefinition):
            self.env.functions[node.name] = node
            return None
        elif isinstance(node, VariableAssignment):
            value = self.eval_node(node.value)
            if node.is_declaration:
                # Cast to type if annotation given
                if node.type_annotation == 'Int':
                    value = int(value)
                elif node.type_annotation == 'Double':
                    value = float(value)
                self.env.variables[node.name] = value
                return value
            else:
                if node.name not in self.env.variables:
                    raise RuntimeError(f"Variable '{node.name}' used before declaration")
                self.env.variables[node.name] = value
                return value
        elif isinstance(node, Identifier):
            if node.name in self.env.variables:
                return self.env.variables[node.name]
            else:
                raise RuntimeError(f"Variable '{node.name}' used before declaration")
        elif isinstance(node, IfElseStatement):
            condition = self.eval_node(node.condition)
            if condition:
                for stmt in node.then_block:
                    self.eval_node(stmt)
            else:
                for stmt in node.else_block:
                    self.eval_node(stmt)
            return None
        elif isinstance(node, IfChain):
            for condition, then_block in node.branches:
                if self.eval_node(condition):
                    for stmt in then_block:
                        self.eval_node(stmt)
                    return None
            for stmt in node.else_block:
                self.eval_node(stmt)
            return None
        elif isinstance(node, CheckStatement):
            subject = self.eval_node(node.subject_expr)
            for pattern_expr, block in node.when_branches:
                if subject == self.eval_node(pattern_expr):
                    for stmt in block:
                        self.eval_node(stmt)
                    return None
            if node.else_block:
                for stmt in node.else_block:
                    self.eval_node(stmt)
            return None
        elif isinstance(node, LoopNode):
            if node.loop_type == 'infinite':
                while True:
                    for stmt in node.body:
                        self.eval_node(stmt)
            elif node.loop_type == 'times':
                count = int(self.eval_node(node.condition_or_count))
                for _ in range(count):
                    for stmt in node.body:
                        self.eval_node(stmt)
            elif node.loop_type == 'until':
                while not self.eval_node(node.condition_or_count):
                    for stmt in node.body:
                        self.eval_node(stmt)
            return None
        elif isinstance(node, UnaryOp):
            val = self.eval_node(node.expr)
            if node.op == 'not':
                return not val
            else:
                raise RuntimeError(f"Unsupported unary operator: {node.op}")
        elif isinstance(node, BinaryOp):
            left = self.eval_node(node.left)
            right = self.eval_node(node.right)
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                if right == 0:
                    raise RuntimeError("Division by zero")
                return left / right
            elif node.op == '==':
                return left == right
            elif node.op in ('!=', 'not='):
                return left != right
            elif node.op == '<':
                return left < right
            elif node.op == '>':
                return left > right
            elif node.op == '<=':
                return left <= right
            elif node.op == '>=':
                return left >= right
            elif node.op == '++':
                return str(left) + str(right)
            else:
                raise RuntimeError(f"Unsupported operator: {node.op}")
        elif isinstance(node, FunctionCall):
            args = [self.eval_node(arg) for arg in node.args]
            return self.call_function(node.name, args)
        elif isinstance(node, InputCall):
            return input()
        elif isinstance(node, int):
            return node
        elif isinstance(node, float):
            return node
        elif isinstance(node, str):
            return node
        else:
            raise RuntimeError(f"Unknown AST node: {node}")

    def call_function(self, name, args):
        if name == 'toInt':
            if len(args) != 1:
                raise RuntimeError("toInt expects exactly 1 argument")
            try:
                return int(args[0])
            except Exception as e:
                raise RuntimeError(f"toInt conversion error: {e}")
        if name == 'toDouble':
            if len(args) != 1:
                raise RuntimeError("toDouble expects exactly 1 argument")
            try:
                return float(args[0])
            except Exception as e:
                raise RuntimeError(f"toDouble conversion error: {e}")
        if name not in self.env.functions:
            raise RuntimeError(f"Function not found: {name}")
        func = self.env.functions[name]
        if len(args) != len(func.params):
            raise RuntimeError(f"Argument count mismatch for {name}")
        local_env = dict(zip(func.params, args))
        return self.eval_function_body_sequence(func.body, local_env)

    def eval_function_body(self, node, local_env):
        if isinstance(node, NumberLiteral):
            return node.value
        elif isinstance(node, StringLiteral):
            return node.value.strip('"')
        elif isinstance(node, VariableAssignment):
            value = self.eval_function_body(node.value, local_env)
            if node.type_annotation == 'Int':
                value = int(value)
            elif node.type_annotation == 'Double':
                value = float(value)
            local_env[node.name] = value
            return value
        elif isinstance(node, BinaryOp):
            left = self.eval_function_body(node.left, local_env)
            right = self.eval_function_body(node.right, local_env)
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                if right == 0:
                    raise RuntimeError("Division by zero")
                return left / right
            elif node.op == '==':
                return left == right
            elif node.op in ('!=', 'not='):
                return left != right
            elif node.op == '<':
                return left < right
            elif node.op == '>':
                return left > right
            elif node.op == '<=':
                return left <= right
            elif node.op == '>=':
                return left >= right
            elif node.op == '++':
                return str(left) + str(right)
            else:
                raise RuntimeError(f"Unsupported operator: {node.op}")
        elif isinstance(node, UnaryOp):
            val = self.eval_function_body(node.expr, local_env)
            if node.op == 'not':
                return not val
            else:
                raise RuntimeError(f"Unsupported unary operator: {node.op}")
        elif isinstance(node, CheckStatement):
            subject = self.eval_function_body(node.subject_expr, local_env)
            for pattern_expr, block in node.when_branches:
                if subject == self.eval_function_body(pattern_expr, local_env):
                    self.eval_function_body_sequence(block, local_env)
                    return None
            if node.else_block:
                self.eval_function_body_sequence(node.else_block, local_env)
                return None
        elif isinstance(node, InputCall):
            return input()
        elif isinstance(node, Identifier):
            if node.name in local_env:
                return local_env[node.name]
            elif node.name in self.env.variables:
                return self.env.variables[node.name]
            else:
                raise RuntimeError(f"Unknown identifier: {node.name}")
        elif isinstance(node, FunctionCall):
            args = [self.eval_function_body(arg, local_env) for arg in node.args]
            return self.call_function(node.name, args)
        elif isinstance(node, PutsStatement):
            result = self.eval_function_body(node.expr, local_env)
            print(result)
            return None
        elif isinstance(node, int):
            return node
        elif isinstance(node, float):
            return node
        elif isinstance(node, str):
            return node
        else:
            raise RuntimeError(f"Unsupported node in function body: {node}")

    def eval_function_body_sequence(self, stmts, local_env):
        result = None
        for stmt in stmts:
            result = self.eval_function_body(stmt, local_env)
        return result

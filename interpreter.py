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
        elif isinstance(node, PutsStatement):
            result = self.eval_node(node.expr)
            print(result)
        elif isinstance(node, FunctionSignature):
            pass
        elif isinstance(node, FunctionDefinition):
            self.env.functions[node.name] = node
        elif isinstance(node, VariableAssignment):
            value = self.eval_node(node.value)
            self.env.variables[node.name] = value
        elif isinstance(node, IfElseStatement):
            condition = self.eval_node(node.condition)
            if condition:
                for stmt in node.then_block:
                    self.eval_node(stmt)
            else:
                for stmt in node.else_block:
                    self.eval_node(stmt)

        elif isinstance(node, IfChain):
            for condition, then_block in node.branches:
                cond_value = self.eval_node(condition)
                if cond_value:
                    for stmt in then_block:
                        self.eval_node(stmt)
                    return
            for stmt in node.else_block:
                self.eval_node(stmt)
                
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
            else:
                raise RuntimeError(f"Unsupported operator: {node.op}")
        elif isinstance(node, FunctionCall):
            arg_values = [self.eval_node(arg) for arg in node.args]
            return self.call_function(node.name, arg_values)
        elif isinstance(node, Identifier):
            if node.name in self.env.variables:
                return self.env.variables[node.name]
            else:
                raise RuntimeError(f"Unknown identifier: {node.name}")
        elif isinstance(node, int):
            return node
        elif isinstance(node, float):
            return node
        elif isinstance(node, str):
            return node.strip('"')
        else:
            raise RuntimeError(f"Unknown AST node: {node}")

    def call_function(self, name, args):
        if name not in self.env.functions:
            raise RuntimeError(f"Function not found: {name}")
        func = self.env.functions[name]
        if len(args) != len(func.params):
            raise RuntimeError(f"Argument count mismatch for {name}")

        local_env = dict(zip(func.params, args))
        return self.eval_function_body(func.body, local_env)

    def eval_function_body(self, node, local_env):
        if isinstance(node, NumberLiteral):
            return node.value
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
            else:
                raise RuntimeError(f"Unsupported operator: {node.op}")
        elif isinstance(node, Identifier):
            if node.name in local_env:
                return local_env[node.name]
            elif node.name in self.env.variables:
                return self.env.variables[node.name]
            else:
                raise RuntimeError(f"Unknown identifier: {node.name}")
        elif isinstance(node, int):
            return node
        elif isinstance(node, str):
            return node.strip('"')
        else:
            raise RuntimeError(f"Unsupported node in function body: {node}")

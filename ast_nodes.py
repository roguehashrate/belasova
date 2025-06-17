class NumberLiteral:
    def __init__(self, value):
        self.value = value

class StringLiteral:
    def __init__(self, value):
        self.value = value

class BooleanLiteral:
    def __init__(self, value):
        self.value = value

class Identifier:
    def __init__(self, name):
        self.name = name

class InputCall:
    def __init__(self):
        pass

class PutsStatement:
    def __init__(self, expr):
        self.expr = expr

class FunctionSignature:
    def __init__(self, name, param_types, return_type):
        self.name = name
        self.param_types = param_types
        self.return_type = return_type

class FunctionDefinition:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ReturnStatement:
    def __init__(self, expr):
        self.expr = expr

class VariableAssignment:
    def __init__(self, name, value, type_annotation=None, is_declaration=False):
        self.name = name
        self.value = value
        self.type_annotation = type_annotation
        self.is_declaration = is_declaration

class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class IfElseStatement:
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class IfChain:
    def __init__(self, branches, else_block):
        self.branches = branches
        self.else_block = else_block

class CheckStatement:
    def __init__(self, subject_expr, when_branches, else_block=None):
        self.subject_expr = subject_expr
        self.when_branches = when_branches
        self.else_block = else_block

class LoopNode:
    def __init__(self, loop_type, condition_or_count, body):
        self.loop_type = loop_type  # 'infinite', 'times', or 'until'
        self.condition_or_count = condition_or_count
        self.body = body

class BreakStatement:
    def __init__(self):
        pass

class ContinueStatement:
    def __init__(self):
        pass
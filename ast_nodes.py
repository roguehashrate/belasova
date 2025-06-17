class FunctionSignature:
    def __init__(self, name, param_types, return_type):
        self.name = name
        self.param_types = param_types
        self.return_type = return_type

    def __repr__(self):
        return f"FunctionSignature({self.name}, {self.param_types} ->> {self.return_type})"

class FunctionDefinition:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDefinition({self.name} {self.params} = {self.body})"

class PutsStatement:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Puts({self.expr})"

class IfElseStatement:
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self):
        return f"IfElse({self.condition}, then={self.then_block}, else={self.else_block})"

class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"

class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall({self.name} {self.args})"

class Identifier:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

class VariableAssignment:
    def __init__(self, name, type_annotation, value):
        self.name = name
        self.type_annotation = type_annotation
        self.value = value

    def __repr__(self):
        return f"VariableAssignment({self.name}, {self.type_annotation}, {self.value})"

class NumberLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberLiteral({self.value})"

class StringLiteral:
    def __init__(self, value):
        # Automatically strip surrounding double quotes if present
        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
            self.value = value[1:-1]
        else:
            self.value = value

    def __repr__(self):
        return f"StringLiteral({self.value})"

class IfChain:
    def __init__(self, branches, else_block):
        self.branches = branches
        self.else_block = else_block

    def __repr__(self):
        return f"IfChain({self.branches}, else={self.else_block})"

class InputCall:
    def __init__(self):
        pass

    def __repr__(self):
        return "InputCall()"

class CheckStatement:
    def __init__(self, subject_expr, when_branches, else_block):
        self.subject_expr = subject_expr        # Expression to match on
        self.when_branches = when_branches      # List of tuples (pattern_expr, [statements])
        self.else_block = else_block            # List of statements or None

    def __repr__(self):
        return f"CheckStatement({self.subject_expr}, when_branches={self.when_branches}, else_block={self.else_block})"

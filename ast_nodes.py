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

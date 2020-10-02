class Program:
    def __init__(self):
        self.statements = []

    def __repr__(self):
        string = ""
        for statement in self.statements:
            string += f" [ {statement} ] "
        return string

class Block:
    def __init__(self):
        self.statements = []

    def __repr__(self):
        string = ""
        for statement in self.statements:
            string += f" [ {statement} ] "
        return string

class AssignNode:
    def __init__(self, type, var_name, var_value, position_start, position_end):
        self.type = type
        self.var_name = var_name
        self.var_value = var_value
    
    def __repr__(self):
        return f"( VAR {self.var_name} = {self.var_value} )"

class NumberNode:
    def __init__(self, tok, position_start, position_end):
        self.tok = tok
        self.position_start = position_start
        self.position_end = position_end

    def get_c_code(self):
        return f"{self.tok.value}"

    def __repr__(self):
        return f"{self.tok}"

class StringNode:
    def __init__(self, tok, position_start, position_end):
        self.tok = tok
        self.position_start = position_start
        self.position_end = position_end

    def __repr__(self):
        return f"{self.tok}"

class IdentifierNode:
    def __init__(self, tok, position_start, position_end):
        self.tok = tok
        self.position_start = position_start
        self.position_end = position_end

    def __repr__(self):
        return f"{self.tok}"

class BinaryOperationNode:
    def __init__(self, left_node, operation_tok, right_node, position_start, position_end):
        self.left_node = left_node
        self.operation_tok = operation_tok
        self.right_node = right_node

        self.position_start = position_start
        self.position_end = position_end

    def __repr__(self):
        return f"({self.left_node} {self.operation_tok} {self.right_node})"


class UnaryOperationNode:
    def __init__(self, operation_tok, node, position_start, position_end):
        self.operation_tok = operation_tok
        self.node = node

        self.position_start = position_start
        self.position_end = position_end

    def __repr__(self):
        return f"({self.operation_tok} {self.node})"

class WriteNode:
    def __init__(self, args, position_start, position_end):
        self.args = args
        self.position_start = position_start
        self.position_end = position_end
    
    def __repr__(self):
        return f"scrie {self.args}"

class ReadNode:
    def __init__(self, args, position_start, position_end):
        self.args = args
        self.position_start = position_start
        self.position_end = position_end
    
    def __repr__(self):
        return f"citeste {self.args}"

class DeclarationNode:
    def __init__(self, elements, types, position_start, position_end):
        self.elements = elements
        self.types = types
        self.position_start = position_start
        self.position_end = position_end

    def __repr__(self):
        return f"Declarations {self.elements}"

class IntCastNode:
    def __init__(self, node):
        self.node = node
    
    def __repr__(self):
        return f"[{self.node}]"

class IfNode:
    def __init__(self, if_cond, if_block, else_block, position_start, position_end):
        self.if_cond = if_cond
        self.if_block = if_block
        self.else_block = else_block

        self.position_start = position_start
        self.position_end = position_end
    
    def __repr__(self):
        return f"IF {self.if_cond} THEN {self.if_block} ALTFEL {self.else_block}"
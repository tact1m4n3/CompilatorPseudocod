from token_ import *

three_address_codes = []

BinOp = "BinOp"
UnaryOp = "UnaryOp"

registers = []

class ThreeAddressCode:
    def __init__(self, type, op, arg1, arg2, result, label=None):
        self.type = type
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
        self.label = label
    
    def __repr__(self):
        return f"[type: {self.type}, op: {self.op}, arg1: {self.arg1}, arg2: {self.arg2}, result: {self.result}]"

class Compiler:
    constants = {}
    uninitialize_temporary_vars = {}
    variables = {}
    next_constant = 0

    def visit(self, node):
        func = getattr(self, "visit_" + type(node).__name__, self.no_visit_method)
        return func(node)
    
    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method declared!")

    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)
        
        print(three_address_codes, self.constants, self.uninitialize_temporary_vars)
    
    def visit_NumberNode(self, node):
        name = "INT_" + str(self.next_constant)
        self.constants[name] = node.tok
        self.next_constant += 1
        return name
    
    def visit_BinaryOperationNode(self, node):
        left_addr = self.visit(node.left_node)
        right_addr = self.visit(node.right_node)

        if node.left_node.tok.type == INT and node.right_node.tok.type == INT:  
            res_addr = self.create_uninitialize_temp(INT)

        tac = ThreeAddressCode(BinOp, node.operation_tok, left_addr, right_addr, res_addr)
        three_address_codes.append(tac)

        return res_addr
    
    def visit_UnaryOperationNode(self, node):
        right_addr = self.visit(node.node)

        if node.node.tok.type == INT:
            res_addr = self.create_uninitialize_temp(INT)
        
        tac = ThreeAddressCode(UnaryOp, node.operation_tok, right_addr, None, res_addr)
        three_address_codes.append(tac)

        return res_addr
    
    def visit_DeclarationNode(self, node):
        for i in range(len(node.elements)):
            self.create_variable(node.elements[i].tok.value, node.types[i].tok.value, None)
    
    def create_variable(self, name, type_, value):
        self.variables[name] = (type_, value)

        return name

    def create_uninitialize_temp(self, type_):
        name = "INT_" + str(self.next_constant)

        self.uninitialize_temporary_vars[name] = type_

        self.next_constant += 1

        return name
        
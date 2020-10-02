from token_ import *
from ast import IfNode
from errors import RTError

class Compiler:
    main = ""

    def visit(self, node):
        func = getattr(self, "visit_" + type(node).__name__, self.no_visit_method)
        code, error = func(node)
        return code, error
    
    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method declared!")

    def visit_Program(self, node):
        for stmt in node.statements:
            code, error = self.visit(stmt)
        
            if error:
                return None, error

            self.main += code
            if not isinstance(stmt, IfNode):
                self.main += ";"
            self.main += "\n"
        
        return """#include <iostream>
using namespace std;

int main() {
""" + self.main + "}", None

    def visit_NumberNode(self, node):
        return str(node.tok.value), None
    
    def visit_IdentifierNode(self, node):
        return node.tok.value, None
    
    def visit_StringNode(self, node):
        return "\"" + node.tok.value + "\"", None
    
    def visit_UnaryOperationNode(self, node):
        value_code, error = self.visit(node.node)
        if error:
            return None, error
        
        if node.operation_tok.type == PLUS:
            code = "+" + value_code
        elif node.operation_tok.type == MINUS:
            code = "-" + value_code
        elif node.operation_tok.matches(KEYWORD, "nu"):
            code = "!" + value_code
        else:
            return None, RTError("Unary operator of type {} is unhandled!".format(node.operation_tok.type), node.position_start, node.position_end)
        
        return "(" + code + ")", None
    
    def visit_BinaryOperationNode(self, node):
        left_code, error = self.visit(node.left_node)
        if error:
            return None, error

        right_code, error = self.visit(node.right_node)
        if error:
            return None, error

        if node.operation_tok.type == PLUS:
            code = left_code + "+" + right_code
        elif node.operation_tok.type == MINUS:
            code = left_code + "-" + right_code
        elif node.operation_tok.type == MUL:
            code = left_code + "*" + right_code
        elif node.operation_tok.type == DIV:
            code = left_code + "/" + right_code
        elif node.operation_tok.type == LT:
            code = left_code + "<" + right_code
        elif node.operation_tok.type == LTOREQ:
            code = left_code + "<=" + right_code
        elif node.operation_tok.type == GT:
            code = left_code + ">" + right_code
        elif node.operation_tok.type == GTOREQ:
            code = left_code + ">=" + right_code
        elif node.operation_tok.type == DOUBLE_EQUALS:
            code = left_code + "==" + right_code
        elif node.operation_tok.type == NOT_EQUALS:
            code = left_code + "!=" + right_code
        elif node.operation_tok.matches(KEYWORD, "si"):
            code = left_code + "&&" + right_code
        elif node.operation_tok.matches(KEYWORD, "sau"):
            code = left_code + "||" + right_code
        else:
            return None, RTError("Binary operator of type {} is unhandled!".format(node.operation_tok.type), node.position_start, node.position_end)
        
        return "(" + code + ")", None

    def visit_DeclarationNode(self, node):
        code = ""
        for i in range(len(node.elements)):
            if node.types[i] == "natural":
                code += "int" + " " + node.elements[i].value
            elif node.types[i] == "real":
                code += "float" + " " + node.elements[i].value
            if i < len(node.elements) - 1:
                code += ";\n"
        
        return code, None
    
    def visit_AssignNode(self, node):
        value_code, error = self.visit(node.var_value)
        if error:
            return None, error

        if node.type == "natural":
            code = "int" + " " + node.var_name.tok.value + "=" + value_code
        elif node.type == "real":
            code = "float" + " " + node.var_name.tok.value + "=" + value_code
        else:
            code = node.var_name.tok.value + "=" + value_code
        
        return code, None

    def visit_ReadNode(self, node):
        code = "cin"
        for arg in node.args:
            arg_code, error = self.visit(arg)
            if error:
                return None, error
            
            code += " >> " + arg_code
        
        return code, None

    def visit_WriteNode(self, node):
        code = "cout"
        for arg in node.args:
            arg_code, error = self.visit(arg)
            if error:
                return None, error
            
            code += " << " + arg_code
        
        return code, None
    
    def visit_IfNode(self, node):
        code = "if"

        cond_code, error = self.visit(node.if_cond)
        if error:
            return None, error
        
        code += "(" + cond_code + ")"

        block_code, error = self.visit(node.if_block)
        if error:
            return error, None
        
        code += block_code

        if node.else_block:
            code += "\nelse"
            else_code, error = self.visit(node.else_block)
            if error:
                return None
            code += else_code
        
        return code, None
        
    def visit_Block(self, node):
        code = "{\n"

        for stmt in node.statements:
            line_code, error = self.visit(stmt)
        
            if error:
                return None, error

            code += line_code
            if not isinstance(stmt, IfNode):
                code += ";"
            code += "\n"

        code += "}"
        return code, None
        

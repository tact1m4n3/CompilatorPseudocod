from token_ import *
from errors import InvalidSyntaxError
from ast import *


class ParserErrors:
    def __init__(self):
        self.errors = []

    def register_error(self, error):
        self.errors.append(error)


###################
# Parser
###################
class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.current_tok = None
        self.errors = ParserErrors()

        self.advance()

    def advance(self):
        self.index += 1
        self.current_tok = self.tokens[self.index] if self.index < len(self.tokens) else None
    
    def parse_program(self):
        program = Program()

        while self.current_tok.type is not EOF:
            stmt = self.parse_statement()

            if stmt:
                program.statements.append(stmt)
            
            while self.current_tok.type == NEWLINE:
                self.advance()

        return program

    def parse_statement(self):
        if self.current_tok.matches(KEYWORD, "scrie"):
            return self.parse_write_statement()
        elif self.current_tok.matches(KEYWORD, "citeste"):
            return self.parse_read_statement()
        elif self.current_tok.matches(KEYWORD, "Di"):
            return self.parse_declaration_statement()
        elif self.current_tok.matches(KEYWORD, "Do"):
            return self.parse_declaration_statement()
        elif self.current_tok.matches(KEYWORD, "daca"):
            return self.parse_if_statement()
        elif self.current_tok.type in (INT, FLOAT, STRING, IDENTIFIER, PLUS, MINUS, LPAREN, LSQUAREBRACKET, KEYWORD):
            stmt = self.parse_expression_statement()
            return stmt
        else:
            self.errors.register_error(InvalidSyntaxError(
                "Expected INT, IDENTIFIER, '+', '-', '(', '['",
                self.current_tok.position_start,
                self.current_tok.position_end,
            ))
            self.advance()
            return None
    
    def parse_if_statement(self):
        position_start = self.current_tok.position_start
        self.advance()

        condition = self.parse_math_expression()

        block = self.parse_block_statement([KEYWORD, KEYWORD], ["altfel", "sfdaca"])

        if not block:
            return None

        else_block = None
        if self.current_tok.matches(KEYWORD, "altfel"):
            else_block = self.parse_block_statement([KEYWORD], ["sfdaca"])
            if not else_block:
                return None

        self.advance()
        return IfNode(condition, block, else_block, position_start, self.current_tok.position_end)

    def parse_block_statement(self, end_token_types, end_token_values):
        position_start = self.current_tok.position_start
        
        self.advance()

        block = Block()
        while not self.current_tok.matches(end_token_types[0], end_token_values[0]):
            if len(end_token_types) == 2:
                if self.current_tok.matches(end_token_types[1], end_token_values[1]):
                    break
            
            while self.current_tok.type == NEWLINE:
                self.advance()
            
            if self.current_tok.type == EOF:
                self.errors.register_error(InvalidSyntaxError(
                    "Unexpected end of file",
                    position_start,
                    self.current_tok.position_end,
                ))
                return None

            stmt = self.parse_statement()

            if stmt:
                block.statements.append(stmt)
            
            while self.current_tok.type == NEWLINE:
                self.advance()
        
        return block
    
    def parse_declaration_statement(self):
        position_start = self.current_tok.position_start
        self.advance()
        if not self.current_tok.type == COLON:
            self.errors.register_error(InvalidSyntaxError("Expected ':'", self.current_tok.position_start, self.current_tok.position_end))
            return

        self.advance()

        elements = []
        types = []
        element = self.current_tok
        elements.append(element)

        self.advance()
        
        if self.is_type():
            types.append(self.current_tok.value)
            self.advance()
        
        while self.current_tok.type == COMMA:
            self.advance()
            element = self.current_tok
            self.advance()
            elements.append(element)

            if self.is_type():
                types.append(self.current_tok.value)
                self.advance()
        
        if len(types) == 1:
            t = types[0]
            for _ in range(len(elements) - 1):
                types.append(t)
    
        if len(types) != len(elements):
            self.errors.register_error(InvalidSyntaxError("The length of elements mismatch the length of types.", position_start, self.current_tok.position_end))
            return None

        return DeclarationNode(elements, types, position_start, self.current_tok.position_end)
        
    def parse_write_statement(self):
        position_start = self.current_tok.position_start

        self.advance()
        elements = []

        element = self.parse_math_expression()
        elements.append(element)
        while self.current_tok.type == COMMA and not self.current_tok.type == NEWLINE:
            self.advance()
            if self.current_tok.type == NEWLINE:
                break

            elements.append(self.parse_math_expression())
        
        return WriteNode(elements, position_start, self.current_tok.position_end)

    def parse_read_statement(self):
        position_start = self.current_tok.position_start

        self.advance()
        elements = []

        element = self.parse_math_expression()
        elements.append(element)
        while self.current_tok.type == COMMA and not self.current_tok.type == NEWLINE:
            self.advance()
            if self.current_tok.type == NEWLINE:
                break

            elements.append(self.parse_math_expression())

        return ReadNode(elements, position_start, self.current_tok.position_end)

    def parse_expression_statement(self):
        if self.current_tok.type in (INT, FLOAT, STRING, IDENTIFIER, PLUS, MINUS, LPAREN, LSQUAREBRACKET, KEYWORD):
            stmt = self.parse_assign_expression()
            return stmt
        else:
            self.errors.register_error(InvalidSyntaxError(
                "Expected INT, IDENTIFIER, '+', '-', '(', '[', 'if'",
                self.current_tok.position_start,
                self.current_tok.position_end,
            ))
            return None

    def parse_assign_expression(self):
        position_start = self.current_tok.position_start
        left = self.parse_math_expression()
        if self.current_tok.type == BACKWORD_ARROW:
            if not isinstance(left, IdentifierNode):
                self.errors.register_error(InvalidSyntaxError(
                    f"You can't assign a value to {left}",
                    self.current_tok.position_start,
                    self.current_tok.position_end,
                ))
                return None
            
            self.advance()
            
            if self.current_tok.type == LPAREN:
                self.advance()
                type_ = self.current_tok.value
                self.advance()

                if self.current_tok.type != RPAREN:
                    self.errors.register_error(InvalidSyntaxError(
                        f"Expected ')'",
                        self.current_tok.position_start,
                        self.current_tok.position_end,
                    ))
                    return None
                
                self.advance()
            else: type_ = None
        
            right = self.parse_math_expression()
            return AssignNode(type_, left, right, position_start, self.current_tok.position_end)
        return left

    def parse_math_expression(self):
        if self.current_tok.type in (INT, FLOAT, STRING, IDENTIFIER, PLUS, MINUS, LPAREN, LSQUAREBRACKET, KEYWORD):
            return self.parse_and_or_expression()
        else:
            self.errors.register_error(InvalidSyntaxError(
                "Expected INT, IDENTIFIER, '+', '-', '(', '['",
                self.current_tok.position_start,
                self.current_tok.position_end,
            ))
            return None
    
    def parse_and_or_expression(self):
        position_start = self.current_tok.position_start
        left = self.parse_comparator_expression()

        while self.current_tok.matches(KEYWORD, "si") or self.current_tok.matches(KEYWORD, "sau"):
            operator = self.current_tok
            self.advance()
            
            right = self.parse_comparator_expression()
            left = BinaryOperationNode(left, operator, right, position_start, self.current_tok.position_end)
        else:
            return left

    def parse_comparator_expression(self):
        position_start = self.current_tok.position_start
        left = self.expression()
        if self.current_tok.type in (LT, LTOREQ, GT, GTOREQ, DOUBLE_EQUALS, NOT_EQUALS):
            operator = self.current_tok
            self.advance()

            right = self.expression()
            return BinaryOperationNode(left, operator, right, position_start, self.current_tok.position_end)
        else:
            return left

    def expression(self):
        position_start = self.current_tok.position_start
        left = self.term()

        while self.current_tok is not None and self.current_tok.type in (PLUS, MINUS):
            if not self.current_tok.type in (PLUS, MINUS):
                self.errors.register_error(InvalidSyntaxError(
                    "Expected '+' or '-'",
                    self.current_tok.position_start,
                    self.current_tok.position_end,
                ))
                return None
            operation_tok = self.current_tok
            self.advance()
            right = self.term()
            left = BinaryOperationNode(left, operation_tok, right, position_start, self.current_tok.position_end)

        return left

    def term(self):
        position_start = self.current_tok.position_start
        left = self.factor()

        while self.current_tok is not None and self.current_tok.type in (MUL, DIV):
            if not self.current_tok.type in (MUL, DIV):
                self.errors.register_error(InvalidSyntaxError(
                    "Expected '*' or '/'",
                    self.current_tok.position_start,
                    self.current_tok.position_end,
                ))
                return None
            operation_tok = self.current_tok
            self.advance()
            right = self.factor()
            left = BinaryOperationNode(left, operation_tok, right, position_start, self.current_tok.position_end)

        return left

    def factor(self):
        position_start = self.current_tok.position_start
        tok = self.current_tok

        if tok.type == LPAREN:
            self.advance()

            result = self.parse_math_expression()
            if self.current_tok.type != RPAREN:
                self.errors.register_error(InvalidSyntaxError(
                    "Expected ')'",
                    self.current_tok.position_start,
                    self.current_tok.position_end,
                ))
                return None
            self.advance()
            return result
        elif tok.type == INT or tok.type == FLOAT:
            self.advance()
            return NumberNode(tok, position_start, self.current_tok.position_end)
        elif tok.type == STRING:
            self.advance()
            return StringNode(tok, position_start, self.current_tok.position_end)
        elif tok.type == IDENTIFIER:
            self.advance()
            return IdentifierNode(tok, position_start, self.current_tok.position_end)
        elif tok.type in (PLUS, MINUS) or tok.matches(KEYWORD, "nu"):
            op_tok = self.current_tok
            self.advance()
            right = self.factor()
            return UnaryOperationNode(op_tok, right, position_start, self.current_tok.position_end)
        elif tok.type == LSQUAREBRACKET:
            self.advance()

            result = self.parse_math_expression()
            if self.current_tok.type != RPAREN:
                self.errors.register_error(InvalidSyntaxError(
                    "Expected ']'",
                    self.current_tok.position_start,
                    self.current_tok.position_end,
                ))
                return None
            self.advance()
            return IntCastNode(result)
        self.errors.register_error(InvalidSyntaxError(
            "Expected INT, IDENTIFIER, '+', '-', '(', '[', 'if'",
            self.current_tok.position_start,
            self.current_tok.position_end,
        ))

    def is_type(self):
        if self.current_tok.matches("KEYWORD", "natural") or self.current_tok.matches("KEYWORD", "real"):
            return True
        return False

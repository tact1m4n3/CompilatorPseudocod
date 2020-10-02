###################
# Token Types
###################
INT = "INT"
FLOAT = "FLOAT"
STRING = "STRING"
IDENTIFIER = "IDENTIFIER"
KEYWORD = "KEYWORD"
PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
DIV = "DIV"
LT = "LT"
LTOREQ = "LTOREQ"
GT = "GT"
MOD = "MOD"
GTOREQ = "GTOREQ"
DOUBLE_EQUALS = "EQUALS"
NOT_EQUALS = "NOT_EQUALS"
NOT = "NOT"
EQUALS = "EQUALS"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
LSQUAREBRACKET = "LSQUAREBRACKET"
RSQUAREBRACKET = "RSQUAREBRACKET"
LBRACKET = "LBRACKET"
RBRACKET = "RBRACKET"
ARROW = "ARROW"
BACKWORD_ARROW = "BACKWORD_ARROW"
COMMA = "COMMA"
COLON = "COLON"
NEWLINE = "NEWLINE"
EOF = "EOF"

###################
# KEYWORDS
###################
keywords = [
    "citeste",
    "scrie",
    "Di",
    "Do",
    "daca",
    "atunci",
    "altfel",
    "sfdaca",
    "si",
    "sau",
    "nu",
    "pentru",
    "executa",
    "catTimp",
    "natural",
    "real"
]


###################
# Token
###################
class Token(object):
    def __init__(self, _type, _value=None, _position_start=None, _position_end=None):
        self.type = _type
        self.value = _value

        self.position_start = _position_start
        if _position_end:
            self.position_end = _position_end
        else:
            self.position_end = _position_start.advance()

    def matches(self, _type, _val):
        if self.type == _type and self.value == _val:
            return True
        else:
            return False

    def __repr__(self):
        if self.value:
            return "{}:{}".format(self.type, self.value)
        return "{}".format(self.type)


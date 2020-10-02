###################
# Errors
###################
class Error(object):
    def __init__(self, _error, _text, _position_start, _position_end):
        self.error = _error
        self.text = _text
        self.position_start = _position_start
        self.position_end = _position_end

    def as_string(self):
        _error = f'File {self.position_start.filename}, line {str(self.position_start.line + 1)}, in main\n'
        _error += f"{self.error}: {self.text}"
        return _error


class IllegalCharError(Error):
    def __init__(self, _text, _position_start, _position_end):
        super().__init__("Illegal Character Error", _text, _position_start, _position_end)

class UnexpectedCharError(Error):
    def __init__(self, _text, _position_start, _position_end):
        super().__init__("Unexpected Character Error", _text, _position_start, _position_end)

class CharacterNotFoundError(Error):
    def __init__(self, _text, _position_start, _position_end):
        super().__init__("Character Not Found Error", _text, _position_start, _position_end)

class InvalidSyntaxError(Error):
    def __init__(self, _text, _position_start, _position_end):
        super().__init__("Invalid Syntax Error", _text, _position_start, _position_end)

class RTError(Error):
    def __init__(self, _text, _position_start, _position_end):
        super().__init__("RunTime Error", _text, _position_start, _position_end)


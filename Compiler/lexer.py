import re

class Token:
    """
    Represents a token with type and value.
    """

    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    """
    Lexer class to tokenize the input source code.
    """

    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_pos = 0

        # Token patterns (regular expressions)
        self.token_specs = [
            ('NUMBER',   r'\d+'),
            ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('PLUS',     r'\+'),
            ('MINUS',    r'-'),
            ('MULT',     r'\*'),
            ('DIV',      r'/'),
            ('ASSIGN',   r'='),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('SEMICOLON', r';'),
            ('SKIP',     r'[ \t\n]+'),  # Skip over spaces and tabs
            ('MISMATCH', r'.'),          # Any other character
        ]
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specs)

    def tokenize(self):
        """
        Tokenize the entire input string.
        """
        for match in re.finditer(self.token_regex, self.source_code):
            token_type = match.lastgroup
            value = match.group(token_type)
            if token_type == 'SKIP':
                continue
            elif token_type == 'MISMATCH':
                raise SyntaxError(f"Unexpected character: {value}")
            else:
                token = Token(token_type, value)
                self.tokens.append(token)

        return self.tokens


# Example usage:
if __name__ == "__main__":
    code = "int x = 5 + 3;"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
# Lexer implementation

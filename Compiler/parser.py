from lexer import Lexer
from ast import Program, VariableDeclaration, Assignment, BinaryOperation

class Parser:
    """
    Parser class to parse tokens and produce an Abstract Syntax Tree (AST).
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
    
    def eat(self, token_type):
        """
        Consume the current token if it matches the expected type.
        """
        if self.current_token.type == token_type:
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
        else:
            raise SyntaxError(f"Expected token {token_type}, but got {self.current_token.type}")

    def parse(self):
        """
        Parse the token list to create an AST.
        """
        return self.parse_program()

    def parse_program(self):
        """
        Parse a program, which consists of a list of statements.
        """
        root = Program()

        while self.current_token_index < len(self.tokens):
            if self.current_token.type == 'ID':
                root.add_child(self.parse_assignment())
            elif self.current_token.type == 'NUMBER':
                raise SyntaxError("Unexpected number")
            else:
                self.eat(self.current_token.type)  # Skips over unrecognized tokens for simplicity
        
        return root

    def parse_assignment(self):
        """
        Parse an assignment statement.
        """
        var_name = self.current_token.value
        self.eat('ID')
        self.eat('ASSIGN')
        value = self.parse_expression()
        self.eat('SEMICOLON')

        return Assignment(var_name, value)

    def parse_expression(self):
        """
        Parse an expression, which can currently only be a simple binary operation.
        """
        left = self.current_token.value
        self.eat('NUMBER')

        if self.current_token.type in ('PLUS', 'MINUS', 'MULT', 'DIV'):
            operator = self.current_token.value
            self.eat(self.current_token.type)

            right = self.current_token.value
            self.eat('NUMBER')

            return BinaryOperation(left, operator, right)
        else:
            raise SyntaxError(f"Unexpected token in expression: {self.current_token.type}")


# Example usage:
if __name__ == "__main__":
    code = "x = 5 + 3;"
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
# Parser implementation

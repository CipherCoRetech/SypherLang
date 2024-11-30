from ast import ASTNode

class Parser:
    """
    Parser for SypherLang that converts a list of tokens into an Abstract Syntax Tree (AST).
    It takes tokens from the lexer and builds a structured tree representation of the program.
    """

    def __init__(self):
        self.tokens = []
        self.current_token_index = 0

    def parse(self, tokens):
        """
        Parse the list of tokens to generate an AST.
        
        :param tokens: List of tokens to parse.
        :return: Root of the generated AST.
        """
        self.tokens = tokens
        self.current_token_index = 0
        return self.program()

    def program(self):
        """
        Parse the entire program.
        
        :return: Root node of the AST representing the program.
        """
        nodes = []
        while self.current_token_index < len(self.tokens):
            nodes.append(self.statement())
        return ASTNode(type='program', body=nodes)

    def statement(self):
        """
        Parse a statement.
        
        :return: AST node representing the statement.
        """
        token_type, token_value = self.current_token()
        if token_type == 'KEYWORD' and token_value == 'let':
            return self.assignment_statement()
        elif token_type == 'KEYWORD' and token_value == 'function':
            return self.function_statement()
        elif token_type == 'IDENTIFIER':
            return self.expression()
        else:
            raise ValueError(f"Unexpected token {token_value} at index {self.current_token_index}")

    def assignment_statement(self):
        """
        Parse an assignment statement.
        
        :return: AST node representing the assignment.
        """
        self.consume('KEYWORD', 'let')
        identifier = self.consume('IDENTIFIER')
        self.consume('OPERATOR', '=')
        value = self.expression()
        self.consume('DELIMITER', ';')
        return ASTNode(type='assignment', name=identifier, value=value)

    def function_statement(self):
        """
        Parse a function definition.
        
        :return: AST node representing the function.
        """
        self.consume('KEYWORD', 'function')
        function_name = self.consume('IDENTIFIER')
        self.consume('DELIMITER', '(')
        args = []
        while self.current_token()[1] != ')':
            args.append(self.consume('IDENTIFIER'))
            if self.current_token()[1] == ',':
                self.consume('DELIMITER', ',')
        self.consume('DELIMITER', ')')
        self.consume('DELIMITER', '{')
        body = []
        while self.current_token()[1] != '}':
            body.append(self.statement())
        self.consume('DELIMITER', '}')
        return ASTNode(type='function_call', function_name=function_name, args=args, body=body)

    def expression(self):
        """
        Parse an expression (could be arithmetic or logical).
        
        :return: AST node representing the expression.
        """
        left = self.term()
        while self.current_token()[1] in ('+', '-'):
            operator = self.consume('OPERATOR')
            right = self.term()
            left = ASTNode(type='expression', left=left, right=right, operator=operator)
        return left

    def term(self):
        """
        Parse a term for expressions.
        
        :return: AST node representing the term.
        """
        token_type, token_value = self.current_token()
        if token_type == 'NUMBER':
            self.consume('NUMBER')
            return ASTNode(type='literal', value=int(token_value))
        elif token_type == 'IDENTIFIER':
            self.consume('IDENTIFIER')
            return ASTNode(type='variable', name=token_value)
        else:
            raise ValueError(f"Unexpected token {token_value} at index {self.current_token_index}")

    def current_token(self):
        """
        Get the current token in the list.
        
        :return: Current token (type, value)
        """
        return self.tokens[self.current_token_index]

    def consume(self, expected_type, expected_value=None):
        """
        Consume the current token if it matches the expected type and value.
        
        :param expected_type: Expected type of the token.
        :param expected_value: Optional expected value of the token.
        :return: The value of the token consumed.
        """
        token_type, token_value = self.current_token()
        if token_type != expected_type or (expected_value is not None and token_value != expected_value):
            raise ValueError(f"Expected token {expected_type} '{expected_value}', got {token_type} '{token_value}'")
        self.current_token_index += 1
        return token_value

import re

class Lexer:
    """
    Lexer for SypherLang that converts source code into tokens.
    It splits the input into meaningful symbols such as keywords, operators, literals, and identifiers.
    """

    def __init__(self):
        # Regular expressions for SypherLang tokens
        self.token_patterns = [
            ('KEYWORD', r'\b(function|if|else|while|let|encrypt|prove_privacy|execute_parallel)\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('NUMBER', r'\b\d+\b'),
            ('STRING', r'"[^"]*"'),
            ('OPERATOR', r'[+\-*/=]'),
            ('DELIMITER', r'[{}(),;]'),
            ('WHITESPACE', r'\s+'),
            ('UNKNOWN', r'.')
        ]

    def tokenize(self, code):
        """
        Tokenize the input source code.
        
        :param code: The SypherLang source code as a string.
        :return: A list of tokens.
        """
        tokens = []
        position = 0
        while position < len(code):
            for token_type, pattern in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(code, position)
                if match:
                    lexeme = match.group(0)
                    position = match.end()
                    if token_type != 'WHITESPACE':
                        tokens.append((token_type, lexeme))
                    break
            else:
                raise ValueError(f"Unknown token at position {position}: {code[position]}")
        
        print(f"[Lexer] Tokenized source code into: {tokens}")
        return tokens

import unittest
from lexer import Lexer
from parser import Parser
from ast import ASTNode
from compiler.compiler import Compiler

class TestSypherLangCompiler(unittest.TestCase):
    """
    Test Suite for SypherLang Compiler
    This suite will test the lexer, parser, and compiler functionality in SypherLang.
    """

    def setUp(self):
        """
        Set up the lexer, parser, and compiler instances for testing.
        """
        self.lexer = Lexer()
        self.parser = Parser()
        self.compiler = Compiler()

    def test_lexer_basic_tokens(self):
        """
        Test that the lexer correctly tokenizes a simple SypherLang script.
        """
        code = 'let x = 10;'
        tokens = self.lexer.tokenize(code)
        expected_tokens = [
            ('KEYWORD', 'let'),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '='),
            ('NUMBER', '10'),
            ('DELIMITER', ';')
        ]
        self.assertEqual(tokens, expected_tokens, f"[Lexer Test] Expected tokens {expected_tokens} but got {tokens}")

    def test_lexer_advanced_tokens(self):
        """
        Test the lexer with a more advanced script containing functions and multiple keywords.
        """
        code = 'function encryptData(data) { let y = data + 5; }'
        tokens = self.lexer.tokenize(code)
        expected_tokens = [
            ('KEYWORD', 'function'),
            ('IDENTIFIER', 'encryptData'),
            ('DELIMITER', '('),
            ('IDENTIFIER', 'data'),
            ('DELIMITER', ')'),
            ('DELIMITER', '{'),
            ('KEYWORD', 'let'),
            ('IDENTIFIER', 'y'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'data'),
            ('OPERATOR', '+'),
            ('NUMBER', '5'),
            ('DELIMITER', ';'),
            ('DELIMITER', '}')
        ]
        self.assertEqual(tokens, expected_tokens, f"[Lexer Test] Expected tokens {expected_tokens} but got {tokens}")

    def test_parser_simple_expression(self):
        """
        Test that the parser can correctly parse a simple expression.
        """
        tokens = [
            ('KEYWORD', 'let'),
            ('IDENTIFIER', 'x'),
            ('OPERATOR', '='),
            ('NUMBER', '10'),
            ('DELIMITER', ';')
        ]
        ast = self.parser.parse(tokens)
        expected_ast = ASTNode(
            type='program',
            body=[
                ASTNode(
                    type='assignment',
                    name='x',
                    value=ASTNode(type='literal', value=10)
                )
            ]
        )
        self.assertEqual(
            ast.to_dict(), expected_ast.to_dict(),
            f"[Parser Test] Expected AST {expected_ast.to_dict()} but got {ast.to_dict()}"
        )

    def test_parser_function_call(self):
        """
        Test that the parser can correctly parse a function call with arguments.
        """
        tokens = [
            ('KEYWORD', 'function'),
            ('IDENTIFIER', 'myFunc'),
            ('DELIMITER', '('),
            ('IDENTIFIER', 'param1'),
            ('DELIMITER', ')'),
            ('DELIMITER', '{'),
            ('KEYWORD', 'let'),
            ('IDENTIFIER', 'result'),
            ('OPERATOR', '='),
            ('IDENTIFIER', 'param1'),
            ('OPERATOR', '*'),
            ('NUMBER', '2'),
            ('DELIMITER', ';'),
            ('DELIMITER', '}')
        ]
        ast = self.parser.parse(tokens)
        expected_ast = ASTNode(
            type='program',
            body=[
                ASTNode(
                    type='function_call',
                    function_name='myFunc',
                    args=['param1'],
                    body=[
                        ASTNode(
                            type='assignment',
                            name='result',
                            value=ASTNode(
                                type='expression',
                                left=ASTNode(type='variable', name='param1'),
                                right=ASTNode(type='literal', value=2),
                                operator='*'
                            )
                        )
                    ]
                )
            ]
        )
        self.assertEqual(
            ast.to_dict(), expected_ast.to_dict(),
            f"[Parser Test] Expected AST {expected_ast.to_dict()} but got {ast.to_dict()}"
        )

    def test_compiler_basic_program(self):
        """
        Test that the compiler can generate bytecode for a simple program.
        """
        code = 'let x = 42;'
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        bytecode = self.compiler.compile(ast)
        expected_bytecode = [
            ('PUSH', 42),
            ('STORE', 'x')
        ]
        self.assertEqual(
            bytecode, expected_bytecode,
            f"[Compiler Test] Expected bytecode {expected_bytecode} but got {bytecode}"
        )

    def test_compiler_function(self):
        """
        Test the compiler for generating bytecode for a function with a return value.
        """
        code = 'function square(num) { return num * num; }'
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        bytecode = self.compiler.compile(ast)
        expected_bytecode = [
            ('FUNC_DEF', 'square', ['num']),
            ('PUSH', 'num'),
            ('PUSH', 'num'),
            ('MUL', None),
            ('RETURN', None)
        ]
        self.assertEqual(
            bytecode, expected_bytecode,
            f"[Compiler Test] Expected bytecode {expected_bytecode} but got {bytecode}"
        )

    def test_privacy_contract(self):
        """
        Test that the compiler can handle a privacy contract with quantum resistance.
        """
        code = '''
        function privacyContract(data) {
            let encrypted = encrypt(data);
            prove_privacy(encrypted);
        }
        '''
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        bytecode = self.compiler.compile(ast)
        expected_bytecode = [
            ('FUNC_DEF', 'privacyContract', ['data']),
            ('PUSH', 'data'),
            ('CALL', 'encrypt'),
            ('STORE', 'encrypted'),
            ('PUSH', 'encrypted'),
            ('CALL', 'prove_privacy')
        ]
        self.assertEqual(
            bytecode, expected_bytecode,
            f"[Privacy Contract Test] Expected bytecode {expected_bytecode} but got {bytecode}"
        )

    def test_concurrent_execution(self):
        """
        Test that the compiler can generate bytecode for concurrent execution commands.
        """
        code = 'execute_parallel(task1, task2, task3);'
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        bytecode = self.compiler.compile(ast)
        expected_bytecode = [
            ('EXEC_PARALLEL', ['task1', 'task2', 'task3'])
        ]
        self.assertEqual(
            bytecode, expected_bytecode,
            f"[Concurrency Test] Expected bytecode {expected_bytecode} but got {bytecode}"
        )

    def test_zero_knowledge_proof(self):
        """
        Test that the zero-knowledge proof function works as expected.
        """
        code = 'prove_privacy(data);'
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        bytecode = self.compiler.compile(ast)
        expected_bytecode = [
            ('PUSH', 'data'),
            ('CALL', 'prove_privacy')
        ]
        self.assertEqual(
            bytecode, expected_bytecode,
            f"[ZKP Test] Expected bytecode {expected_bytecode} but got {bytecode}"
        )


if __name__ == '__main__':
    unittest.main()

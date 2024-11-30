import unittest
from lexer import Lexer
from parser import Parser
from ast import ASTNode
from interpreter import Interpreter

class TestSypherLangInterpreter(unittest.TestCase):
    """
    Test Suite for SypherLang Interpreter
    This suite will test the correct execution of SypherLang code.
    """

    def setUp(self):
        """
        Set up the lexer, parser, and interpreter instances for testing.
        """
        self.lexer = Lexer()
        self.parser = Parser()
        self.interpreter = Interpreter()

    def test_variable_assignment(self):
        """
        Test that the interpreter can handle a simple variable assignment.
        """
        code = 'let x = 5;'
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        result = self.interpreter.execute(ast)
        self.assertEqual(
            self.interpreter.get_variable('x'), 5,
            "[Variable Assignment Test] Expected variable 'x' to be 5, but got {}".format(self.interpreter.get_variable('x'))
        )

    def test_arithmetic_operations(self):
        """
        Test that the interpreter correctly executes arithmetic operations.
        """
        code = 'let y = 10 + 15 * 2;'
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.interpreter.execute(ast)
        expected_value = 10 + 15 * 2
        self.assertEqual(
            self.interpreter.get_variable('y'), expected_value,
            "[Arithmetic Operations Test] Expected variable 'y' to be {}, but got {}".format(expected_value, self.interpreter.get_variable('y'))
        )

    def test_function_definition_and_call(self):
        """
        Test that the interpreter can define and execute a function correctly.
        """
        code = '''
        function add(a, b) {
            return a + b;
        }
        let result = add(10, 20);
        '''
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.interpreter.execute(ast)
        self.assertEqual(
            self.interpreter.get_variable('result'), 30,
            "[Function Call Test] Expected 'result' to be 30, but got {}".format(self.interpreter.get_variable('result'))
        )

    def test_conditionals(self):
        """
        Test the interpreter's handling of conditional statements.
        """
        code = '''
        let a = 10;
        let b = 20;
        if (a < b) {
            let result = "a is less than b";
        } else {
            let result = "a is not less than b";
        }
        '''
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.interpreter.execute(ast)
        self.assertEqual(
            self.interpreter.get_variable('result'), "a is less than b",
            "[Conditionals Test] Expected 'result' to be 'a is less than b', but got {}".format(self.interpreter.get_variable('result'))
        )

    def test_loops(self):
        """
        Test that the interpreter correctly executes loops.
        """
        code = '''
        let sum = 0;
        for (let i = 0; i < 5; i = i + 1) {
            sum = sum + i;
        }
        '''
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.interpreter.execute(ast)
        self.assertEqual(
            self.interpreter.get_variable('sum'), 10,
            "[Loops Test] Expected 'sum' to be 10, but got {}".format(self.interpreter.get_variable('sum'))
        )

    def test_concurrent_execution(self):
        """
        Test that the interpreter can execute multiple functions concurrently.
        """
        code = '''
        function task1() {
            return 5;
        }
        function task2() {
            return 10;
        }
        execute_parallel(task1(), task2());
        '''
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        result = self.interpreter.execute(ast)
        expected_result = [5, 10]
        self.assertEqual(
            result, expected_result,
            "[Concurrent Execution Test] Expected result to be {}, but got {}".format(expected_result, result)
        )

    def test_privacy_contract_execution(self):
        """
        Test the interpreter's handling of a privacy contract.
        """
        code = '''
        function privacyContract(data) {
            let encrypted = encrypt(data);
            prove_privacy(encrypted);
            return encrypted;
        }
        let result = privacyContract("Sensitive Data");
        '''
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.interpreter.execute(ast)
        self.assertTrue(
            self.interpreter.get_variable('result').startswith("encrypted_"),
            "[Privacy Contract Test] Expected 'result' to be encrypted data, but got {}".format(self.interpreter.get_variable('result'))
        )

    def test_zero_knowledge_proof(self):
        """
        Test that zero-knowledge proof can be verified correctly.
        """
        code = '''
        let data = "secret";
        let proof = prove_privacy(data);
        if (verify_proof(proof)) {
            let result = "Proof Verified";
        } else {
            let result = "Proof Failed";
        }
        '''
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.interpreter.execute(ast)
        self.assertEqual(
            self.interpreter.get_variable('result'), "Proof Verified",
            "[Zero-Knowledge Proof Test] Expected 'result' to be 'Proof Verified', but got {}".format(self.interpreter.get_variable('result'))
        )

    def test_error_handling(self):
        """
        Test the interpreter's ability to handle runtime errors.
        """
        code = '''
        let x = 10 / 0;
        '''
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        with self.assertRaises(ZeroDivisionError):
            self.interpreter.execute(ast)

    def test_quantum_resistance_function(self):
        """
        Test that quantum-resistant cryptographic functions are executed properly.
        """
        code = '''
        let secureKey = generate_quantum_resistant_key();
        '''
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.interpreter.execute(ast)
        self.assertTrue(
            self.interpreter.get_variable('secureKey').startswith("lattice_key_"),
            "[Quantum Resistance Test] Expected 'secureKey' to start with 'lattice_key_', but got {}".format(self.interpreter.get_variable('secureKey'))
        )


if __name__ == '__main__':
    unittest.main()

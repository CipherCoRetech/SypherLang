import ast
import operator as op
import sys
import traceback

class SypherLangInterpreter:
    def __init__(self):
        # Define supported operators and their functions for safe evaluation
        self.operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Mod: op.mod,
            ast.Pow: op.pow,
            ast.BitXor: op.xor,
            ast.USub: op.neg,
            ast.Lt: op.lt,
            ast.Gt: op.gt,
            ast.LtE: op.le,
            ast.GtE: op.ge,
            ast.Eq: op.eq,
            ast.NotEq: op.ne,
            ast.And: op.and_,
            ast.Or: op.or_,
        }
        
    def interpret(self, code):
        try:
            # Parse the code into an AST (Abstract Syntax Tree)
            parsed_code = ast.parse(code, mode='eval')
            
            # Evaluate the AST recursively
            result = self._evaluate(parsed_code.body)
            return result
        except Exception as e:
            # Catch and print detailed error traceback
            traceback.print_exc()
            return f"Error: {str(e)}"

    def _evaluate(self, node):
        """
        Recursively evaluate an AST node.
        """
        if isinstance(node, ast.Expression):
            return self._evaluate(node.body)
        
        elif isinstance(node, ast.Num):  # <number>
            return node.n
        
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            operator_func = self.operators[type(node.op)]
            return operator_func(left, right)
        
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand>
            operand = self._evaluate(node.operand)
            operator_func = self.operators[type(node.op)]
            return operator_func(operand)
        
        elif isinstance(node, ast.Compare):  # <left> <comparator> <right>
            left = self._evaluate(node.left)
            comparators = [self._evaluate(comp) for comp in node.comparators]
            comparison = type(node.ops[0])
            operator_func = self.operators[comparison]
            return operator_func(left, comparators[0])
        
        elif isinstance(node, ast.BoolOp):  # <left> <boolop> <right>
            values = [self._evaluate(v) for v in node.values]
            bool_op_func = self.operators[type(node.op)]
            result = values[0]
            for value in values[1:]:
                result = bool_op_func(result, value)
            return result
        
        else:
            raise TypeError(f"Unsupported type: {type(node)}")

if __name__ == "__main__":
    interpreter = SypherLangInterpreter()
    print("SypherLang Interpreter\nEnter your code below or type 'exit' to quit.")
    while True:
        try:
            code = input("\n>>> ")
            if code.lower() in ["exit", "quit"]:
                break
            result = interpreter.interpret(code)
            print(result)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

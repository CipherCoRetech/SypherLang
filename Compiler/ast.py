class ASTNode:
    """
    Class representing a node in the Abstract Syntax Tree.
    Each node represents an element of the source code, such as expressions, assignments, or function calls.
    """

    def __init__(self, type, value=None, name=None, left=None, right=None, operator=None, function_name=None, args=None, condition=None, body=None, data=None, contract=None, tasks=None):
        self.type = type            # Type of node, e.g., 'assignment', 'expression', 'function_call'
        self.value = value          # Value associated with the node, e.g., a constant value
        self.name = name            # Name for variable assignment
        self.left = left            # Left child for expressions
        self.right = right          # Right child for expressions
        self.operator = operator    # Operator for binary operations, e.g., '+', '-'
        self.function_name = function_name  # Name of the function called
        self.args = args            # Arguments for function calls
        self.condition = condition  # Condition for control flow constructs
        self.body = body            # Body of statements for control flow
        self.data = data            # Data for quantum operations
        self.contract = contract    # Privacy contract information
        self.tasks = tasks          # Parallel execution tasks

    def __repr__(self):
        return f"ASTNode(type={self.type}, value={self.value}, name={self.name})"

    def to_dict(self):
        """
        Convert the AST node to a dictionary for easier serialization and debugging.
        """
        return {
            "type": self.type,
            "value": self.value,
            "name": self.name,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "operator": self.operator,
            "function_name": self.function_name,
            "args": self.args,
            "condition": self.condition,
            "body": [n.to_dict() for n in self.body] if self.body else None,
            "data": self.data,
            "contract": self.contract,
            "tasks": self.tasks
        }

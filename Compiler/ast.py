class ASTNode:
    """
    Base class for all AST nodes.
    Each node in the AST has a type and may have children or attributes.
    """

    def __init__(self, node_type, **kwargs):
        self.node_type = node_type
        self.attributes = kwargs
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"ASTNode({self.node_type}, {self.attributes}, children={len(self.children)})"


class Program(ASTNode):
    """
    Root node representing an entire program.
    """

    def __init__(self):
        super().__init__(node_type="Program")


class Function(ASTNode):
    """
    Node representing a function.
    """

    def __init__(self, name, return_type):
        super().__init__(node_type="Function", name=name, return_type=return_type)


class VariableDeclaration(ASTNode):
    """
    Node representing a variable declaration.
    """

    def __init__(self, var_name, var_type):
        super().__init__(node_type="VariableDeclaration", name=var_name, var_type=var_type)


class BinaryOperation(ASTNode):
    """
    Node representing a binary operation like addition or multiplication.
    """

    def __init__(self, left_operand, operator, right_operand):
        super().__init__(node_type="BinaryOperation", operator=operator)
        self.add_child(left_operand)
        self.add_child(right_operand)


class Assignment(ASTNode):
    """
    Node representing an assignment statement.
    """

    def __init__(self, variable, value):
        super().__init__(node_type="Assignment", variable=variable)
        self.add_child(value)


# Example usage:
# Creating a simple AST for: int x = 5 + 3;
if __name__ == "__main__":
    root = Program()
    var_decl = VariableDeclaration("x", "int")
    binary_op = BinaryOperation("5", "+", "3")
    assignment = Assignment("x", binary_op)

    root.add_child(var_decl)
    root.add_child(assignment)

    print(root)
# Abstract Syntax Tree (AST) implementation

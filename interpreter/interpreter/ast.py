from interpreter.token import Token

class Node:
    pass

class Number(Node):
    def __init__(self, token:Token):
        self.token=token

    def __str__(self):
        return f"{self.__class__.__name__}({self.token})"

class BinOp(Node):
    def __init__(self, left: Node, op: Token, right: Node):
        self.left=left
        self.op=op
        self.right=right

    def __str__(self):
        return f"{self.__class__.__name__}{self.op.value}({self.left}, {self.right})"
    
class UnaryOp(Node):
    def __init__(self, op: Token, expr: Node):
        self.op=op
        self.expr= expr

    def __str__(self) -> str:
        return f"{self.__class__.__name__}{self.op.value}({self.expr})"
    
class Assign(Node):
    def __init__(self, variable: Token, value: Node):
        self.variable = variable
        self.value = value

    def __str__(self):
        return f"{self.__class__.__name__}({self.variable.value} := {self.value})"
    
class Variable(Node):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):
        return f"{self.__class__.__name__}({self.token.value})"
    
class Begin(Node):
    def __init__(self, statements: list):
        self.statements = statements

    def __str__(self):
        return f"{self.__class__.__name__}({self.statements})"

class End(Node):
    def __init__(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}END"
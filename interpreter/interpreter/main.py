from interpreter.parser import Parser
from interpreter.ast import Number, BinOp, UnaryOp, Assign, Variable, Begin, End

class NodeVisitor:
    def visit(self):
        ...

class Interpreter(NodeVisitor):
    def __init__(self):
        self._parser=Parser()
        self.variable_stack = []

    def eval(self, code: str) -> None:
        tree = self._parser.eval(code)
        self.visit(tree)

    def visit(self, node):
        if isinstance(node, Number):
            return self._visit_number(node)
        elif isinstance(node, BinOp):
            return self._visit_binop(node)
        elif isinstance(node, UnaryOp):
            return self._visit_unaryop(node)
        elif isinstance(node, Assign):
            return self._visit_assignment(node)
        elif isinstance(node, Variable):
            return self._visit_variable(node)
        elif isinstance(node, Begin):
            self._visit_begin(node)
        elif isinstance(node, End):
            self._visit_end(node)
    
    def _visit_assignment(self, node: Assign):
        current_variables = self.variable_stack[-1]
        current_variables[node.variable.value] = self.visit(node.value)

    def _visit_variable(self, node: Variable):
        for context in reversed(self.variable_stack):
            if node.token.value in context:
                return context[node.token.value]
        raise NameError(f'Variable {node.token.value} is not defined')

    def _visit_begin(self, node):
        self.variable_stack.append({})
        for statement in node.statements:
            self.visit(statement)

    def _visit_end(self, node):
        current_variables = self.variable_stack.pop()
        for var, value in current_variables.items():
            print(f"{var}: {value}")

    def _visit_number(self, node: Number):
        return float(node.token.value)
    
    def _visit_binop(self, node:BinOp):
        match node.op.value:
            case "+":
                return self.visit(node.left) + self.visit(node.right)
            case "-":
                return self.visit(node.left) - self.visit(node.right)
            case "/":
                return self.visit(node.left) / self.visit(node.right)
            case "*":
                return self.visit(node.left) * self.visit(node.right)
            # Тесты в других модулях не допускают значений других значений в этот блок.
            #case _:
            #    raise RuntimeError("Invalid operator")

    def _visit_unaryop(self, node:UnaryOp):
        match node.op.value:
            case "+":
                return self.visit(node.expr)
            case "-":
                return -self.visit(node.expr)
            # Тесты в других модулях не допускают значений кроме + или - в этот блок.
            #case _:
            #    raise RuntimeError("Invalid operator")
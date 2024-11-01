from notation.exceptions import UnknownOperatorError, MissingOperandError, TooManyOperandsError

def isOperand(s: str) -> bool:
    try:
        operand=float(s)
        return True
    except ValueError:
        return False

def isOperator(operator: str) -> bool:
    available_operators=['+', '-', '*', '/']
    if operator in available_operators:
        return True
    else:
        raise UnknownOperatorError("Unknown operator")

def calculate(s: str) -> float:
    operands=[]
    for x in s.split()[::-1]:
        if (isOperand(x)):
            operands.append(float(x))
        else:
            if isOperator(x):
                try:
                    op1=operands.pop()
                    op2=operands.pop()
                except IndexError:
                    raise MissingOperandError("Not enough operands for the operation")
                match x:
                    case '+':
                        operands.append(op1+op2)
                    case '-':
                        operands.append(op1-op2)
                    case '*':
                        operands.append(op1*op2)
                    case '/':
                        try:
                            operands.append(op1/op2)
                        except ZeroDivisionError:
                            raise ZeroDivisionError("Division by zero")
    if len(operands)>1:
        raise TooManyOperandsError("Invalid expression. Too many operands")
    return operands[0]

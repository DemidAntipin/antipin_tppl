from notation.exceptions import MissingOperandError, InterpreterError, BadToken
from notation.token import Token, TokenType

class Interpreter():
    def __init__(self):
        self._pos=0
        self._text=""
        self._current_token = None

    def __next(self):
        if self._pos > len(self._text)-1:
            return Token(TokenType.EOL, "")
        current_char = self._text[self._pos]
        if current_char.isdigit():
            self._pos+=1
            while not self._text[self._pos].isspace():
                current_char=self._text[self._pos]+current_char
                self._pos+=1
            return Token(TokenType.INTEGER, current_char)
        available_operators=["+", "-", "*", "/"]
        if current_char in available_operators:
            self._pos+=1
            return Token(TokenType.OPERATOR, current_char)
        if current_char.isspace():
            self._pos+=1
            return Token(TokenType.SPACE, current_char)
        raise BadToken("Bad token")

    def __check_token(self, type_:TokenType)->bool:
        if self._current_token.type_ == type_:
            return True
        else:
            return False

    def eval(self, s:str)->float:
        self._text=s[::-1]
        operands=[]
        self._current_token=self.__next()
        while not self.__check_token(TokenType.EOL):
          if self.__check_token(TokenType.INTEGER):
            operands.append(float(self._current_token.value))
          elif self.__check_token(TokenType.OPERATOR):
            try:
              left=operands.pop()
              right=operands.pop()
              op=self._current_token
              match op.value:
                case "+":
                    operands.append( left + right )
                case "-":
                    operands.append( left - right )
                case "*":
                    operands.append( left * right )
                case "/":
                    if right==0:
                        raise ZeroDivisionError
                    operands.append( left / right )
            except IndexError:
              raise MissingOperandError("Too few operands for operation")
          self._current_token=self.__next()
        print(operands)
        if len(operands)==1:
          return operands[0]
        else:
          raise InterpreterError("Interpreter finished job with error")


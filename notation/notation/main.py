from notation.token import Token, TokenType
from notation.exceptions import BadToken, MissingOperandError, NotationError

class Notation():
    def __init__(self):
        self._pos=0
        self._prefix=None
        self._current_char=None
        self._current_token=None

    def __forward(self):
        self._pos+=1
        if self._pos>=len(self._prefix):
           self._current_char=None
        else:
            self._current_char=self._prefix[self._pos]

    def __skip(self):
       while self._current_char is not None and self._current_char.isspace():
          self.__forward()

    def __integer(self):
        result = ""
        while (self._current_char is not None and (self._current_char.isdigit() or self._current_char=='.')):
            result+=self._current_char
            self.__forward()
        return result[::-1]

    def __next(self):
        while self._current_char:
           if self._current_char.isspace():
              self.__skip()
              continue
           if self._current_char.isdigit():
              val = self.__integer()
              return Token(TokenType.NUMBER, val)
           if self._current_char in ["+", "-", "*", "/"]:
              op=self._current_char
              self.__forward()
              return Token(TokenType.OPERATOR, op)
           else:
              raise BadToken("Bad token")
        return Token(TokenType.EOL, "")

    def __expr(self)->str:
        result=[]
        while self._current_token and (self._current_token.type_ != TokenType.EOL):
            if self._current_token.type_ == TokenType.NUMBER:
                result.append(self._current_token.value)
            elif self._current_token.type_ == TokenType.OPERATOR:
                try:
                    left=result.pop()
                    right=result.pop()
                    result.append( f"( {left} {self._current_token.value} {right} )" )
                except IndexError:
                   raise MissingOperandError("Too few operands for operation")
            self._current_token=self.__next()
        if len(result)==1:
            return result[0]
        else:
           raise NotationError("Invalid notation")

    def to_infix(self, s:str)->str:
        self._prefix=s[::-1]
        self._pos=0
        self._current_char=self._prefix[self._pos]
        self._current_token=self.__next()
        return self.__expr()
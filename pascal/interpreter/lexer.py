from interpreter.exceptions import MissingOperandError, InterpreterError, BadToken
from interpreter.token import Token, TokenType

class Lexer():
    def __init__(self):
        self._pos=0
        self._text=""
        self._current_char = None

    def __forward(self):
        self._pos+=1
        if self._pos>=len(self._text):
           self._current_char=None
        else:
            self._current_char=self._text[self._pos]

    def __skip(self):
       while self._current_char is not None and self._current_char.isspace():
          self.__forward()

    def __integer(self):
        result = ""
        while (self._current_char is not None and (self._current_char.isdigit() or self._current_char=='.')):
            result+=self._current_char
            self.__forward()
        return result
    
    def __word(self):
      result = ""
      while (self._current_char is not None and self._current_char.isalpha()):
            result+=self._current_char
            self.__forward()
      return result
    
    def __symbol(self):
      result = ""
      if self._current_char == ":":
         result += self._current_char
         self.__forward()
         if self._current_char.isspace():
            self.__skip()
         if self._current_char == "=":
            result += self._current_char
            self.__forward()
            return result
      raise BadToken("Bad token")

    def init(self, s:str):
       self._text=s
       self._pos=0
       self._current_char=self._text[self._pos]

    def next(self):
        while self._current_char:
           if self._current_char.isspace():
              self.__skip()
              continue
           if self._current_char.isdigit():
              val = self.__integer()
              return Token(TokenType.NUMBER, val)
           if self._current_char.isalpha():
              val = self.__word()
              if val=="BEGIN":
                 return Token(TokenType.BEGIN, val)
              elif val=="END":
                 return Token(TokenType.END, val)
              else:
                 return Token(TokenType.VAR, val)
           if self._current_char in ["+", "-", "*", "/"]:
              op=self._current_char
              self.__forward()
              return Token(TokenType.OPERATOR, op)
           if self._current_char=="(":
              val=self._current_char
              self.__forward()
              return Token(TokenType.LPAREN, val)
           if self._current_char==")":
              val=self._current_char
              self.__forward()
              return Token(TokenType.RPAREN, val)
           if self._current_char==":":
              val=self.__symbol()
              self.__forward()
              return Token(TokenType.ASSIGN, val)
           if self._current_char==";":
              val=self._current_char
              self.__forward()
              return Token(TokenType.SEMICOLON, val)
           else:
              raise BadToken("Bad token")
        return Token(TokenType.EOL, "")
    

    
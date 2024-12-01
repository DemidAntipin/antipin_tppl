from interpreter.exceptions import MissingOperandError, InterpreterError, BadToken
from interpreter.token import TokenType
from interpreter.lexer import Lexer
from interpreter.ast import BinOp, Number, UnaryOp, Assign, Variable, Begin, End

class Parser():
    def __init__(self):
        self._current_token = None
        self._lexer = Lexer()

    def __check_token(self, type_:TokenType)->None:
        if self._current_token.type_ == type_:
            self._current_token = self._lexer.next()
        #else:
        #    raise SyntaxError("invalid token order")

    def __factor(self):
        token=self._current_token
        if token.type_ == TokenType.VAR:
            self.__check_token(TokenType.VAR)
            if self._current_token.type_ == TokenType.ASSIGN:
                self.__check_token(TokenType.ASSIGN)
                return Assign(token, self.__expr())
            else:
                return Variable(token)
        if token.value == "+":
            self.__check_token(TokenType.OPERATOR)
            return UnaryOp(token, self.__factor())
        if token.value == "-":
            self.__check_token(TokenType.OPERATOR)
            return UnaryOp(token, self.__factor())
        if token.type_ == TokenType.NUMBER:
            self.__check_token(TokenType.NUMBER)
            return Number(token)
        if token.type_ == TokenType.LPAREN:
            self.__check_token(TokenType.LPAREN)
            result=self.__expr()
            self.__check_token(TokenType.RPAREN)
            return result
        if token.type_ == TokenType.BEGIN:
            return self.__begin_block()
        if token.type_ == TokenType.END:
            return self.__end_block()
        raise SyntaxError("invalid error")

    def __term(self):
        result = self.__factor()
        while self._current_token and (self._current_token.type_ == TokenType.OPERATOR):
            if self._current_token.value not in ["*","/"]:
                break
            token=self._current_token
            self.__check_token(TokenType.OPERATOR)
            result = BinOp(result, token, self.__factor())
        return result

    def __expr(self):
        result=self.__term()
        while self._current_token and (self._current_token.type_ == TokenType.OPERATOR):
            #if self._current_token.value not in ["+", "-"]:
            #    break
            token = self._current_token
            self.__check_token(TokenType.OPERATOR)
            result = BinOp(result, token, self.__term())
        return result

    def __begin_block(self):
        self.__check_token(TokenType.BEGIN)
        statements = []
        while self._current_token and self._current_token.type_ != TokenType.END:
            expr=self.__expr()
            statements.append(expr)
            if self._current_token and self._current_token.type_ == TokenType.SEMICOLON:
                self.__check_token(TokenType.SEMICOLON)
        statements.append(self.__expr())
        self.__check_token(TokenType.END)
        return Begin(statements)

    def __end_block(self):
        return End()

    def eval(self, s:str)->BinOp:
        self._lexer.init(s)
        self._current_token=self._lexer.next()
        return self.__expr()
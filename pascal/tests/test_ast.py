import pytest
from interpreter.token import Token
from interpreter.ast import Node, Number, BinOp, UnaryOp, Begin, End, Assign, Variable
from interpreter.lexer import Lexer

@pytest.fixture
def lexer():
    return Lexer()

@pytest.fixture
def num(lexer):
    lexer.init("5")
    token=lexer.next()
    return Number(token)

class TestAst:
    def test_create_node(self):
        Node()

    def test_number_node(self, lexer):
        lexer.init("5")
        token=lexer.next()
        number=Number(token)
        assert str(number)=='Number(Token(TokenType.NUMBER, 5))'

    def test_binop_node(self, num, lexer):
        lexer.init("+")
        op=lexer.next()
        binop=BinOp(num, op, num)
        assert str(binop)=="BinOp+(Number(Token(TokenType.NUMBER, 5)), Number(Token(TokenType.NUMBER, 5)))"
    
    def test_unaryop_node(self, lexer, num):
        lexer.init("-")
        op=lexer.next()
        unop=UnaryOp(op, num)
        assert str(unop)=="UnaryOp-(Number(Token(TokenType.NUMBER, 5)))"

    def test_variable_node(self, lexer):
        lexer.init("x")
        x=lexer.next()
        var=Variable(x)
        assert str(var)=="Variable(x)"

    def test_assign_node(self, lexer, num):
        lexer.init("x")
        x=lexer.next()
        var=Assign(x, num)
        assert str(var)=="Assign(x, Number(Token(TokenType.NUMBER, 5)))"

    def test_begin_node(self):
        statements=list()
        begin=Begin(statements)
        assert str(begin)=="Begin()"

    def test_end_node(self):
        end=End()
        assert str(end)=="End()"



        
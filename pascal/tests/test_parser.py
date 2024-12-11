import pytest
from interpreter.parser import Parser

@pytest.fixture
def parser():
    return Parser()

class TestParser:
    def test_create_parser(self):
        Parser()

    def test_check_token(self, parser):
        with pytest.raises(SyntaxError):
            parser.eval("5 -*-***- 3")

    def test_parse_token(self, parser):
        parsed=parser.eval("5")
        assert str(parsed)=="Number(Token(TokenType.NUMBER, 5))"

    def test_parse_expr(self, parser):
        parsed1=parser.eval("(6-5)/(-(-(-5)))")
        parsed2=parser.eval("+5")
        assert str(parsed1)=="BinOp/(BinOp-(Number(Token(TokenType.NUMBER, 6)), Number(Token(TokenType.NUMBER, 5))), UnaryOp-(UnaryOp-(UnaryOp-(Number(Token(TokenType.NUMBER, 5))))))"
        assert str(parsed2)=="UnaryOp+(Number(Token(TokenType.NUMBER, 5)))"

    def test_parse_var(self, parser):
        var1=parser.eval("x")
        assert str(var1)=="Variable(x)"
        var2=parser.eval("5+x+y+5")
        assert str(var2)=="BinOp+(BinOp+(BinOp+(Number(Token(TokenType.NUMBER, 5)), Variable(x)), Variable(y)), Number(Token(TokenType.NUMBER, 5)))"

    def test_parse_assignment(self, parser):
        parsed=parser.eval("x := 5+5")
        assert str(parsed)=="Assign(x, BinOp+(Number(Token(TokenType.NUMBER, 5)), Number(Token(TokenType.NUMBER, 5))))"

    def test_parse_block(self, parser):
        empty_block=parser.eval("BEGIN END")
        assert str(empty_block)=="Begin(End())"
        with pytest.raises(SyntaxError):
            separator=parser.eval(";")
        block=parser.eval('''BEGIN
                                x := 2+5;
                            END
                          ''')
        assert str(block)=="Begin(Assign(x, BinOp+(Number(Token(TokenType.NUMBER, 2)), Number(Token(TokenType.NUMBER, 5))))End())"
    
    def test_parse_missing_token(self, parser):
        with pytest.raises(SyntaxError):
            parser.eval(" 8 *")
    
    def test_parse_all(self, parser):
        text='''
            BEGIN
                y: = 2;
                BEGIN
                    a := 3;
                    a := a;
                    b := 10 + a + 10 * y / 4;
                    c := a - b
                END;
            x := 11;
            END
        '''
        parsed=parser.eval(text)
        assert str(parsed)=="Begin(Assign(y, Number(Token(TokenType.NUMBER, 2)))Begin(Assign(a, Number(Token(TokenType.NUMBER, 3)))Assign(a, Variable(a))Assign(b, BinOp+(BinOp+(Number(Token(TokenType.NUMBER, 10)), Variable(a)), BinOp/(BinOp*(Number(Token(TokenType.NUMBER, 10)), Variable(y)), Number(Token(TokenType.NUMBER, 4)))))Assign(c, BinOp-(Variable(a), Variable(b)))End())Assign(x, Number(Token(TokenType.NUMBER, 11)))End())"
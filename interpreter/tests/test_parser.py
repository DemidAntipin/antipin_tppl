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
        parser.eval("5")

    def test_parse_expr(self, parser):
        parser.eval("(6-5)/(-(-(-5)))")
        parser.eval("+5")

    def test_parse_var(self, parser):
        parser.eval("x")

    def test_parse_assignment(self, parser):
        parser.eval("x := 5+5")

    def test_parse_block(self, parser):
        parser.eval("BEGIN END")
    
    def test_parse_fail(self, parser):
        with pytest.raises(SyntaxError):
            parser.eval(";")
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
        parser.eval(text)
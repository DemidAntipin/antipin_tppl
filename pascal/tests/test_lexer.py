import pytest
from interpreter.lexer import Lexer
from interpreter.exceptions import BadToken
from interpreter.token import Token, TokenType

@pytest.fixture
def lexer():
    return Lexer()

class TestLexer:
    def test_create_lexer(self):
        Lexer()

    def test_init_lexer(self, lexer):
        lexer.init("test_string")

    def test_token(self, lexer):
        lexer.init("some_token")
        token=lexer.next()
        string=str(token)
        assert isinstance(token, Token)

    def test_int_token(self, lexer):
        lexer.init("5")
        token=lexer.next()
        assert token.type_==TokenType.NUMBER

    def test_EOL_token(self, lexer):
        lexer.init("5")
        token=lexer.next()
        token=lexer.next()
        assert token.type_==TokenType.EOL

    def test_long_int_token(self, lexer):
        lexer.init("5245")
        token=lexer.next()
        assert token.type_==TokenType.NUMBER

    def test_float_token(self, lexer):
        lexer.init("5.5")
        token=lexer.next()
        assert token.type_==TokenType.NUMBER

    def test_more_tokens(self, lexer):
        lexer.init("425            3.63")
        token1=lexer.next()
        token2=lexer.next()
        assert token1.type_==TokenType.NUMBER
        assert token2.type_==TokenType.NUMBER

    def test_paren_tokens(self, lexer):
        lexer.init("(5326)")
        lparen=lexer.next()
        num=lexer.next()
        rparen=lexer.next()
        assert lparen.type_==TokenType.LPAREN
        assert num.type_==TokenType.NUMBER
        assert rparen.type_==TokenType.RPAREN

    def test_word_tokens(self, lexer):
        lexer.init("variable")
        var=lexer.next()
        assert var.type_==TokenType.VAR
    
    def test_block_tokens(self, lexer):
        lexer.init("BEGIN END")
        begin=lexer.next()
        end=lexer.next()
        assert begin.type_==TokenType.BEGIN
        assert end.type_==TokenType.END
    
    def test_assign_token(self, lexer):
        lexer.init(":=    :     =   :?")
        token1=lexer.next()
        token2=lexer.next()
        assert token1.type_==TokenType.ASSIGN
        assert token2.type_==TokenType.ASSIGN
        with pytest.raises(BadToken):
            lexer.next()

    def test_operator_token(self, lexer):
        lexer.init("+ - * / ^")
        add=lexer.next()
        sub=lexer.next()
        mul=lexer.next()
        div=lexer.next()
        assert add.type_==TokenType.OPERATOR
        assert sub.type_==TokenType.OPERATOR
        assert mul.type_==TokenType.OPERATOR
        assert div.type_==TokenType.OPERATOR
        with pytest.raises(BadToken):
            lexer.next()

    def test_semicolon_token(self, lexer):
        lexer.init(";")
        s=lexer.next()
        assert s.type_==TokenType.SEMICOLON

    def test_all_tokens(self, lexer):
        text='''
            BEGIN
                x := 2 * (5 - 5.5);
                y := 5 / -4;
            END
        '''
        lexer.init(text)
        token=lexer.next()
        while token.type_!=TokenType.EOL:
            token=lexer.next()
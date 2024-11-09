import pytest
from notation import Notation
from notation.exceptions import MissingOperandError, NotationError, BadToken
from notation.token import Token, TokenType

@pytest.fixture
def notate():
    return Notation()

class TestNotation:
    def test_notation(self):
        Notation()

    def test_token_types(self):
        IntegerToken = Token(TokenType.NUMBER, 2)
        OperatorToken = Token(TokenType.OPERATOR, '+')
        assert IntegerToken.type_ == TokenType.NUMBER
        assert OperatorToken.type_ == TokenType.OPERATOR

    def test_token_to_str(self):
        token = Token(TokenType.NUMBER, "42")
        assert str(token) == f"Token({TokenType.NUMBER}, 42)"

    @pytest.mark.parametrize(
        "notation, result",
        [
            ("+ - 13 4 55", "( ( 13 - 4 ) + 55 )"),
            ("+ 2 * 2 - 2 1", "( 2 + ( 2 * ( 2 - 1 ) ) )"),
            ("+ + 10 20 30", "( ( 10 + 20 ) + 30 )"),
            ("/ + 3 10 * + 2 3 - 3 5", "( ( 3 + 10 ) / ( ( 2 + 3 ) * ( 3 - 5 ) ) )")
        ]
    )
    def test_eval(self, notate, notation, result):
        assert notate.to_infix(notation) == result

    def test_bad_token(self, notate):
        notation="^"
        with pytest.raises(BadToken):
            notate.to_infix(notation)

    def test_missing_operands(self, notate):
        notation1="+"
        notation2="- - 1 2"
        with pytest.raises(MissingOperandError):
            notate.to_infix(notation1)
        with pytest.raises(MissingOperandError):
            notate.to_infix(notation2)

    def test_notation_error(self, notate):
        notation="- - 2 2 2 2 2 2"
        with pytest.raises(NotationError):
            notate.to_infix(notation)

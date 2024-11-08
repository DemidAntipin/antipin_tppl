import pytest
from notation import Interpreter
from notation.exceptions import MissingOperandError, InterpreterError, BadToken
from notation.token import Token, TokenType

class TestNotation:
    def test_interpreter_init(self):
        Interpreter()

    def test_token_types(self):
        IntegerToken = Token(TokenType.INTEGER, 2)
        OperatorToken = Token(TokenType.OPERATOR, '+')
        SpaceToken = Token(TokenType.SPACE, ' ')
        assert IntegerToken.type_ == TokenType.INTEGER
        assert OperatorToken.type_ == TokenType.OPERATOR
        assert SpaceToken.type_ == TokenType.SPACE

    def test_token_to_str(self):
        token = Token(TokenType.INTEGER, "42")
        assert str(token) == f"Token({TokenType.INTEGER}, 42)"

    @pytest.mark.parametrize(
        "notation, result",
        [
            ("+ - 13 4 55", 64.0),
            ("+ 2 * 2 - 2 1", 4.0),
            ("+ + 10 20 30", 60.0),
            ("/ + 3 10 * + 2 3 - 3 5", -1.3)
        ]
    )
    def test_eval(self, notation, result):
        interpreter = Interpreter()
        assert interpreter.eval(notation) == pytest.approx(result, 0.01)

    def test_bad_token(self):
        interpreter = Interpreter()
        notation="^"
        with pytest.raises(BadToken):
            interpreter.eval(notation)

    def test_missing_operands(self):
        interpreter = Interpreter()
        notation1="+"
        notation2="- - 1 2"
        with pytest.raises(MissingOperandError):
            interpreter.eval(notation1)
        with pytest.raises(MissingOperandError):
            interpreter.eval(notation2)

    def test_zero_division(self):
        interpreter = Interpreter()
        notation="/ 2 0"
        with pytest.raises(ZeroDivisionError):
            interpreter.eval(notation)

    def test_interpreter_error(self):
        interpreter = Interpreter()
        notation="- - 2 2 2 2 2 2"
        with pytest.raises(InterpreterError):
            interpreter.eval(notation)

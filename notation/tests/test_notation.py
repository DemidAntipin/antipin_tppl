import pytest
from notation import isOperand, isOperator, calculate
from notation.exceptions import MissingOperandError, TooManyOperandsError, UnknownOperatorError

class TestNotation:

    def test_operand(self):
        operand='25'
        not_operand='+'
        assert isOperand(operand)
        assert not isOperand(not_operand)

    def test_operator(self):
        known_operator='+'
        unknown_operator='^'
        assert isOperator(known_operator)
        with pytest.raises(UnknownOperatorError):
            isOperator(unknown_operator)

    @pytest.mark.parametrize(
        "notation, result",
        [
            ("+ - 13 4 55", 64.0),
            ("+ 2 * 2 - 2 1", 4.0),
            ("+ + 10 20 30", 60.0),
            ("/ + 3 10 * + 2 3 - 3 5", -1.3)
        ]
    )
    def test_calculation(self, notation, result):
        assert calculate(notation) == pytest.approx(result, 0.1)

    def test_missing_operands(self):
        notation1="+"
        notation2="- - 1 2"
        with pytest.raises(MissingOperandError):
            calculate(notation1)
        with pytest.raises(MissingOperandError):
            calculate(notation2)

    def test_zero_division(self):
        notation="/ 2 0"
        with pytest.raises(ZeroDivisionError):
            calculate(notation)

    def test_many_operands(self):
        notation="- - 2 2 2 2 2 2"
        with pytest.raises(TooManyOperandsError):
            calculate(notation)

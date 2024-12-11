import pytest
from interpreter import Interpreter, NodeVisitor
import io
import sys

@pytest.fixture
def inter():
    return Interpreter()

class TestInterpreter:
    def test_create_interpreter(self):
        Interpreter()

    def test_nodevisitor(self):
        n=NodeVisitor()
        n.visit()

    def test_blocks(self, inter):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        inter.eval('''
            BEGIN
            END
        ''')
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        assert len(output)==0

    def test_assignments(self, inter):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        inter.eval('''
            BEGIN
	            x:= 2 + 3 * (2 + 3);
                y:= 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1));
            END
        ''')
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        assert "x: 17" in output
        assert "y: 11"

    def test_inner_blocks(self, inter):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        inter.eval('''
            BEGIN
                y: = 2;
                BEGIN
                    a := 3;
                    a := -a;
                    b := +10 - a + 10 * y / 4;
                    c := -a - b
                END;
                x := 11;
            END
        ''')
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        assert "a: -3.0" in output
        assert "b: 18.0" in output
        assert "c: -15.0" in output
        assert "y: 2.0" in output
        assert "x: 11.0" in output

    def test_undefined_var(self, inter):
        with pytest.raises(NameError):
            inter.eval('''
                BEGIN
                       x := y;
                END
            ''')
import sys
import os
import pytest

# ensure project root is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from operations import evaluate_expression, calculate


def test_evaluate_simple_add():
    assert evaluate_expression('2+3') == 5


def test_evaluate_precedence():
    assert evaluate_expression('2+3*4') == 14


def test_evaluate_division():
    assert evaluate_expression('5/2') == 2.5


def test_evaluate_unary():
    assert evaluate_expression('-3+5') == 2


def test_evaluate_invalid():
    with pytest.raises(Exception):
        evaluate_expression('2 + unknown')


def test_calculate_add():
    assert calculate(10, 5, '+') == 15


def test_calculate_div():
    assert calculate(11, 2, '/') == 5.5


def test_calculate_invalid_op():
    with pytest.raises(ValueError):
        calculate(1, 2, '^')

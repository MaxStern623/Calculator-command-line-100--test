"""
Unit tests for the calculation module.

This module contains comprehensive tests for Calculation and CalculationFactory
classes with parameterized tests and edge case coverage.
"""

from datetime import datetime

import pytest

from calculation import Calculation, CalculationFactory
from operation import (
    AddOperation,
    DivideOperation,
    MultiplyOperation,
    SubtractOperation,
)


class TestCalculation:
    """Test cases for Calculation class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.add_op = AddOperation()
        self.divide_op = DivideOperation()

    def test_init(self):
        """Test calculation initialization."""
        calc = Calculation(5, 3, self.add_op)
        assert calc.a == 5
        assert calc.b == 3
        assert calc.operation == self.add_op
        assert isinstance(calc.timestamp, datetime)
        assert calc._result is None
        assert calc._executed is False

    def test_execute_once(self):
        """Test that calculation executes correctly."""
        calc = Calculation(5, 3, self.add_op)
        result = calc.execute()
        assert result == 8
        assert calc._executed is True
        assert calc._result == 8

    def test_execute_multiple_times(self):
        """Test that multiple executions return same result."""
        calc = Calculation(5, 3, self.add_op)
        result1 = calc.execute()
        result2 = calc.execute()
        assert result1 == result2 == 8

    def test_result_property(self):
        """Test result property executes calculation if needed."""
        calc = Calculation(10, 2, self.divide_op)
        assert calc._executed is False
        result = calc.result
        assert result == 5.0
        assert calc._executed is True

    def test_execute_with_error(self):
        """Test calculation execution with division by zero."""
        calc = Calculation(10, 0, self.divide_op)
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            calc.execute()

    @pytest.mark.parametrize(
        "a, b, operation_class, expected",
        [
            (5, 3, AddOperation, "5 + 3 = 8"),
            (10, 2, SubtractOperation, "10 - 2 = 8"),
            (4, 7, MultiplyOperation, "4 * 7 = 28"),
            (15, 3, DivideOperation, "15 / 3 = 5.0"),
            (-5, 3, AddOperation, "-5 + 3 = -2"),
            (0, 5, MultiplyOperation, "0 * 5 = 0"),
        ],
    )
    def test_str_representation_executed(self, a, b, operation_class, expected):
        """Test string representation after execution."""
        calc = Calculation(a, b, operation_class())
        calc.execute()
        assert str(calc) == expected

    def test_str_representation_not_executed(self):
        """Test string representation before execution."""
        calc = Calculation(5, 3, self.add_op)
        assert str(calc) == "5 + 3 = ?"

    def test_repr_representation(self):
        """Test developer representation."""
        calc = Calculation(5, 3, self.add_op)
        assert repr(calc) == "Calculation(5, 3, AddOperation)"

    @pytest.mark.parametrize(
        "operation_class, expected_symbol",
        [
            (AddOperation, "+"),
            (SubtractOperation, "-"),
            (MultiplyOperation, "*"),
            (DivideOperation, "/"),
        ],
    )
    def test_operation_symbols(self, operation_class, expected_symbol):
        """Test operation symbols in string representation."""
        calc = Calculation(1, 1, operation_class())
        calc.execute()
        assert expected_symbol in str(calc)


class TestCalculationFactory:
    """Test cases for CalculationFactory class."""

    @pytest.mark.parametrize(
        "operation_type, a, b, expected_result",
        [
            ("add", 5, 3, 8),
            ("subtract", 10, 4, 6),
            ("multiply", 3, 7, 21),
            ("divide", 12, 3, 4.0),
            ("+", 2, 8, 10),
            ("-", 15, 5, 10),
            ("*", 4, 6, 24),
            ("/", 20, 4, 5.0),
        ],
    )
    def test_create_calculation_valid_operations(
        self, operation_type, a, b, expected_result
    ):
        """Test factory creates correct calculations for valid operations."""
        calc = CalculationFactory.create_calculation(a, b, operation_type)
        assert isinstance(calc, Calculation)
        assert calc.a == a
        assert calc.b == b
        result = calc.execute()
        assert result == expected_result

    @pytest.mark.parametrize(
        "operation_type",
        [
            "ADD",
            "SUBTRACT",
            "MULTIPLY",
            "DIVIDE",  # uppercase
            " add ",
            " + ",  # with whitespace
            "Add",
            "Subtract",  # mixed case
        ],
    )
    def test_create_calculation_case_insensitive(self, operation_type):
        """Test factory handles case insensitive and whitespace in operations."""
        calc = CalculationFactory.create_calculation(5, 3, operation_type)
        assert isinstance(calc, Calculation)

    @pytest.mark.parametrize(
        "invalid_operation", ["invalid", "modulo", "%", "", " ", "power", "^", None]
    )
    def test_create_calculation_invalid_operations(self, invalid_operation):
        """Test factory raises error for invalid operations."""
        with pytest.raises(ValueError, match="Unsupported operation"):
            CalculationFactory.create_calculation(5, 3, invalid_operation)

    def test_create_calculation_with_floats(self):
        """Test factory works with floating point numbers."""
        calc = CalculationFactory.create_calculation(2.5, 1.5, "add")
        result = calc.execute()
        assert result == 4.0

    def test_create_calculation_with_negative_numbers(self):
        """Test factory works with negative numbers."""
        calc = CalculationFactory.create_calculation(-5, -3, "multiply")
        result = calc.execute()
        assert result == 15

    def test_create_calculation_division_by_zero(self):
        """Test factory creates calculation that can handle division by zero."""
        calc = CalculationFactory.create_calculation(10, 0, "divide")
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            calc.execute()

    def test_error_message_contains_valid_operations(self):
        """Test that error message shows valid operations."""
        try:
            CalculationFactory.create_calculation(1, 2, "invalid")
        except ValueError as e:
            error_msg = str(e)
            assert "add" in error_msg
            assert "+" in error_msg
            assert "Valid operations are:" in error_msg

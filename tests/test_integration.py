"""
Integration tests for the calculator application.

These tests verify that all components work together correctly.
"""

from unittest.mock import patch

import pytest

from calculation import CalculationFactory
from calculator import Calculator
from operation import AddOperation


class TestCalculatorIntegration:
    """Integration tests for the complete calculator system."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = Calculator()

    def test_full_calculation_workflow(self):
        """Test complete calculation workflow from input to history."""
        # Simulate user performing calculations
        calculations = ["5 + 3", "10 - 4", "6 * 7", "20 / 4"]

        expected_results = ["5 + 3 = 8", "10 - 4 = 6", "6 * 7 = 42", "20 / 4 = 5.0"]

        with patch("builtins.print"):
            for calc_input in calculations:
                self.calculator._handle_calculation(calc_input)

        # Verify all calculations are in history
        assert len(self.calculator.history) == 4

        history = self.calculator.history.get_history()
        for i, expected in enumerate(expected_results):
            assert str(history[i]) == expected

    def test_calculator_factory_integration(self):
        """Test integration between calculator and calculation factory."""
        # Test that calculator uses factory correctly
        with patch("builtins.print"):
            self.calculator._handle_calculation("7 + 2")

        last_calc = self.calculator.history.get_last_calculation()
        assert last_calc is not None
        assert last_calc.a == 7
        assert last_calc.b == 2
        assert isinstance(last_calc.operation, AddOperation)
        assert last_calc.result == 9

    def test_error_handling_integration(self):
        """Test error handling across all components."""
        test_cases = [
            "5 / 0",  # Division by zero
            "abc + 3",  # Invalid number
            "5 % 3",  # Invalid operation
            "5 +",  # Invalid format (prints 2 messages)
        ]

        with patch("builtins.print") as mock_print:
            for test_input in test_cases:
                self.calculator._handle_calculation(test_input)

        # No calculations should be added to history due to errors
        assert len(self.calculator.history) == 0

        # Verify error messages were printed (5 total: 4 single errors + 1 extra for format)
        assert mock_print.call_count >= len(test_cases)

    @patch(
        "builtins.input", side_effect=["5 + 3", "10 * 2", "history", "clear", "exit"]
    )
    @patch("builtins.print")
    def test_complete_user_session(self, mock_print, mock_input):
        """Test complete user session with multiple commands."""
        self.calculator.start()

        # Verify calculator processed all commands
        assert not self.calculator.running

        # History should be cleared
        assert len(self.calculator.history) == 0

    def test_calculator_state_consistency(self):
        """Test that calculator maintains consistent state."""
        # Perform several operations
        operations = ["1 + 1", "2 * 3", "10 / 2"]

        with patch("builtins.print"):
            for op in operations:
                self.calculator._handle_calculation(op)

        # Verify state consistency
        assert len(self.calculator.history) == 3

        # Get last calculation and verify it's accessible
        last_calc = self.calculator.history.get_last_calculation()
        assert last_calc is not None
        assert last_calc.result == 5.0  # 10 / 2

        # Verify history order is maintained
        history = self.calculator.history.get_history()
        assert str(history[0]) == "1 + 1 = 2"
        assert str(history[1]) == "2 * 3 = 6"
        assert str(history[2]) == "10 / 2 = 5.0"


class TestFactoryOperationIntegration:
    """Test integration between factory and operations."""

    @pytest.mark.parametrize(
        "operation_str, a, b, expected",
        [
            ("add", 5, 3, 8),
            ("+", 5, 3, 8),
            ("subtract", 10, 3, 7),
            ("-", 10, 3, 7),
            ("multiply", 4, 6, 24),
            ("*", 4, 6, 24),
            ("divide", 12, 3, 4.0),
            ("/", 12, 3, 4.0),
        ],
    )
    def test_factory_creates_working_calculations(self, operation_str, a, b, expected):
        """Test that factory creates calculations that execute correctly."""
        calc = CalculationFactory.create_calculation(a, b, operation_str)
        result = calc.execute()
        assert result == expected

    def test_factory_error_propagation(self):
        """Test that operation errors propagate through factory-created calculations."""
        calc = CalculationFactory.create_calculation(5, 0, "divide")

        with pytest.raises(ValueError, match="Division by zero"):
            calc.execute()


class TestEndToEndScenarios:
    """End-to-end test scenarios."""

    def test_scientific_calculation_sequence(self):
        """Test a sequence of related calculations."""
        calculator = Calculator()

        # Simulate calculating area of a rectangle step by step
        calculations = [
            "10 * 5",  # length * width = 50
            "50 * 2",  # area * 2 = 100
            "100 / 4",  # divide by 4 = 25
        ]

        with patch("builtins.print"):
            for calc in calculations:
                calculator._handle_calculation(calc)

        # Verify final result
        last_calc = calculator.history.get_last_calculation()
        assert last_calc.result == 25.0

        # Verify all intermediate results are preserved
        history = calculator.history.get_history()
        assert len(history) == 3
        assert history[0].result == 50
        assert history[1].result == 100
        assert history[2].result == 25.0

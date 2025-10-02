"""
Unit tests for the calculator module.

This module contains comprehensive tests for Calculator, CalculatorHistory,
and InputValidator classes with parameterized tests and edge case coverage.
"""

from unittest.mock import Mock, patch

import pytest

from calculation import Calculation
from calculator import Calculator, CalculatorHistory, InputValidator
from operation import AddOperation


class TestCalculatorHistory:
    """Test cases for CalculatorHistory class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.history = CalculatorHistory()

    def test_init_empty_history(self):
        """Test history initializes empty."""
        assert len(self.history) == 0
        assert self.history.get_history() == []
        assert self.history.get_last_calculation() is None

    def test_add_calculation(self):
        """Test adding calculations to history."""
        calc = Calculation(5, 3, AddOperation())
        self.history.add_calculation(calc)

        assert len(self.history) == 1
        assert self.history.get_last_calculation() == calc
        assert calc in self.history.get_history()

    def test_add_multiple_calculations(self):
        """Test adding multiple calculations maintains order."""
        calc1 = Calculation(5, 3, AddOperation())
        calc2 = Calculation(10, 2, AddOperation())

        self.history.add_calculation(calc1)
        self.history.add_calculation(calc2)

        assert len(self.history) == 2
        assert self.history.get_last_calculation() == calc2
        history_list = self.history.get_history()
        assert history_list[0] == calc1
        assert history_list[1] == calc2

    def test_clear_history(self):
        """Test clearing history."""
        calc = Calculation(5, 3, AddOperation())
        self.history.add_calculation(calc)
        assert len(self.history) == 1

        self.history.clear_history()
        assert len(self.history) == 0
        assert self.history.get_history() == []
        assert self.history.get_last_calculation() is None

    def test_get_history_returns_copy(self):
        """Test that get_history returns a copy, not reference."""
        calc = Calculation(5, 3, AddOperation())
        self.history.add_calculation(calc)

        history_copy = self.history.get_history()
        history_copy.clear()

        # Original history should be unchanged
        assert len(self.history) == 1


class TestInputValidator:
    """Test cases for InputValidator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = InputValidator()

    @pytest.mark.parametrize(
        "input_str, expected_type, expected_value",
        [
            ("5", int, 5),
            ("-3", int, -3),
            ("0", int, 0),
            ("5.5", float, 5.5),
            ("-2.7", float, -2.7),
            ("0.0", float, 0.0),
            ("1e2", float, 100.0),
            ("1.5e-1", float, 0.15),
            ("  42  ", int, 42),  # with whitespace
            (" -3.14 ", float, -3.14),
        ],
    )
    def test_validate_number_valid_inputs(
        self, input_str, expected_type, expected_value
    ):
        """Test number validation with valid inputs."""
        result = self.validator.validate_number(input_str)
        assert isinstance(result, expected_type)
        assert result == expected_value

    @pytest.mark.parametrize(
        "invalid_input",
        ["", "   ", "abc", "5.5.5", "1 2", "five", "1+2", ".", "-", "e5", "5e"],
    )
    def test_validate_number_invalid_inputs(self, invalid_input):
        """Test number validation with invalid inputs."""
        with pytest.raises(ValueError):
            self.validator.validate_number(invalid_input)

    def test_validate_number_empty_string_specific_message(self):
        """Test specific error message for empty string."""
        with pytest.raises(ValueError, match="Empty input is not a valid number"):
            self.validator.validate_number("")

    @pytest.mark.parametrize(
        "operation, expected",
        [
            ("add", "add"),
            ("ADD", "ADD"),
            ("  multiply  ", "multiply"),
            ("+", "+"),
            ("-", "-"),
            ("*", "*"),
            ("/", "/"),
        ],
    )
    def test_validate_operation_valid_inputs(self, operation, expected):
        """Test operation validation with valid inputs."""
        result = self.validator.validate_operation(operation)
        assert result == expected

    @pytest.mark.parametrize(
        "invalid_operation", ["modulo", "%", "^", "power", "invalid", "123"]
    )
    def test_validate_operation_invalid_inputs(self, invalid_operation):
        """Test operation validation with invalid inputs."""
        with pytest.raises(ValueError, match="Unsupported operation"):
            self.validator.validate_operation(invalid_operation)

    @pytest.mark.parametrize("empty_operation", ["", "   "])
    def test_validate_operation_empty_inputs(self, empty_operation):
        """Test operation validation with empty inputs."""
        with pytest.raises(ValueError, match="Operation cannot be empty"):
            self.validator.validate_operation(empty_operation)

    def test_validate_operation_empty_string_specific_message(self):
        """Test specific error message for empty operation."""
        with pytest.raises(ValueError, match="Operation cannot be empty"):
            self.validator.validate_operation("")


class TestCalculator:
    """Test cases for Calculator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = Calculator()

    def test_init(self):
        """Test calculator initialization."""
        assert isinstance(self.calculator.history, CalculatorHistory)
        assert isinstance(self.calculator.validator, InputValidator)
        assert self.calculator.running is False

    @patch("builtins.input")
    @patch("builtins.print")
    def test_process_command_exit(self, mock_print, mock_input):
        """Test exit command processing."""
        self.calculator.running = True
        self.calculator._process_command("exit")
        assert self.calculator.running is False
        mock_print.assert_called_with("Thank you for using the calculator. Goodbye!")

    @pytest.mark.parametrize("exit_command", ["exit", "quit", "q", "EXIT", "QUIT", "Q"])
    def test_process_command_exit_variations(self, exit_command):
        """Test various exit command variations."""
        self.calculator.running = True
        with patch("builtins.print"):
            self.calculator._process_command(exit_command)
        assert self.calculator.running is False

    @patch("builtins.print")
    def test_process_command_help(self, mock_print):
        """Test help command processing."""
        self.calculator._process_command("help")
        # Check that help text was printed
        assert mock_print.called
        printed_text = str(mock_print.call_args)
        assert "Calculator Help" in printed_text

    @pytest.mark.parametrize("help_command", ["help", "h", "?", "HELP", "H"])
    def test_process_command_help_variations(self, help_command):
        """Test various help command variations."""
        with patch("builtins.print") as mock_print:
            self.calculator._process_command(help_command)
        assert mock_print.called

    @patch("builtins.print")
    def test_process_command_history_empty(self, mock_print):
        """Test history command with empty history."""
        self.calculator._process_command("history")
        mock_print.assert_called_with("No calculations in history.")

    @patch("builtins.print")
    def test_process_command_history_with_calculations(self, mock_print):
        """Test history command with calculations."""
        # Add a calculation to history
        calc = Calculation(5, 3, AddOperation())
        calc.execute()
        self.calculator.history.add_calculation(calc)

        self.calculator._process_command("history")

        # Check that history was printed
        assert mock_print.called
        printed_calls = [str(call) for call in mock_print.call_args_list]
        printed_text = " ".join(printed_calls)
        assert "Calculation History" in printed_text
        assert "5 + 3 = 8" in printed_text

    @patch("builtins.print")
    def test_process_command_clear_history(self, mock_print):
        """Test clear history command."""
        # Add calculations
        calc1 = Calculation(5, 3, AddOperation())
        calc2 = Calculation(10, 2, AddOperation())
        self.calculator.history.add_calculation(calc1)
        self.calculator.history.add_calculation(calc2)

        self.calculator._process_command("clear")

        assert len(self.calculator.history) == 0
        mock_print.assert_called_with("Cleared 2 calculation(s) from history.")

    @patch("builtins.print")
    def test_handle_calculation_valid(self, mock_print):
        """Test valid calculation handling."""
        self.calculator._handle_calculation("5 + 3")

        # Check calculation was added to history
        assert len(self.calculator.history) == 1
        last_calc = self.calculator.history.get_last_calculation()
        assert str(last_calc) == "5 + 3 = 8"

        # Check result was printed
        mock_print.assert_called_with("Result: 5 + 3 = 8")

    @pytest.mark.parametrize(
        "expression, expected_result",
        [
            ("5 + 3", "5 + 3 = 8"),
            ("10 - 4", "10 - 4 = 6"),
            ("3 * 7", "3 * 7 = 21"),
            ("15 / 3", "15 / 3 = 5.0"),
            ("2.5 + 1.5", "2.5 + 1.5 = 4.0"),
            ("-5 + 3", "-5 + 3 = -2"),
        ],
    )
    def test_handle_calculation_various_operations(self, expression, expected_result):
        """Test calculation handling with various operations."""
        with patch("builtins.print") as mock_print:
            self.calculator._handle_calculation(expression)

        last_calc = self.calculator.history.get_last_calculation()
        assert str(last_calc) == expected_result
        mock_print.assert_called_with(f"Result: {expected_result}")

    @patch("builtins.print")
    def test_handle_calculation_invalid_format(self, mock_print):
        """Test calculation with invalid format."""
        self.calculator._handle_calculation("5 +")  # Missing second operand

        # No calculation should be added to history
        assert len(self.calculator.history) == 0

        # Error message should be printed (check both calls)
        printed_calls = [str(call) for call in mock_print.call_args_list]
        printed_text = " ".join(printed_calls)
        assert (
            "Please enter calculation in format" in printed_text
            or "Example: 5 + 3 or 10 / 2" in printed_text
        )

    @patch("builtins.print")
    def test_handle_calculation_division_by_zero(self, mock_print):
        """Test calculation with division by zero."""
        self.calculator._handle_calculation("5 / 0")

        # No calculation should be added to history
        assert len(self.calculator.history) == 0

        # Error message should be printed
        printed_text = str(mock_print.call_args)
        assert "Division by zero" in printed_text

    @patch("builtins.print")
    def test_handle_calculation_invalid_number(self, mock_print):
        """Test calculation with invalid number."""
        self.calculator._handle_calculation("abc + 3")

        # No calculation should be added to history
        assert len(self.calculator.history) == 0

        # Error message should be printed
        printed_text = str(mock_print.call_args)
        assert "Input Error" in printed_text

    @patch("builtins.print")
    def test_handle_calculation_invalid_operation(self, mock_print):
        """Test calculation with invalid operation."""
        self.calculator._handle_calculation("5 % 3")

        # No calculation should be added to history
        assert len(self.calculator.history) == 0

        # Error message should be printed
        printed_text = str(mock_print.call_args)
        assert "Input Error" in printed_text

    @patch("builtins.input", side_effect=["5 + 3", "exit"])
    @patch("builtins.print")
    def test_start_calculator_basic_flow(self, mock_print, mock_input):
        """Test basic calculator startup flow."""
        self.calculator.start()

        # Calculator should have processed the calculation
        assert len(self.calculator.history) == 1
        assert not self.calculator.running

    @patch("builtins.input", side_effect=KeyboardInterrupt())
    @patch("builtins.print")
    def test_start_calculator_keyboard_interrupt(self, mock_print, mock_input):
        """Test calculator handles keyboard interrupt gracefully."""
        self.calculator.start()

        # Should exit gracefully (running state is set to False after KeyboardInterrupt)
        # The running flag is set to True at start, then False when interrupted
        assert not self.calculator.running

    @patch("builtins.input", side_effect=EOFError())
    @patch("builtins.print")
    def test_start_calculator_eof_error(self, mock_print, mock_input):
        """Test calculator handles EOF error gracefully."""
        self.calculator.start()

        # Should exit gracefully and print exit message
        assert not self.calculator.running
        mock_print.assert_called_with("\n\nExiting calculator...")

    @patch("builtins.input", side_effect=RuntimeError("Test error"))
    @patch("builtins.print")
    def test_start_calculator_unexpected_error(self, mock_print, mock_input):
        """Test calculator handles unexpected errors."""
        self.calculator.start()

        # Should handle the unexpected error and continue (in this case exit due to error)
        assert mock_print.called
        printed_calls = [str(call) for call in mock_print.call_args_list]
        printed_text = " ".join(printed_calls)
        assert "Unexpected error" in printed_text

    @patch("calculation.CalculationFactory.create_calculation")
    @patch("builtins.print")
    def test_handle_calculation_unexpected_error(self, mock_print, mock_create):
        """Test _handle_calculation with unexpected error during calculation creation."""
        # Mock factory to raise unexpected error
        mock_create.side_effect = RuntimeError("Unexpected factory error")

        self.calculator._handle_calculation("5 + 3")

        # Should print error message and not add to history
        assert len(self.calculator.history) == 0
        mock_print.assert_called_with(
            "Error processing calculation: Unexpected factory error"
        )

    @patch("calculation.Calculation.execute")
    @patch("calculation.CalculationFactory.create_calculation")
    @patch("builtins.print")
    def test_handle_calculation_execution_unexpected_error(
        self, mock_print, mock_create, mock_execute
    ):
        """Test _handle_calculation with unexpected error during calculation execution."""
        # Mock calculation execution to raise unexpected error
        mock_calc = Mock()
        mock_create.return_value = mock_calc
        mock_execute.side_effect = RuntimeError("Execution error")
        mock_calc.execute = mock_execute

        self.calculator._handle_calculation("5 + 3")

        # Should print error message and not add to history
        assert len(self.calculator.history) == 0
        mock_print.assert_called_with("Unexpected calculation error: Execution error")

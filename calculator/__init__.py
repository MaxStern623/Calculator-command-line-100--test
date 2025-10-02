"""
Calculator module - Main calculator application with REPL interface.

This module provides a professional calculator with history, help commands,
and comprehensive error handling.
"""

from typing import List, Union, Optional
from calculation import Calculation, CalculationFactory

Number = Union[int, float]


class CalculatorHistory:
    """Manages calculation history for the calculator."""
    
    def __init__(self):
        """Initialize empty history."""
        self._history: List[Calculation] = []
    
    def add_calculation(self, calculation: Calculation) -> None:
        """Add a calculation to history."""
        self._history.append(calculation)
    
    def get_history(self) -> List[Calculation]:
        """Get all calculations in history."""
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear all history."""
        self._history.clear()
    
    def get_last_calculation(self) -> Optional[Calculation]:
        """Get the most recent calculation."""
        return self._history[-1] if self._history else None
    
    def __len__(self) -> int:
        """Get number of calculations in history."""
        return len(self._history)


class InputValidator:
    """Validates user input for the calculator."""
    
    @staticmethod
    def validate_number(value: str) -> Number:
        """
        Validate and convert string to number.
        
        Args:
            value: String representation of number
            
        Returns:
            Converted number (int or float)
            
        Raises:
            ValueError: If string cannot be converted to number
        """
        value = value.strip()
        if not value:
            raise ValueError("Empty input is not a valid number")
        
        try:
            # Try integer first
            if '.' not in value and 'e' not in value.lower():
                return int(value)
            else:
                return float(value)
        except ValueError:
            raise ValueError(f"'{value}' is not a valid number")
    
    @staticmethod
    def validate_operation(operation: str) -> str:
        """
        Validate operation string.
        
        Args:
            operation: Operation string
            
        Returns:
            Validated operation string
            
        Raises:
            ValueError: If operation is not supported
        """
        operation = operation.strip()
        if not operation:
            raise ValueError("Operation cannot be empty")
        
        valid_operations = ['add', 'subtract', 'multiply', 'divide', '+', '-', '*', '/']
        if operation.lower() not in valid_operations:
            raise ValueError(f"Unsupported operation: '{operation}'. "
                           f"Valid operations: {valid_operations}")
        
        return operation


class Calculator:
    """Main calculator class with REPL interface."""
    
    def __init__(self):
        """Initialize calculator with empty history."""
        self.history = CalculatorHistory()
        self.validator = InputValidator()
        self.running = False
    
    def start(self) -> None:
        """Start the calculator REPL interface."""
        self.running = True
        self._print_welcome()
        
        while self.running:
            try:
                user_input = input("\nCalculator> ").strip()
                if not user_input:
                    continue
                
                self._process_command(user_input)
                
            except KeyboardInterrupt:
                print("\n\nExiting calculator...")
                break
            except EOFError:
                print("\n\nExiting calculator...")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
    
    def _process_command(self, command: str) -> None:
        """Process user command."""
        command_lower = command.lower()
        
        if command_lower in ['exit', 'quit', 'q']:
            self._handle_exit()
        elif command_lower in ['help', 'h', '?']:
            self._handle_help()
        elif command_lower in ['history', 'hist']:
            self._handle_history()
        elif command_lower in ['clear', 'cls']:
            self._handle_clear_history()
        else:
            self._handle_calculation(command)
    
    def _handle_calculation(self, expression: str) -> None:
        """Handle calculation input."""
        try:
            # Parse expression (format: "number operation number")
            parts = expression.split()
            
            if len(parts) != 3:
                print("Error: Please enter calculation in format: <number> <operation> <number>")
                print("Example: 5 + 3 or 10 / 2")
                return
            
            # Validate and convert inputs
            try:
                num1 = self.validator.validate_number(parts[0])
                operation = self.validator.validate_operation(parts[1])
                num2 = self.validator.validate_number(parts[2])
            except ValueError as e:
                print(f"Input Error: {e}")
                return
            
            # Create and execute calculation
            try:
                calculation = CalculationFactory.create_calculation(num1, num2, operation)
                calculation.execute()
                
                # Add to history and display result
                self.history.add_calculation(calculation)
                print(f"Result: {calculation}")
                
            except ValueError as e:
                print(f"Calculation Error: {e}")
            except Exception as e:
                print(f"Unexpected calculation error: {e}")
                
        except Exception as e:
            print(f"Error processing calculation: {e}")
    
    def _handle_exit(self) -> None:
        """Handle exit command."""
        print("Thank you for using the calculator. Goodbye!")
        self.running = False
    
    def _handle_help(self) -> None:
        """Display help information."""
        help_text = """
Calculator Help
===============

Usage:
  <number> <operation> <number>    Perform calculation
  
Operations:
  +, add         Addition
  -, subtract    Subtraction  
  *, multiply    Multiplication
  /, divide      Division

Commands:
  help, h, ?     Show this help message
  history, hist  Show calculation history
  clear, cls     Clear calculation history
  exit, quit, q  Exit calculator

Examples:
  5 + 3          Addition: 5 + 3 = 8
  10.5 - 2.3     Subtraction: 10.5 - 2.3 = 8.2
  4 * 7          Multiplication: 4 * 7 = 28
  15 / 3         Division: 15 / 3 = 5.0
  
Notes:
  - Use decimal points for floating-point numbers
  - Division by zero is not allowed
  - All calculations are saved in history
        """
        print(help_text)
    
    def _handle_history(self) -> None:
        """Display calculation history."""
        if len(self.history) == 0:
            print("No calculations in history.")
            return
        
        print(f"\nCalculation History ({len(self.history)} entries):")
        print("=" * 40)
        
        for i, calc in enumerate(self.history.get_history(), 1):
            timestamp = calc.timestamp.strftime("%H:%M:%S")
            print(f"{i:2d}. [{timestamp}] {calc}")
    
    def _handle_clear_history(self) -> None:
        """Clear calculation history."""
        count = len(self.history)
        self.history.clear_history()
        print(f"Cleared {count} calculation(s) from history.")
    
    def _print_welcome(self) -> None:
        """Print welcome message."""
        welcome_text = """
╔══════════════════════════════════════╗
║        Professional Calculator        ║
║                v1.0.0                ║
╚══════════════════════════════════════╝

Type 'help' for usage instructions.
Type 'exit' to quit.
        """
        print(welcome_text)


def main():
    """Main entry point for the calculator application."""
    calculator = Calculator()
    calculator.start()


if __name__ == "__main__":
    main()
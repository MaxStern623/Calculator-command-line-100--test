"""
Calculation module for calculator application.

This module defines the Calculation class and CalculationFactory for creating calculations.
"""

from typing import Union
from datetime import datetime
from operation import Operation

Number = Union[int, float]


class Calculation:
    """Represents a single calculation with operands, operation, and result."""
    
    def __init__(self, a: Number, b: Number, operation: Operation):
        """
        Initialize a calculation.
        
        Args:
            a: First operand
            b: Second operand
            operation: Operation to perform
        """
        self.a = a
        self.b = b
        self.operation = operation
        self.timestamp = datetime.now()
        self._result = None
        self._executed = False
    
    def execute(self) -> Number:
        """
        Execute the calculation and return the result.
        
        Returns:
            Result of the calculation
            
        Raises:
            ValueError: If operation cannot be performed
        """
        if not self._executed:
            self._result = self.operation.execute(self.a, self.b)
            self._executed = True
        return self._result
    
    @property
    def result(self) -> Number:
        """Get the result of the calculation (executes if not already done)."""
        return self.execute()
    
    def __str__(self) -> str:
        """String representation of the calculation."""
        if self._executed:
            return f"{self.a} {self._get_operation_symbol()} {self.b} = {self._result}"
        else:
            return f"{self.a} {self._get_operation_symbol()} {self.b} = ?"
    
    def __repr__(self) -> str:
        """Developer representation of the calculation."""
        return f"Calculation({self.a}, {self.b}, {self.operation.__class__.__name__})"
    
    def _get_operation_symbol(self) -> str:
        """Get the symbol for the operation."""
        operation_symbols = {
            'AddOperation': '+',
            'SubtractOperation': '-',
            'MultiplyOperation': '*',
            'DivideOperation': '/'
        }
        return operation_symbols.get(self.operation.__class__.__name__, '?')


class CalculationFactory:
    """Factory for creating calculations based on operation type."""
    
    @staticmethod
    def create_calculation(a: Number, b: Number, operation_type: str) -> Calculation:
        """
        Create a calculation instance based on operation type.
        
        Args:
            a: First operand
            b: Second operand
            operation_type: Type of operation ('add', 'subtract', 'multiply', 'divide')
            
        Returns:
            Calculation instance
            
        Raises:
            ValueError: If operation type is not supported
        """
        from operation import (AddOperation, SubtractOperation, 
                             MultiplyOperation, DivideOperation)
        
        # Handle None case
        if operation_type is None:
            raise ValueError("Unsupported operation: None. "
                           "Valid operations are: ['add', 'subtract', 'multiply', 'divide', '+', '-', '*', '/']")
        
        operations_map = {
            'add': AddOperation(),
            'subtract': SubtractOperation(),
            'multiply': MultiplyOperation(),
            'divide': DivideOperation(),
            '+': AddOperation(),
            '-': SubtractOperation(),
            '*': MultiplyOperation(),
            '/': DivideOperation()
        }
        
        operation_type_lower = operation_type.lower().strip()
        
        if operation_type_lower not in operations_map:
            valid_operations = list(set(operations_map.keys()))
            raise ValueError(f"Unsupported operation: {operation_type}. "
                           f"Valid operations are: {valid_operations}")
        
        operation = operations_map[operation_type_lower]
        return Calculation(a, b, operation)
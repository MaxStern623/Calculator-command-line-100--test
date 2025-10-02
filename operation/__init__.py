"""
Operation module for calculator application.

This module defines the base operation interface and concrete arithmetic operations.
"""

from abc import ABC, abstractmethod
from typing import Union

Number = Union[int, float]


class Operation(ABC):
    """Abstract base class for all operations."""
    
    @abstractmethod
    def execute(self, a: Number, b: Number) -> Number:
        """
        Execute the operation on two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Result of the operation
            
        Raises:
            ValueError: If operation cannot be performed
        """
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """String representation of the operation."""
        pass


class AddOperation(Operation):
    """Addition operation."""
    
    def execute(self, a: Number, b: Number) -> Number:
        """Add two numbers."""
        return a + b
    
    def __str__(self) -> str:
        return "addition"


class SubtractOperation(Operation):
    """Subtraction operation."""
    
    def execute(self, a: Number, b: Number) -> Number:
        """Subtract second number from first number."""
        return a - b
    
    def __str__(self) -> str:
        return "subtraction"


class MultiplyOperation(Operation):
    """Multiplication operation."""
    
    def execute(self, a: Number, b: Number) -> Number:
        """Multiply two numbers."""
        return a * b
    
    def __str__(self) -> str:
        return "multiplication"


class DivideOperation(Operation):
    """Division operation."""
    
    def execute(self, a: Number, b: Number) -> Number:
        """Divide first number by second number."""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b
    
    def __str__(self) -> str:
        return "division"
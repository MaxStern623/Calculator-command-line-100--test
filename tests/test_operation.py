"""
Unit tests for the operation module.

This module contains comprehensive tests for all operation classes with
parameterized tests and edge case coverage.
"""

import pytest
from operation import (Operation, AddOperation, SubtractOperation, 
                      MultiplyOperation, DivideOperation)


class TestAddOperation:
    """Test cases for AddOperation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.add_op = AddOperation()
    
    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (-5, -3, -8),
        (1.5, 2.5, 4.0),
        (10, -5, 5),
        (0.1, 0.2, 0.3),
        (1000000, 2000000, 3000000),
        (-1.5, -2.5, -4.0)
    ])
    def test_execute_valid_inputs(self, a, b, expected):
        """Test addition with various valid inputs."""
        result = self.add_op.execute(a, b)
        assert result == pytest.approx(expected, rel=1e-9)
    
    def test_str_representation(self):
        """Test string representation."""
        assert str(self.add_op) == "addition"
    
    def test_inheritance(self):
        """Test that AddOperation inherits from Operation."""
        assert isinstance(self.add_op, Operation)


class TestSubtractOperation:
    """Test cases for SubtractOperation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.subtract_op = SubtractOperation()
    
    @pytest.mark.parametrize("a, b, expected", [
        (5, 3, 2),
        (0, 0, 0),
        (1, 1, 0),
        (-5, -3, -2),
        (10.5, 2.5, 8.0),
        (-10, 5, -15),
        (0.3, 0.1, 0.2),
        (1000000, 500000, 500000),
        (-1.5, 2.5, -4.0)
    ])
    def test_execute_valid_inputs(self, a, b, expected):
        """Test subtraction with various valid inputs."""
        result = self.subtract_op.execute(a, b)
        assert result == pytest.approx(expected, rel=1e-9)
    
    def test_str_representation(self):
        """Test string representation."""
        assert str(self.subtract_op) == "subtraction"
    
    def test_inheritance(self):
        """Test that SubtractOperation inherits from Operation."""
        assert isinstance(self.subtract_op, Operation)


class TestMultiplyOperation:
    """Test cases for MultiplyOperation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.multiply_op = MultiplyOperation()
    
    @pytest.mark.parametrize("a, b, expected", [
        (3, 4, 12),
        (0, 5, 0),
        (5, 0, 0),
        (-3, 4, -12),
        (-3, -4, 12),
        (2.5, 4, 10.0),
        (0.5, 0.2, 0.1),
        (1000, 1000, 1000000),
        (-2.5, -2, 5.0)
    ])
    def test_execute_valid_inputs(self, a, b, expected):
        """Test multiplication with various valid inputs."""
        result = self.multiply_op.execute(a, b)
        assert result == pytest.approx(expected, rel=1e-9)
    
    def test_str_representation(self):
        """Test string representation."""
        assert str(self.multiply_op) == "multiplication"
    
    def test_inheritance(self):
        """Test that MultiplyOperation inherits from Operation."""
        assert isinstance(self.multiply_op, Operation)


class TestDivideOperation:
    """Test cases for DivideOperation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.divide_op = DivideOperation()
    
    @pytest.mark.parametrize("a, b, expected", [
        (10, 2, 5.0),
        (1, 1, 1.0),
        (-10, 2, -5.0),
        (-10, -2, 5.0),
        (7, 2, 3.5),
        (0, 5, 0.0),
        (1.5, 0.5, 3.0),
        (100, 4, 25.0),
        (-7.5, 2.5, -3.0)
    ])
    def test_execute_valid_inputs(self, a, b, expected):
        """Test division with various valid inputs."""
        result = self.divide_op.execute(a, b)
        assert result == pytest.approx(expected, rel=1e-9)
    
    @pytest.mark.parametrize("a", [1, -1, 0, 5.5, -3.2])
    def test_execute_division_by_zero(self, a):
        """Test division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            self.divide_op.execute(a, 0)
    
    def test_str_representation(self):
        """Test string representation."""
        assert str(self.divide_op) == "division"
    
    def test_inheritance(self):
        """Test that DivideOperation inherits from Operation."""
        assert isinstance(self.divide_op, Operation)


class TestOperationAbstractBase:
    """Test cases for the abstract Operation base class."""
    
    def test_cannot_instantiate_operation(self):
        """Test that Operation cannot be directly instantiated."""
        with pytest.raises(TypeError):
            Operation()
    
    def test_all_operations_implement_interface(self):
        """Test that all concrete operations implement the required interface."""
        operations = [AddOperation(), SubtractOperation(), 
                     MultiplyOperation(), DivideOperation()]
        
        for operation in operations:
            # Check that execute method exists and is callable
            assert hasattr(operation, 'execute')
            assert callable(operation.execute)
            
            # Check that __str__ method exists and returns string
            assert hasattr(operation, '__str__')
            assert isinstance(str(operation), str)
            
            # Check inheritance
            assert isinstance(operation, Operation)
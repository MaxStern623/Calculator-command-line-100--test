# Professional Calculator Application

A comprehensive calculator application with REPL interface, featuring robust error handling, calculation history, and 100% test coverage.

## Features

- **Interactive REPL Interface**: User-friendly command-line interface with clear prompts
- **Arithmetic Operations**: Support for addition, subtraction, multiplication, and division
- **Input Validation**: Comprehensive validation for numbers and operations
- **Error Handling**: Graceful handling of division by zero and invalid inputs
- **Calculation History**: Maintains session history with timestamps
- **Help System**: Built-in help and command documentation
- **Modular Design**: Clean separation of concerns with factory pattern
- **100% Test Coverage**: Comprehensive unit and integration tests

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup
1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:

```bash
pip install pytest pytest-cov
```

## Usage

### Running the Calculator

```bash
# From project directory
python -m calculator

# Or directly
python calculator/__init__.py
```

### Calculator Commands

- **Basic Operations**: `<number> <operation> <number>`
  - `5 + 3` - Addition
  - `10 - 4` - Subtraction  
  - `6 * 7` - Multiplication
  - `15 / 3` - Division

- **Built-in Commands**:
  - `help` or `h` or `?` - Show help information
  - `history` or `hist` - Display calculation history
  - `clear` or `cls` - Clear calculation history
  - `exit` or `quit` or `q` - Exit calculator

### Example Session

```
╔══════════════════════════════════════╗
║        Professional Calculator        ║
║                v1.0.0                ║
╚══════════════════════════════════════╝

Type 'help' for usage instructions.
Type 'exit' to quit.

Calculator> 5 + 3
Result: 5 + 3 = 8

Calculator> 10.5 * 2
Result: 10.5 * 2 = 21.0

Calculator> history
Calculation History (2 entries):
========================================
 1. [14:30:15] 5 + 3 = 8
 2. [14:30:22] 10.5 * 2 = 21.0

Calculator> exit
Thank you for using the calculator. Goodbye!
```

## Project Structure

```
calculator/
├── calculator/           # Main calculator module
│   └── __init__.py      # Calculator, History, and InputValidator classes
├── calculation/         # Calculation logic module  
│   └── __init__.py     # Calculation and CalculationFactory classes
├── operation/          # Operation definitions module
│   └── __init__.py    # Operation base class and implementations
├── tests/             # Comprehensive test suite
│   ├── __init__.py
│   ├── test_calculator.py     # Calculator component tests
│   ├── test_calculation.py    # Calculation logic tests
│   ├── test_operation.py      # Operation tests
│   └── test_integration.py    # Integration tests
├── __init__.py        # Package initialization
├── __main__.py        # Module entry point
├── pyproject.toml     # Project configuration
├── README.md          # This file
└── requirements.txt   # Python dependencies
```

## Architecture

The application follows a modular design with clear separation of concerns:

### Core Components

1. **Operation Module** (`operation/`)
   - Abstract `Operation` base class
   - Concrete operations: `AddOperation`, `SubtractOperation`, `MultiplyOperation`, `DivideOperation`
   - Each operation encapsulates its specific logic and validation

2. **Calculation Module** (`calculation/`)
   - `Calculation` class: Represents a single calculation with operands, operation, and result
   - `CalculationFactory`: Creates calculation instances based on user input using factory pattern
   - Handles calculation execution and result caching

3. **Calculator Module** (`calculator/`)
   - `Calculator`: Main REPL interface and command processing
   - `CalculatorHistory`: Manages calculation history with timestamps
   - `InputValidator`: Validates user input for numbers and operations

### Design Principles

- **DRY (Don't Repeat Yourself)**: Common functionality abstracted into reusable components
- **Single Responsibility**: Each class has a focused, single purpose
- **Factory Pattern**: `CalculationFactory` creates appropriate calculation instances
- **Input Validation**: Centralized validation with clear error messages
- **Error Handling**: Comprehensive error handling at all levels

## Testing

The project maintains 100% test coverage with comprehensive unit and integration tests.

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_calculator.py

# Run tests with coverage report
pytest --cov=calculator --cov=calculation --cov=operation --cov-report=html
```

### Test Structure

- **Unit Tests**: Test individual components in isolation
- **Parametrized Tests**: Test multiple scenarios efficiently
- **Integration Tests**: Test component interactions
- **Edge Case Coverage**: Tests for error conditions and boundary cases

### Test Categories

1. **Operation Tests** (`test_operation.py`)
   - Tests for each arithmetic operation
   - Edge cases like division by zero
   - Input validation and error handling

2. **Calculation Tests** (`test_calculation.py`)
   - Calculation creation and execution
   - Factory pattern functionality
   - Result caching and string representation

3. **Calculator Tests** (`test_calculator.py`)
   - REPL interface functionality
   - Command processing and history management
   - Input validation and error handling

4. **Integration Tests** (`test_integration.py`)
   - End-to-end workflow testing
   - Component interaction verification
   - Complete user session simulation

## Error Handling

The calculator provides comprehensive error handling:

- **Invalid Numbers**: Clear messages for non-numeric input
- **Invalid Operations**: Helpful suggestions for supported operations
- **Division by Zero**: Specific error message and graceful handling
- **Malformed Input**: Guidance on correct input format
- **Unexpected Errors**: Graceful handling with informative messages

## Development

### Code Quality

The project maintains high code quality standards:

- **Type Hints**: Full type annotation for better code documentation
- **Docstrings**: Comprehensive documentation for all classes and methods
- **Linting**: Code follows PEP 8 standards
- **Testing**: 100% test coverage requirement

### Adding New Operations

To add a new operation:

1. Create a new operation class in `operation/__init__.py`:
```python
class PowerOperation(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        return a ** b
    
    def __str__(self) -> str:
        return "exponentiation"
```

2. Add it to the factory in `calculation/__init__.py`:
```python
operations_map = {
    # existing operations...
    'power': PowerOperation(),
    '^': PowerOperation()
}
```

3. Add comprehensive tests in `tests/test_operation.py`

## Contributing

1. Follow existing code style and patterns
2. Maintain 100% test coverage
3. Add comprehensive documentation
4. Test edge cases thoroughly
5. Update README if adding new features

## Version History

- **v1.0.0**: Initial release with core functionality
  - REPL interface
  - Basic arithmetic operations
  - History management
  - 100% test coverage

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions:
1. Check the help command within the calculator
2. Review the test files for usage examples
3. Examine the source code documentation
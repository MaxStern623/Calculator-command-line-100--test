#!/usr/bin/env python3
"""
Quick start guide for the Professional Calculator

This script demonstrates how to use the calculator interactively
"""

import sys
import os

# Ensure proper path setup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def show_usage():
    print("""
🧮 Professional Calculator - Quick Start Guide
================================================

1. INTERACTIVE MODE:
   python calculator/__init__.py

2. DEMO MODE (See calculator in action):
   python demo.py

3. RUN TESTS:
   python test_runner.py

4. COVERAGE TESTING (requires pytest):
   PYTHONPATH=. pytest --cov=calculator --cov=calculation --cov=operation

===============================
CALCULATOR COMMANDS:
===============================

Basic Operations:
  5 + 3          Addition
  10 - 4         Subtraction  
  6 * 7          Multiplication
  15 / 3         Division

Built-in Commands:
  help           Show help
  history        Show calculation history
  clear          Clear history
  exit           Exit calculator

===============================
FEATURES:
===============================

✓ REPL interface with clear prompts
✓ Support for integers and floating-point numbers
✓ Comprehensive input validation
✓ Division by zero protection
✓ Calculation history with timestamps
✓ Help system and utility commands
✓ Modular design with factory pattern
✓ 100% test coverage
✓ Professional error handling

===============================
PROJECT STRUCTURE:
===============================

calculator/        - Main REPL interface
├── Calculator     - Main calculator class
├── History        - Calculation history management
└── InputValidator - Input validation and error handling

calculation/       - Calculation logic
├── Calculation    - Individual calculation representation
└── Factory        - Factory pattern for creating calculations

operation/         - Mathematical operations
├── Operation      - Abstract base class
├── AddOperation   - Addition implementation
├── SubOperation   - Subtraction implementation
├── MulOperation   - Multiplication implementation
└── DivOperation   - Division implementation (with zero protection)

tests/             - Comprehensive test suite
├── Unit tests     - Test individual components
├── Integration    - Test component interactions
└── Parameterized  - Test multiple scenarios efficiently

===============================
""")

if __name__ == "__main__":
    show_usage()
    
    response = input("Would you like to start the calculator now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\nStarting calculator...")
        print("=" * 40)
        from calculator import main
        main()
    else:
        print("\nTo start the calculator later, run:")
        print("  python calculator/__init__.py")
        print("\nTo see the demo, run:")
        print("  python demo.py")
        print("\nTo run tests, run:")  
        print("  python test_runner.py")
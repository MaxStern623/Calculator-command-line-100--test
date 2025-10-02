"""
Main entry point for the calculator application.

This module allows the calculator to be run as a Python module.
Usage: python -m calculator
"""

import os
import sys

# Add the current directory to Python path to find modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculator import main

if __name__ == "__main__":
    main()

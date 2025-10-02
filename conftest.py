# Test configuration file to ensure proper imports
import os
import sys

# Add the project root to Python path and ensure it's first
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir in sys.path:
    sys.path.remove(project_dir)
sys.path.insert(0, project_dir)

# Remove any parent directory paths that might interfere
parent_dir = os.path.dirname(project_dir)
while parent_dir in sys.path:
    sys.path.remove(parent_dir)

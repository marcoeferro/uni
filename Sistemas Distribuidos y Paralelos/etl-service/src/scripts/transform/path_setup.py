import sys
from pathlib import Path

# Get the current file's directory
current_dir = Path(__file__).resolve().parent

# Go two levels up
parent_dir = current_dir.parents[1]

# Add the parent directory to sys.path
sys.path.append(str(parent_dir))

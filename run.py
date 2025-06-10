#!/usr/bin/env python3
"""
nice to have script to run from project root
Usage: python3 run.py [command]
"""
import sys
import os
from pathlib import Path

project_root = Path(__file__).parent
os.chdir(project_root)
sys.path.insert(0, str(project_root / 'src'))

try:
    from src.main import cli
    cli()
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory.")
    sys.exit(1)
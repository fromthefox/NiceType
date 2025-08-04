#!/usr/bin/env python3
"""
Launcher script for NiceType development and testing.
This script helps test NiceType in different modes without installation.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nicetype.main import main

if __name__ == "__main__":
    main()
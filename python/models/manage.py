#!/usr/bin/env python
import os
import sys
from os.path import dirname

# to handle models as py 'folder' package, not as single file
sys.path.insert(0, os.path.abspath(os.path.join(dirname(__file__), '..')))

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

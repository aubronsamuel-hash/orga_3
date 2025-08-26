import os
import sys

# Add backend/ to PYTHONPATH for 'from app import ...'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

"""Shared pytest configuration for CNQ engine tests."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_ENGINE_DIR = _HERE.parent.parent       # HCI-CNQ/engine/
if str(_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(_ENGINE_DIR))

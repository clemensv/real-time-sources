"""Pytest configuration for aviationweather tests.

Ensures that the aviationweather_core package is importable even when
pytest adds the CWD (feeders/aviationweather/) to sys.path, which would
otherwise cause the outer wrapper directory to shadow the editable install.
"""
import pathlib
import sys

# Insert the outer core wrapper directory at the front of sys.path so that
# Python resolves `aviationweather_core` to the inner package directory
# (which has __init__.py) before reaching '' (CWD) in sys.path.
_core_wrapper = str(pathlib.Path(__file__).parent / "aviationweather_core")
if _core_wrapper not in sys.path:
    sys.path.insert(0, _core_wrapper)

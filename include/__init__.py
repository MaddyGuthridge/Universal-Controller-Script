"""
include

Initialise substitute modules to add them to the path variable, so that they
can be imported normally.

WARNING: The substitute modules aren't complete replacements, and should only
be used for purposes that have no effect at runtime, such as type checking.
"""

import sys

try:
    import typing
    import abc
except ImportError:
    directory = __file__.removesuffix("\\__init__.py")

    # Add right to the start of the path
    sys.path.insert(0, directory)

"""
common > util > hotreload

Contains helper functions for hot reloading components of the script

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

import sys


def getTemporaryModule(name: str):
    """
    Returns a reference to a module that will be hot reloaded each time a
    request is made.

    WARNING: This implementation is very unreliable, and if possible, using
    importlib is preferred - this is only included until importlib actually
    becomes a component in the standard library for FL Studio's Python
    interface

    ### THIS WILL FAIL WHEN:
    * The module is already loaded elsewhere
    * The module is a component of a higher-level module (not sure why)

    ### Args:
    * `name` (`str`): name of the module to get a reference to

    ### Returns:
    * `module`: temporary module
    """

    # Import the module
    module = __import__(name)

    sys.modules.pop(name)

    return module

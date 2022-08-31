"""
tests

Contains code to test the project, using Pytest

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

# Add the source directory to the PATH variable so the project doesn't break
# when we import things
import sys
sys.path.append('./src')

# Make sure that we don't break things due to circular imports
import common  # noqa: E402
del common

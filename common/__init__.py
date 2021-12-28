"""common

Contains common functions and code required to initialise and manage the script.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

from .contextmanager import getContext, resetContext, catchContextResetException

from . import util

import consts

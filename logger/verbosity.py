
from typing import NewType

Verbosity = NewType("Verbosity", int)

MOST_VERBOSE = Verbosity(100)

NOTE = Verbosity(5)
INFO = Verbosity(4)
WARNING = Verbosity(3)
ERROR = Verbosity(2)
CRITICAL = Verbosity(1)

DEFAULT = INFO

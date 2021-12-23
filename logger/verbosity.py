
from typing import NewType

Verbosity = NewType("Verbosity", int)

MOST_VERBOSE = Verbosity(-1)

NOTE = Verbosity(1)
INFO = Verbosity(2)
WARNING = Verbosity(3)
ERROR = Verbosity(4)
CRITICAL = Verbosity(5)

DEFAULT = INFO

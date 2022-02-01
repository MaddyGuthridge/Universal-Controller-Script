

from typing import Type, Union


EllipsisType: Type = type(Ellipsis)

# Variable type for byte match expression
ByteMatch = Union[int, range, tuple[int, ...], 'ellipsis']

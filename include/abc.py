"""
include > abc

A basic stand-in for the abstract base class module, to prevent crashes during
runtime
"""

def abstractmethod(func):
    return func

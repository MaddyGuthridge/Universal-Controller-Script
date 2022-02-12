

class _AnnotationType:
    def __init__(self, name) -> None:
        self._name = name
    def __getitem__(self, key):
        return object

TypeGuard = _AnnotationType('TypeGuard')

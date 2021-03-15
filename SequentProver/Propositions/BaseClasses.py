class Proposition:
    pass


class Unary(Proposition):
    """Superclass for unary propositions."""
    arity: int = 1
    string: str = None
    symbol: str = None

    def __init__(self, prop) -> None:
        super().__init__()
        self._prop = prop

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.prop})"

    def __str__(self) -> str:
        return f"({self.string} {self.prop})"

    def __iter__(self):
        yield self.prop

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self.prop == other.prop:
                return True
        return False

    def __ne__(self, other):
        if self == other:
            return False
        return True

    def __len__(self):
        return 1

    @property
    def prop(self):
        return self._prop

    @property
    def names(self):
        return self.prop.names

    @property
    def complexity(self):
        return 1 + self.prop.complexity


class Binary(Proposition):
    """Superclass for binary propositions"""
    arity: int = 2
    string: str = None
    symbol: str = None
    _names = None

    def __init__(self, left, right) -> None:
        self._left = left
        self._right = right

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.left}, {self.right})"

    def __str__(self) -> str:
        return f"({self.left} {self.string} {self.right})"

    def __iter__(self):
        yield self.left
        yield self.right

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self.left == other.left and self.right == other.right:
                return True
        return False

    def __ne__(self, other):
        if self == other:
            return False
        return True

    def __len__(self):
        return 2

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def names(self):
        if self._names is None:
            names = list(self.left.names)
            names.extend([name for name in self.right.names if name not in names])
            self._names = tuple(names)
        return self._names

    @property
    def complexity(self) -> int:
        return 1 + self.left.complexity + self.right.complexity

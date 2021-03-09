class Proposition:
    """Base class for propositions."""
    pass


class Unary(Proposition):
    """Superclass for unary propositions."""
    arity: int = 1
    __slots__ = ["_prop", "_complexity"]

    def __init__(self, prop) -> None:
        if isinstance(prop, Proposition) or isinstance(prop, str):
            self._prop = prop
        else:
            raise RuntimeError(f"{prop} is not a Proposition")
        self._complexity = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.prop})"

    def __str__(self) -> str:
        return f"({self.string} {self.prop})"

    @property
    def prop(self):
        return self._prop

    @property
    def complexity(self):
        if self._complexity is None:
            if isinstance(self.prop, Proposition):
                self._complexity = 1 + self.prop.complexity
            else:
                self._complexity = 0
        return self._complexity


class Binary(Proposition):
    """Superclass for binary propositions"""
    arity: int = 2
    __slots__ = ["_left", "_right", "_complexity"]

    def __init__(self, left: Proposition, right: Proposition) -> None:
        if isinstance(left, Proposition) and isinstance(right, Proposition):
            self._left = left
            self._right = right
        else:
            raise RuntimeError(f"Either {left} or {right} is not a Proposition")
        self._complexity = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.left}, {self.right})"

    def __str__(self) -> str:
        return f"({self.left} {self.string} {self.right})"

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def complexity(self) -> int:
        if self._complexity is None:
            self._complexity = 1 + self.left.complexity + self.right.complexity
        return self._complexity
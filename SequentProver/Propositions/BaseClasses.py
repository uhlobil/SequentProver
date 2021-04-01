import itertools
from typing import Sequence


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

    def instantiate(self, var, name):
        prop = self.prop.instantiate(var, name)
        return self.__class__(prop)


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

    def instantiate(self, var, name):
        left = self.left.instantiate(var, name)
        right = self.right.instantiate(var, name)
        return self.__class__(left, right)


class Quantifier(Proposition):
    arity: int = 1
    string: str = None
    symbol: str = None
    _names: list = None
    __slots__ = ("_var", "_prop")

    def __init__(self, var, prop) -> None:
        self._var = var
        self._prop = prop

    def __repr__(self) -> str:
        return f"{self.__str__()}({self.var}, {self.prop})"

    def __str__(self) -> str:
        return f"{self.symbol}({self.var})({self.prop})"

    def __len__(self) -> int:
        return 1

    def __iter__(self):
        yield self.prop

    def __eq__(self, other) -> bool:
        if self.__class__ == other.__class__:
            generator = self._name_generator()
            name = next(generator)
            while name in self.prop.names:
                name = next(generator)
            if self.instantiate(self.var, name) == other.instantiate(other.var, name):
                return True
        return False

    def __ne__(self, other) -> bool:
        if self == other:
            return False
        return True

    @property
    def var(self):
        return self._var

    @property
    def prop(self):
        return self._prop

    @property
    def names(self):
        if self._names is None:
            names = list(self.prop.names)
            names.remove(self.var)
            self._names = names
        return self._names

    @property
    def complexity(self):
        return 1 + self.prop.complexity

    def instantiate(self, var, name):
        if isinstance(self.prop, Quantifier):
            inner_prop = self.prop
            instantiated = inner_prop.instantiate(var, name)
            return inner_prop.__class__(inner_prop.var, instantiated)
        else:
            return self.prop.instantiate(var, name)

    def _name_generator(self):
        """Produces 2-character combinations of lowercase letters from
        aaa to zzz in order."""
        for i in itertools.product(map(chr, range(97, 123)), repeat=2):
            yield ''.join(i)


class Atom(Proposition):
    """Atomic propositions that form the base of each other proposition.
    Has either the form "Proposition" or "Property(name)"
    """
    arity: int = 0
    complexity: int = 0
    __slots__ = ("_prop", "_names")

    def __init__(self, prop: str, *names: Sequence):
        self._prop = prop
        self._names = tuple(*names)

    def __str__(self):
        if self.names:
            return f"{self.prop}({'; '.join(self.names)})"
        else:
            return f"{self.prop}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.prop == other.prop and self.names == other.names:
            return True
        return False

    def __ne__(self, other):
        if self.prop == other.prop:
            return False
        return True

    # Strictly speaking, this should be called "predicate" or something
    # but naming it prop allows me to use fewer "if" statements, which
    # is better for everyone in the long run.
    @property
    def prop(self):
        return self._prop

    @property
    def names(self):
        return self._names

    def instantiate(self, var, name):
        new_names = [n if n != var else name for n in self.names]
        return Atom(self.prop, new_names)


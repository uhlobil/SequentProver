from Propositions.BaseClasses import Unary, Binary, Proposition
from typing import TypeVar, Sequence


class Atom(Proposition):
    """Atomic propositions that form the base of each other proposition.
    Has either the form "Proposition" or "Property(name)"
    """
    arity: int = 0
    complexity: int = 0
    __slots__ = ("_predicate", "_names")

    def __init__(self, predicate: str, *names: Sequence):
        self._predicate = predicate
        self._names = tuple(*names)

    def __str__(self):
        if self.names:
            return f"{self.predicate}({'; '.join(self.names)})"
        else:
            return f"{self.predicate}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.predicate == other.predicate:
            return True
        return False

    def __ne__(self, other):
        if self.predicate == other.prop:
            return False
        return True

    @property
    def predicate(self):
        return self._predicate

    @property
    def names(self):
        return self._names


class Negation(Unary):
    symbol = "~"
    string = "not"
    __slots__ = "_prop"

    def __init__(self, prop):
        super().__init__(prop)


class Conditional(Binary):
    symbol = "->"
    string = "implies"
    __slots__ = ("_left", "_right")

    def __init__(self, left, right):
        super().__init__(left, right)


class Conjunction(Binary):
    symbol = "&"
    string = "and"
    __slots__ = ("_left", "_right")

    def __init__(self, left, right):
        super().__init__(left, right)


class Disjunction(Binary):
    symbol = "v"
    string = "or"
    __slots__ = ("_left", "_right")

    def __init__(self, left, right):
        super().__init__(left, right)

from typing import Sequence

from Objects.Propositions.ABC import Unary, Proposition, Binary


class Atom(Unary):
    """The basic proposition type. Contains no connectives and is what
    each other proposition type bottoms out in."""
    complexity: int = 0
    symbol = ""
    string = ""

    def __int__(self, prop: str):
        if isinstance(prop, str):
            self._prop = prop
        else:
            raise RuntimeError(f"{prop} is not a string.")

    def __str__(self) -> str:
        return f"{self.prop}"

    def __repr__(self) -> str:
        return f"Atom({self.prop})"


class Formula(Atom):

    def __init__(self, prop: str, variables: Sequence[str]):
        super().__init__(prop)
        self.vars = variables

    def __str__(self):
        return f"{self.prop}({', '.join(self.vars)})"

    def __repr__(self):
        return f"Form({self.prop}, {str(self.vars)})"

    def __eq__(self, other):
        if self.prop == other.prop and self.vars == other.vars:
            return True
        return False

    def __ne__(self, other):
        if self.prop == other.prop and self.vars == other.vars:
            return False
        return True


class Negation(Unary):
    symbol = "~"
    string = "not"

    def __init__(self, prop: Proposition):
        super().__init__(prop)

    def __repr__(self):
        super(Negation, self).__repr__()


class Conditional(Binary):
    symbol = "->"
    string = "implies"

    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        super(Conditional, self).__repr__()


class Conjunction(Binary):
    symbol = "&"
    string = "and"

    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        super(Conjunction, self).__repr__()


class Disjunction(Binary):
    symbol = "v"
    string = "or"

    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        super(Disjunction, self).__repr__()


class Universal(Unary):
    symbol = "_A"
    string = "forall"

    def __init__(self, variable: str, prop: Proposition):
        super().__init__(prop)
        self.variable = variable

    def __repr__(self):
        return f"Universal({self.variable}, {self.prop})"

    def __eq__(self, other):
        if self.prop == other.prop:
            pass

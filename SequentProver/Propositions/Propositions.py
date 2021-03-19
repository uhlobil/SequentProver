from Propositions.BaseClasses import Unary, Binary, Quantifier


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


class Universal(Quantifier):
    symbol = "forall"
    string = "forall"
    __slots__ = ("_var", "_prop")

    def __init__(self, var, prop):
        super().__init__(var, prop)


class Existential(Quantifier):
    symbol = "exists"
    string = "exists"
    __slots__ = ("_var", "_prop")

    def __init__(self, var, prop):
        super().__init__(var, prop)

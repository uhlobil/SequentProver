import json
import os
from collections import namedtuple

from Controllers.Settings import Settings
from Propositions.Propositions import Negation, Conditional, Conjunction, Disjunction, Universal

unit = namedtuple('unit', 'ant, con')


class DecompProp:
    """Base class for decomposable propositions."""
    symbol = None
    side = None

    def __init__(self):
        self.rule = Settings().get_rule(self.side + self.symbol)

    def decompose(self):
        raise NotImplementedError

    def _check_explosivity_invertibility(self):
        if self.rule == "Add":
            self.is_invertible = True
            self.is_explosive = False
        else:
            self.is_invertible = False
            self.is_explosive = True

    def _check_invertibility(self):
        if self.rule == "Add":
            self.is_invertible = False
        else:
            self.is_invertible = True


class LeftDecomp(DecompProp):
    """Intermediary class for propositions in the antecedent."""
    side = "L"

    def __init__(self):
        super().__init__()

    def decompose(self):
        super().decompose()


class RightDecomp(DecompProp):
    """Intermediary class for propositions in the consequent."""
    side = "R"

    def __init__(self):
        super().__init__()

    def decompose(self):
        super().decompose()


class LeftNegation(Negation):
    """Contains rules for decomposing left negations."""

    side = "L"

    def __init__(self, prop):
        super(Negation, self).__init__(prop)
        self.rule = Settings().get_rule(self.side + self.symbol)

    @property
    def is_invertible(self):
        return True

    @property
    def is_explosive(self):
        return False

    def decompose(self) -> tuple:
        return unit([], [self.prop]),


class RightNegation(Negation):
    """Contains rules for decomposing right negations."""

    side = "R"

    def __init__(self, prop):
        super(Negation, self).__init__(prop)
        self.rule = Settings().get_rule(self.side + self.symbol)

    @property
    def is_invertible(self):
        return True

    @property
    def is_explosive(self):
        return False

    def decompose(self) -> tuple:
        return unit([self.prop], []),


class LeftConditional(Conditional):
    """Contains rules for decomposing left conditionals."""

    side = "L"

    def __init__(self, left, right):
        super(Conditional, self).__init__(left, right)
        self.rule = Settings().get_rule(self.side + self.symbol)

    @property
    def is_invertible(self):
        if self.rule == "Add":
            return True
        elif self.rule == "Mult":
            return False
        else:
            raise RuntimeError("L-> rule set to an invalid value.")

    @property
    def is_explosive(self):
        if self.rule == "Add":
            return False
        elif self.rule == "Mult":
            return True
        else:
            raise RuntimeError("L-> rule set to invalid value.")

    def decompose(self) -> tuple:
        return unit([], [self.left]), unit([self.right], [])


class RightConditional(Conditional):
    """Contains rules for decomposing right conditionals."""

    side = "R"

    def __init__(self, left, right):
        super(Conditional, self).__init__(left, right)
        self.rule = Settings().get_rule(self.side + self.symbol)

    @property
    def is_invertible(self):
        if self.rule == "Add":
            return False
        elif self.rule == "Mult":
            return True
        else:
            raise RuntimeError("R-> rule set to an invalid value.")

    @property
    def is_explosive(self):
        return False

    def decompose(self) -> tuple:
        if self.rule == "Add":
            return unit([self.left], []), unit([], [self.right]), unit([self.left], [self.right])
        elif self.rule == "Mult":
            return unit([self.left], [self.right]),


class LeftConjunction(Conjunction):
    """Contains rules for decomposing left Conjunctions."""

    side = "L"

    def __init__(self, left, right):
        super(Conjunction, self).__init__(left, right)
        self.rule = Settings().get_rule(self.side + self.symbol)

    @property
    def is_invertible(self):
        if self.rule == "Add":
            return False
        elif self.rule == "Mult":
            return True
        else:
            raise RuntimeError("L& rule set to an invalid value.")

    @property
    def is_explosive(self):
        return False

    def decompose(self) -> tuple:
        if self.rule == "Add":
            return unit([self.left], []), unit([self.right], []), unit([self.left, self.right], [])
        elif self.rule == "Mult":
            return unit([self.left, self.right], []),


class RightConjunction(Conjunction):
    """Contains rules for decomposing right Conjunctions."""

    side = "R"

    def __init__(self, left, right):
        super(Conjunction, self).__init__(left, right)
        self.rule = Settings().get_rule(self.side + self.symbol)

    @property
    def is_invertible(self):
        if self.rule == "Add":
            return True
        elif self.rule == "Mult":
            return False
        else:
            raise RuntimeError("R& rule set to invalid value.")

    @property
    def is_explosive(self):
        if self.rule == "Add":
            return False
        elif self.rule == "Mult":
            return True
        else:
            raise RuntimeError("R& rule set to invalid value.")

    def decompose(self) -> tuple:
        return unit([], [self.left]), unit([], [self.right])


class LeftDisjunction(Disjunction):
    """Contains rules for decomposing left disjunctions."""

    side = "L"

    def __init__(self, left, right):
        super(Disjunction, self).__init__(left, right)
        self.rule = Settings().get_rule(self.side + self.symbol)

    @property
    def is_invertible(self):
        if self.rule == "Add":
            return True
        elif self.rule == "Mult":
            return False
        else:
            raise RuntimeError("Lv rule set to invalid value.")

    @property
    def is_explosive(self):
        if self.rule == "Add":
            return False
        if self.rule == "Mult":
            return True
        else:
            raise RuntimeError("Lv rule set to invalid value.")

    def decompose(self) -> tuple:
        return unit([self.left], []), unit([self.right], [])


class RightDisjunction(Disjunction):
    """Contains rules for decomposing right disjunctions"""

    side = "R"

    def __init__(self, left, right):
        super(Disjunction, self).__init__(left, right)
        self.rule = Settings().get_rule(self.side + self.symbol)

    @property
    def is_invertible(self):
        if self.rule == "Add":
            return False
        elif self.rule == "Mult":
            return True
        else:
            raise RuntimeError("Rv rule set to invalid value.")

    @property
    def is_explosive(self):
        return False

    def decompose(self) -> tuple:
        if self.rule == "Add":
            return unit([], [self.left]), unit([], [self.right]), unit([], [self.left, self.right])
        elif self.rule == "Mult":
            return unit([], [self.left, self.right]),


class LeftUniversal(Universal):
    """Contains rules for decomposing left universals."""

    side = "L"

    def __init__(self, var, prop):
        super(Universal, self).__init__(var, prop)
        self.rule = Settings().get_rule(self.side + self.symbol)

    @property
    def is_invertible(self):
        return False

    @property
    def is_explosive(self):
        return True

    def decompose(self) -> tuple:
        names = _load_object_names()
        units = [unit([self.instantiate(self.var, name)], []) for name in names]
        return tuple(units)


class RightUniversal(Universal):
    pass


def create(attributes):
    """Returns the decomposable proposition based on the input attributes."""
    proposition = attributes.proposition
    symbol = proposition.symbol
    side = attributes.side
    if attributes.proposition.arity == 1:
        return _create_unary_prop(proposition, side, symbol)
    else:
        return _create_binary_prop(proposition, side, symbol)


def _create_unary_prop(proposition, side, symbol):
    """Return the relevant unary decomposable proposition."""
    if symbol == "~":
        return _create_negation(proposition, side)
    elif symbol == "forall":
        return _create_universal(proposition, side)
    elif symbol == "exists":
        return _create_existential(proposition, side)


def _create_binary_prop(proposition, side, symbol):
    """Returns the relevant binary decomposable proposition."""
    left = proposition.left
    right = proposition.right
    if symbol == "->":
        return _create_conditional(left, right, side)
    elif symbol == "&":
        return _create_conjunction(left, right, side)
    elif symbol == "v":
        return _create_disjunction(left, right, side)


def _create_disjunction(left, right, side):
    """Returns a decomposable disjunction based on inputs."""
    if side == "ant":
        return LeftDisjunction(left, right)
    else:
        return RightDisjunction(left, right)


def _create_conjunction(left, right, side):
    """Returns a decomposable conjunction based on inputs."""
    if side == "ant":
        return LeftConjunction(left, right)
    else:
        return RightConjunction(left, right)


def _create_conditional(left, right, side):
    """Returns a decomposable conditional based on inputs."""
    if side == "ant":
        return LeftConditional(left, right)
    else:
        return RightConditional(left, right)


def _create_negation(proposition, side):
    """Returns a decomposable negation based on inputs."""
    contents = proposition.prop
    if side == "ant":
        return LeftNegation(contents)
    else:
        return RightNegation(contents)


def _create_universal(proposition, side):
    """Return a decomposable Universal."""
    prop = proposition.prop
    var = proposition.var
    if side == "ant":
        return LeftUniversal(var, prop)
    elif side == "con":
        return RightUniversal(var, prop)


def _create_existential(proposition, side):
    pass


def _load_object_names():
    current_file_name = os.path.dirname(__file__)
    names_file = os.path.join(current_file_name, "..", "data", "Names.json")
    with open(names_file, "r") as file:
        return json.load(file)

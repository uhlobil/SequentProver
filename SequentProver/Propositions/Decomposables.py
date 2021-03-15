from collections import namedtuple

from Controllers.Settings import Settings
from Propositions.Propositions import Negation, Conditional, Conjunction, Disjunction

unit = namedtuple('unit', 'ant, con')


class DecompProp:
    """Base class for decomposable propositions."""

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


class LeftNegation(Negation, LeftDecomp):
    """Contains rules for decomposing left negations."""
    is_invertible = True
    is_explosive = False

    def __init__(self, prop):
        super(Negation, self).__init__(prop)
        super(LeftDecomp, self).__init__()

    def decompose(self) -> tuple:
        return unit([], [self.prop]),


class RightNegation(Negation, RightDecomp):
    """Contains rules for decomposing right negations."""
    is_invertible = True
    is_explosive = False

    def __init__(self, prop):
        super(Negation, self).__init__(prop)
        super(RightDecomp, self).__init__()

    def decompose(self) -> tuple:
        return unit([self.prop], []),


class LeftConditional(Conditional, LeftDecomp):
    """Contains rules for decomposing left conditionals."""

    def __init__(self, left, right):
        super(Conditional, self).__init__(left, right)
        super(LeftDecomp, self).__init__()
        self._check_explosivity_invertibility()

    def decompose(self) -> tuple:
        return unit([], [self.left]), unit([self.right], [])


class RightConditional(Conditional, RightDecomp):
    """Contains rules for decomposing right conditionals."""
    is_explosive = False

    def __init__(self, left, right):
        super(Conditional, self).__init__(left, right)
        super(RightDecomp, self).__init__()
        self._check_invertibility()

    def decompose(self) -> tuple:
        if self.rule == "Add":
            return unit([self.left], []), unit([], [self.right]), unit([self.left], [self.right])
        elif self.rule == "Mult":
            return unit([self.left], [self.right]),


class LeftConjunction(Conjunction, LeftDecomp):
    """Contains rules for decomposing left Conjunctions."""
    is_explosive = False

    def __init__(self, left, right):
        super(Conjunction, self).__init__(left, right)
        super(LeftDecomp, self).__init__()
        self._check_invertibility()

    def decompose(self) -> tuple:
        if self.rule == "Add":
            return unit([self.left], []), unit([self.right], []), unit([self.left, self.right], [])
        elif self.rule == "Mult":
            return unit([self.left, self.right], []),


class RightConjunction(Conjunction, RightDecomp):
    """Contains rules for decomposing right Conjunctions."""

    def __init__(self, left, right):
        super(Conjunction, self).__init__(left, right)
        super(RightDecomp, self).__init__()
        self._check_explosivity_invertibility()

    def decompose(self) -> tuple:
        return unit([], [self.left]), unit([], [self.right])


class LeftDisjunction(Disjunction, LeftDecomp):
    """Contains rules for decomposing left disjunctions."""

    def __init__(self, left, right):
        super(Disjunction, self).__init__(left, right)
        super(LeftDecomp, self).__init__()
        self._check_explosivity_invertibility()

    def decompose(self) -> tuple:
        return unit([self.left], []), unit([self.right], [])


class RightDisjunction(Disjunction, RightDecomp):
    """Contains rules for decomposing right disjunctions"""
    is_explosive = False

    def __init__(self, left, right):
        super(Disjunction, self).__init__(left, right)
        super(RightDecomp, self).__init__()
        self._check_invertibility()

    def decompose(self) -> tuple:
        if self.rule == "Add":
            return unit([], [self.left]), unit([], [self.right]), unit([], [self.left, self.right])
        elif self.rule == "Mult":
            return unit([], [self.left, self.right]),


def create(attributes):
    """Returns the decomposable proposition based on the input attributes."""
    proposition = attributes.proposition
    symbol = proposition.symbol
    side = attributes.side
    if attributes.proposition.arity == 1:
        return _create_negation(proposition, side)
    else:
        return _create_binary_prop(proposition, side, symbol)


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
    contents = proposition._prop
    if side == "ant":
        return LeftNegation(contents)
    else:
        return RightNegation(contents)

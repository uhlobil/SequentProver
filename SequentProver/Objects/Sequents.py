"""
This module contains the Sequent class and its methods.

Sequents are made up of an antecedent and consequent, each of which are
lists of propositions (see Objects.Propositions). Antecedents and
consequents can be initialized with any sequence (list, tuple, etc.).

.complexity returns the number of connectives in the sequent.

.principal returns the principal proposition as a tuple containing the
side of the turnstile in which the proposition sits, the index of that
proposition within that side, and a decomposable version of that
proposition.

.is_reflexive returns a boolean value reflecting whether any of the
antecedents appear in the consequent.

.decompose() returns either a tuple of sequents (for invertible
sequents) or a tuple of tuples of sequents (non-invertible
sequents). When calling this, you should be prepared to handle
whichever the rules you've set will generate. Notably, each sequent has
only one unique decomposition. To decompose further, each child must
have its .decompose() called.
"""

import itertools
from collections import namedtuple
from typing import Sequence, Any, Generator

import Propositions
import Propositions.Decomposables

principal = namedtuple('principal', 'side, index, proposition')


class Sequent:
    """The main concern of the Sequent Prover.

    Complexity is the number of connectives in the sequent.
    The principal is the leftmost proposition with one or more connectives.
    """

    __slots__ = ["_ant", "_con", "_complexity", "_principal", "_is_reflexive"]

    def __init__(self, antecedent: Sequence, consequent: Sequence):
        self._ant = tuple(prop for prop in antecedent)
        self._con = tuple(prop for prop in consequent)
        self._complexity = None
        self._principal = None
        self._is_reflexive = None

    def __repr__(self) -> str:
        return f"Sequent({self.ant}, {self.con})"

    def __str__(self) -> str:
        """Converts self to string."""
        antecedent = [str(prop) for prop in self.ant]
        consequent = [str(prop) for prop in self.con]
        ant_string = ', '.join(antecedent)
        con_string = ', '.join(consequent)
        return f'{ant_string} |~ {con_string}'

    def __bool__(self) -> bool:
        """Return whether sequent is empty (i.e. " |~ ")."""
        if self.ant or self.con:
            return True
        return False

    def __eq__(self, o: object) -> bool:
        if isinstance(o, self.__class__) and o.ant == self.ant \
                and o.con == self.con:
            return True
        return False

    def __ne__(self, other) -> bool:
        if self == other:
            return False
        return True

    def __iter__(self) -> list:
        yield self.ant
        yield self.con

    @property
    def ant(self):
        return self._ant

    @property
    def con(self):
        return self._con

    @property
    def complexity(self):
        """The number of connectives in the sequent."""
        if self._complexity is None:
            self._complexity = sum([a.complexity for a in self.ant]) \
                               + sum([c.complexity for c in self.con])
        return self._complexity

    @property
    def principal(self) -> tuple:
        """Return the principal proposition of this sequent.

        The main proposition: (side, index, proposition), where
        side = 'ant' or 'con', index = n where n is its position in
        side, proposition = a decomposable proposition (cf.
        Decomposables.py in Propositions)."""
        if self._principal is None:
            attributes = self._get_principal()
            proposition = Propositions.Decomposables.create(attributes)
            self._principal = principal(attributes.side, attributes.index, proposition)
        return self._principal

    @property
    def is_reflexive(self) -> bool:
        """Whether this sequent is reflexive."""
        if self._is_reflexive is None:
            self._is_reflexive = self._get_reflexivity()
        return self._is_reflexive

    def decompose(self):
        """Return the result of decomposing this sequent.

        Due to possible complexity, this ends up being a list of tuples
        of sequents. Each result in self._recombine() is a tuple of
        sequents which corresponds to one possible way to decompose
        that sequent (relevant only for non-invertible sequents), and
        these are all put together into a larger tuple to keep cognates
        together.

        For example:

        >>> results: list = Sequent.decompose()
        >>> dimension: tuple                # invertible decompositions have only one dimension
        >>> for dimension in results:       # non-invertible decompositions may have any number
        >>>    sequent: Sequent
        >>>    for sequent in dimension:    # the actual child sequents (left, right, or middle)
        >>>         print(sequent)

        If you're guaranteed to get invertible sequents only, you might
        desire something like the following, where the results[0] is
        the left or only (middle) result, and results[1] is the right
        result (or does not exist):

        >>> results: tuple = Sequent.decompose()[0]
        >>> if len(results) == 1:   # single parent decomposition
        >>>     child = results[0]
        >>>     print(f"Child sequent is: {child}")
        >>> else:                   # if len(results) == 2
        >>>     left = results[0]
        >>>     right = results[1]
        >>>     print(f"Left child is: {left}. Right child is: {right}")
        """

        units: tuple = self.principal.proposition.decompose()
        templates: Sequent = self._templates()
        result = [r for r in self._recombine(units, templates)]
        return result

    def _get_principal(self):
        """Returns side, index, type of the principal proposition."""
        for side in ("ant", "con"):
            for index, proposition in enumerate(getattr(self, side)):
                if proposition.complexity > 0:
                    return principal(side, index, proposition)

    def _get_reflexivity(self):
        """Checks whether this sequent is reflexive."""
        for antecedent in self.ant:
            for consequent in self.con:
                if antecedent == consequent:
                    return True
        return False

    def _templates(self):  # Split explosive portion into two for 1-/2-parent explosives
        """If the principal is_explosive, returns a generator of 2-
        tuples, with template[0] being the left child and template[1]
        being the right child. Otherwise, the base template (which is
        just a sequent) is returned."""
        if self.principal.proposition.is_explosive and self.principal.proposition.arity == 2:
            return (template for template in self._permute_two_parent_template())
        return self._base_template()

    def _base_template(self):
        """Returns this sequent minus the principal."""
        temp_ant = [prop for prop in self.ant]
        temp_con = [prop for prop in self.con]
        if self.principal.side == "ant":
            # noinspection PyTypeChecker
            # PTC thinks this is not an int
            del temp_ant[self.principal.index]
        else:
            # noinspection PyTypeChecker
            # PTC thinks this is not an int
            del temp_con[self.principal.index]
        return Sequent(temp_ant, temp_con)

    def _permute_two_parent_template(self) -> Generator[tuple, list, None]:
        """Yields possible two-parent templates for explosive sequents."""
        base: Sequent = self._base_template()
        ant_permutations = _permute_two_parent(base.ant)
        for antecedent in ant_permutations:
            con_permutations = _permute_two_parent(base.con)
            for consequent in con_permutations:
                yield Sequent(antecedent[0], consequent[0]), \
                      Sequent(antecedent[1], consequent[1])

    def _recombine(self, units, templates):
        """Yields results of putting the units with the templates in
        the right way."""
        if self.principal.proposition.is_explosive and self.principal.proposition.arity == 2:
            yield from _recombine_multiplicative_two_parent(templates, units)
        elif self.principal.proposition.is_invertible:
            if len(units) == 1:
                yield from _recombine_multiplicative_one_parent(templates, units)
            else:
                yield from _recombine_additive_two_parent(templates, units)
        else:
            yield from _recombine_additive_one_parent(templates, units)


def _permute_two_parent(propositions: tuple) -> Generator[tuple, Any, None]:
    """Generates possible combinations for propositions in sides of two
    parent multiplicative rules."""
    permutations = [
        tuple(i) for i in itertools.product([0, 1], repeat=len(propositions))
    ]
    for permutation in permutations:
        x = []
        y = []
        for i, value in enumerate(permutation):
            if value:
                y.append(propositions[i])
            else:
                x.append(propositions[i])
        yield x, y


def _recombine_additive_two_parent(templates, units):
    """Yields sequents decomposed from Additive Right If, Left And,
    and Right Or."""
    x_ant = units[0].ant + [prop for prop in templates.ant]
    x_con = units[0].con + [prop for prop in templates.con]
    y_ant = units[1].ant + [prop for prop in templates.ant]
    y_con = units[1].con + [prop for prop in templates.con]
    yield Sequent(x_ant, x_con), Sequent(y_ant, y_con)


def _recombine_additive_one_parent(template, units):
    """Yields sequents decomposed from Additive Left If, Right And,
    and Left Or."""
    for unit in units:
        antecedent = unit.ant + [prop for prop in template.ant]
        consequent = unit.con + [prop for prop in template.con]
        yield Sequent(antecedent, consequent),


def _recombine_multiplicative_one_parent(templates, units):
    """Yields sequents decomposed from Multiplicative Right If,
    Left And, and Right Or."""
    antecedent = units[0].ant + [prop for prop in templates.ant]
    consequent = units[0].con + [prop for prop in templates.con]
    yield Sequent(antecedent, consequent),


def _recombine_multiplicative_two_parent(templates, units):
    """Yields sequents decomposed from Multiplicative Left If,
    Left And, and Right Or."""
    for template in templates:
        x_ant = units[0].ant + [prop for prop in template[0].ant]
        x_con = units[0].con + [prop for prop in template[0].con]
        y_ant = units[1].ant + [prop for prop in template[1].ant]
        y_con = units[1].con + [prop for prop in template[1].con]
        yield Sequent(x_ant, x_con), Sequent(y_ant, y_con)

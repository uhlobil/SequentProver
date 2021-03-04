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

import Objects.Propositions

principal = namedtuple('principal', 'side, index, proposition')


class Sequent:
    """The main concern of the Sequent Prover.

    complexity is the number of connectives in the sequent.

    the principal is the leftmost proposition with one or more connectives.


    """

    def __init__(self, antecedent: Sequence, consequent: Sequence):
        self.ant = [a for a in antecedent]
        self.con = [c for c in consequent]
        self._complexity = None
        self._principal = None
        self._is_reflexive = None

    def __repr__(self) -> str:
        return f"Sequent({self.ant}, {self.con})"

    def __str__(self):
        antecedent = [str(prop) for prop in self.ant]
        consequent = [str(prop) for prop in self.con]
        ant_string = ', '.join(antecedent)
        con_string = ', '.join(consequent)
        return f'{ant_string} |~ {con_string}'

    def __bool__(self) -> bool:
        """Effectively checks whether the sequent is empty, i.e.
        whether it is ' |~ '."""
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

    @property
    def complexity(self):
        """The number of connectives in the sequent."""
        if self._complexity is None:
            self._complexity = sum([a.complexity for a in self.ant]) \
                               + sum([c.complexity for c in self.con])
        return self._complexity

    @property
    def principal(self):
        """The main proposition: (side, index, proposition), where
        side = 'ant' or 'con', index = n where n is its position in
        side, proposition = a decomposable proposition (cf. DecompProp
        and its subclasses in Propositions.py)."""
        if self.complexity == 0:
            raise AttributeError(f"{self.__repr__} is atomic.")
        if self._principal is None:
            attributes = self._get_principal()
            proposition = Objects.Propositions.create(attributes)
            self._principal = principal(attributes.side, attributes.index, proposition)
        return self._principal

    @property
    def is_reflexive(self):
        """Whether this sequent is reflexive."""
        if self._is_reflexive is None:
            self._is_reflexive = self._get_reflexivity()
        return self._is_reflexive

    def decompose(self):
        """Returns a tuple of tuples of sequents resulting from
        decomposition of this sequent. Each result in self._recombine()
        is a tuple of sequents which corresponds to one possible way to
        decompose that sequent (relevant only for non-invertible
        sequents), and these are all put together into a larger tuple
        to keep cognates together.

        One way to handle the results is:

        results: tuple = Sequent.decompose()
        for dimension: tuple in results:
            for sequent: Sequent in dimension:
                ...

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

    def _templates(self):
        """If the principal is_explosive, returns a generator of 2-
        tuples, with template[0] being the left child and template[1]
        being the right child. Otherwise, the base template (which is
        just a sequent) is returned."""
        if self.principal.proposition.is_explosive:
            return (template for template in self._permute_template())
        return self._base_template()

    def _base_template(self):
        """Returns this sequent minus the principal."""
        temp_ant = [a for a in self.ant]
        temp_con = [c for c in self.con]
        if self.principal.side == "ant":
            del temp_ant[self.principal.index]
        else:
            del temp_con[self.principal.index]
        return Sequent(temp_ant, temp_con)

    def _permute_template(self) -> Generator[tuple, list, None]:
        """Yields possible two-parent templates for explosive sequents."""
        base = self._base_template()
        ant_permutations = _permute(base.ant)
        for antecedent in ant_permutations:
            con_permutations = _permute(base.con)
            for consequent in con_permutations:
                yield Sequent(antecedent[0], consequent[0]), \
                      Sequent(antecedent[1], consequent[1])

    def _recombine(self, units, templates):
        """Yields results of putting the units with the templates in
        the right way."""
        if self.principal.proposition.is_explosive:
            yield from _recombine_multiplicative_two_parent(templates, units)
        elif self.principal.proposition.is_invertible:
            if len(units) == 1:
                yield from _recombine_multiplicative_one_parent(templates, units)
            else:
                yield from _recombine_additive_two_parent(templates, units)
        else:
            yield from _recombine_additive_one_parent(templates, units)


def _permute(propositions: list) -> Generator[tuple, Any, None]:
    """Generates possible combinations for propositions in sides of two
    parent multiplicative rules."""
    permutations = [
        list(i) for i in itertools.product([0, 1], repeat=len(propositions))
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
    x_ant = units[0].ant + templates.ant
    x_con = units[0].con + templates.con
    y_ant = units[1].ant + templates.ant
    y_con = units[1].con + templates.con
    yield Sequent(x_ant, x_con), Sequent(y_ant, y_con)


def _recombine_additive_one_parent(template, units):
    """Yields sequents decomposed from Additive Left If, Right And,
    and Left Or."""
    for unit in units:
        antecedent = unit.ant + template.ant
        consequent = unit.con + template.con
        yield Sequent(antecedent, consequent),


def _recombine_multiplicative_one_parent(templates, units):
    """Yields sequents decomposed from Multiplicative Right If,
    Left And, and Right Or."""
    antecedent = units[0].ant + templates.ant
    consequent = units[0].con + templates.con
    yield Sequent(antecedent, consequent),


def _recombine_multiplicative_two_parent(templates, units):
    """Yields sequents decomposed from Multiplicative Left If,
    Left And, and Right Or."""
    for template in templates:
        x_ant = units[0].ant + template[0].ant
        x_con = units[0].con + template[0].con
        y_ant = units[1].ant + template[1].ant
        y_con = units[1].con + template[1].con
        yield Sequent(x_ant, x_con), Sequent(y_ant, y_con)

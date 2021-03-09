"""
Module for converting strings into sequents and propositions. You
should know what kind of input you're passing here, as trying to
convert a proposition string into a sequent or vice versa will generate
an exception.

Convert(_your_string_).to_sequent() turns the string into a sequent
with each proposition inside converted for you.

Convert(_your_string_).to_proposition() turns the string into a
proposition instead.
"""

from typing import Iterator

from Objects.Propositions.Propositions import Proposition, Atom, \
    Conditional, Conjunction, Disjunction, Negation, Formula
from Objects.Sequents import Sequent

connectives = {
    "implies": Conditional,
    "and": Conjunction,
    "or": Disjunction,
    "not": Negation
}


class String:
    def __init__(self, data) -> None:
        if not isinstance(data, str):
            raise TypeError(f"Input {data} must be a string.")
        self.data = data
        self._is_atomic = None

    @property
    def is_atomic(self):
        """Whether self.data contains any connectives."""
        if self._is_atomic is None:
            for word in self.data.split(' '):
                if word.strip('()') in connectives.keys():
                    self._is_atomic = False
                    break
            else:
                self._is_atomic = True
        return self._is_atomic

    def to_sequent(self) -> Sequent:
        """Returns a sequent from the input."""
        try:
            sides = self.data.split(' |~ ')
            ant_list = sides[0].split(', ')
            con_list = sides[1].split(', ')
            antecedent = [ant for ant in _convert_list(ant_list)]
            consequent = [con for con in _convert_list(con_list)]
            return Sequent(antecedent, consequent)
        except IndexError:
            raise TypeError(f"{self.data} must be a sequent.")

    def to_proposition(self) -> Proposition:
        """Returns a proposition from the input."""
        if ' |~ ' in self.data:
            raise TypeError(f"{self.data} must be a Proposition, not Sequent")
        self._deparen()
        if self.is_atomic:
            if "(" in self.data or ")" in self.data:
                return self._formula()
            else:
                return Atom(self.data)
        return self._proposition()

    def _proposition(self) -> Proposition:
        """Gets the type and location of the main connective."""
        degree = 0
        for index, word in enumerate(self.data.split(' ')):
            degree += _word_degree(word)
            if degree == 0 and word in connectives.keys():
                return self._create(word, index)

    def _create(self, connective, index) -> Proposition:
        """Creates a proposition of input connective's type with the
         contents of self.data. self.data is converted as well, making
         this as recursive as it needs to be."""
        proposition = connectives[connective]
        prop_list = self.data.split(" ")
        if proposition.arity == 1:
            prop_string = " ".join(prop_list[1:])
            prop = String(prop_string).to_proposition()
            return proposition(prop)
        else:
            left_string: str = " ".join(prop_list[:index])
            right_string: str = " ".join(prop_list[index + 1:])
            left: Proposition = String(left_string).to_proposition()
            right: Proposition = String(right_string).to_proposition()
            return proposition(left, right)

    def _deparen(self):
        """Removes all connected sets of outer parentheses in
        self.data."""
        try:
            while self.data[0] == '(' and self.data[-1] == ')':
                degree = 0
                for index, letter in enumerate(self.data):
                    degree += _letter_degree(letter)
                    if degree <= 0 and ((index + 1) < len(self.data)):
                        return
                else:
                    self.data = self.data[1:-1]
        except IndexError:
            return

    def _formula(self):
        wff, variables = _formula_fields(self.data)
        return Formula(wff, variables)


def _letter_degree(letter) -> int:
    """Returns degree of parentheses nesting for letters."""
    if letter == '(':
        return 1
    elif letter == ')':
        return -1
    else:
        return 0


def _word_degree(word) -> int:
    """Returns degree of parentheses nesting for whole words."""
    degree = 0
    for letter in word:
        degree += _letter_degree(letter)
    return degree


def _convert_list(cedent: list) -> Iterator[Proposition]:
    """Generates converted propositions (from strings)."""
    for string in cedent:
        yield String(string).to_proposition()


def _formula_fields(string):
    for i, letter in enumerate(string):
        if letter == "(":
            wff = string[:i]
            var_string = string[i:].strip("()")
            variables = var_string.split(", ")
            return wff, variables
    raise RuntimeError("{string} has not been formatted correctly.")

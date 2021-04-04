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

from Propositions.Propositions import Conditional, Conjunction, Disjunction,\
                                      Negation, Existential, Universal
from Propositions.BaseClasses import Atom
from Objects.Sequents import Sequent


connectives = {
    "implies": Conditional,
    "and": Conjunction,
    "or": Disjunction,
    "not": Negation,
    "exists": Existential,
    "forall": Universal
}

quantifiers = {
    "exists": Existential,
    "forall": Universal
}


class String:
    def __init__(self, data) -> None:
        if not isinstance(data, str):
            raise TypeError(f"Input {data} must be a string.")
        self.data = data
        self._is_atomic = None

    def __repr__(self) -> str:
        return self.data

    @property
    def contains_connective(self):
        """Checks specifically for non-quantifier strings in self.data."""
        for word in self.data.split(' '):
            if word.strip('()') in connectives.keys():
                break
        else:
            if not self.contains_quantifier:
                return False
        return True

    @property
    def contains_quantifier(self):
        """Checks specifically for quantifier strings in self.data."""
        if "exists" in self.data or "forall" in self.data:
            return True
        else:
            return False

    @property
    def is_atomic(self):
        """Whether self.data contains any connectives."""
        if self._is_atomic is None:
            if self.contains_connective:
                self._is_atomic = False
            else:
                self._is_atomic = True
        return self._is_atomic

    def to_sequent(self) -> Sequent:
        """Returns a sequent from the input."""
        try:
            assert ' |~ ' in self.data
            sides = self.data.split(' |~ ')
            ant_list = sides[0].split(', ')
            con_list = sides[1].split(', ')
            antecedent = [ant for ant in _convert_list(ant_list)]
            consequent = [con for con in _convert_list(con_list)]
            return Sequent(antecedent, consequent)
        except AssertionError:
            raise ValueError(f"{self.data} must be a sequent.")

    def to_proposition(self):
        """Returns a proposition from the input."""
        try:
            assert ' |~ ' not in self.data
            self._deparen()
            if self.is_atomic:
                return self._atom()
            return self._proposition()
        except AssertionError:
            raise ValueError(f"{self.data} must be a Proposition, not Sequent")

    def _atom(self):
        if "(" not in self.data:
            return Atom(self.data)
        *extra, prop, names = self.data[:-1].split("(")
        names = names.strip("()")
        return Atom(prop, names.split("; "))

    def _proposition(self):
        """Gets the type and location of the main connective."""
        if self.contains_quantifier:
            return self._create_quantified()
        else:
            word, index = self._proposition_location()
            return self._create_sentential(word, index)

    def _create_quantified(self):
        quantifier = quantifiers[self.data[:6]]
        var = self.data[7]
        contents = self.data[10:-1]
        prop = String(contents).to_proposition()
        return quantifier(var, prop)

    def _create_sentential(self, connective, index):
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
            left = String(left_string).to_proposition()
            right = String(right_string).to_proposition()
            return proposition(left, right)

    def _proposition_location(self):
        degree = 0
        for index, word in enumerate(self.data.split(" ")):
            degree += _word_degree(word)
            if degree == 0 and word in connectives.keys():
                return word, index

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


def _convert_list(cedent: list):
    """Generates converted propositions (from strings)."""
    for string in cedent:
        yield String(string).to_proposition()


def _letter_generator():
    for letter in map(chr, range(97, 123)):
        yield letter

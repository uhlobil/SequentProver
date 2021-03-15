from collections.abc import MutableMapping
from itertools import product
from typing import Union

from Propositions.Converters import String
from Controllers.Settings import Settings
from Objects.Sequents import Sequent


class Tree(MutableMapping):

    def __init__(self, sequent: Union[Sequent, str]):
        if isinstance(sequent, str):
            sequent = String(sequent).to_sequent()
        if not isinstance(sequent, Sequent):
            raise TypeError(f"{sequent} is neither a Sequent nor a string.")
        self.leaves = {}
        self.update({'0000': sequent})
        self.root = self.leaves['0000']
        self.has_been_truncated = False

    def __repr__(self):
        return f"Tree({self.root})"

    def __getitem__(self, key: str) -> Sequent:
        return self.leaves[key]

    def __setitem__(self, key: str, value: Sequent) -> None:
        self.leaves[key] = value

    def __delitem__(self, key: str) -> None:
        del self.leaves[key]

    def __len__(self) -> int:
        return len(self.leaves)

    def __iter__(self):
        return iter(self.leaves)

    def __eq__(self, other):
        if self.leaves == other.leaves:
            return True
        return False

    def __ne__(self, other):
        if not self == other:
            return True
        return False

    def populate(self) -> None:
        """Pseudo-recursively fills the tree with the results of
        decomposing each sequent in it."""
        for complexity in range(self.root.complexity, 0, -1):
            items = [(k, v) for k, v in self.items()]
            for item in items:
                key = item[0]
                sequent: Sequent = item[1]
                if sequent.complexity == complexity:
                    new_items: dict = self._decompose(key, sequent)
                    self.update(new_items)

    def fill_with(self, dictionary) -> None:
        """Fills the tree with the values in the input dictionary."""
        for key, value in dictionary.items():
            sequent = String(value).to_sequent()
            self.update({key: sequent})

    def _decompose(self, key: str, sequent: Sequent) -> dict:
        """Returns the results of decomposing a sequent as a dictionary
        with keys matching their locations in the tree. If reflexivity
        is off, deletes reflexive results and marks the tree as having
        been truncated."""
        new_items = {}
        children: tuple = sequent.decompose()
        if sequent.principal.proposition.is_invertible:
            new_items.update(_invertible_decomp(children, key))
        else:
            new_items.update(_non_invertible_decomp(children, key))
        if not Settings()['Reflexivity']:
            for new_key, new_sequent in new_items.items():
                if new_sequent.is_reflexive:
                    del new_items[new_key]
                    if not self.has_been_truncated:
                        self.has_been_truncated = True
        return new_items


def _non_invertible_decomp(children: tuple, key: str) -> dict:
    """Returns the results of decomposing non-invertible sequents."""
    cognates = generate_cognates()
    results = {}
    if len(children[0]) == 1:
        for dimension in children:
            result: Sequent = dimension[0]
            cognate = next(cognates)
            new_key = key + cognate + "M"
            results.update({new_key: result})
    else:
        for dimension in children:
            cognate = next(cognates)
            left, right = dimension
            left_key = key + cognate + "L"
            right_key = key + cognate + "R"
            results.update({left_key: left, right_key: right})
    return results


def _invertible_decomp(children: tuple, key: str) -> dict:
    """Returns results of decomposing invertible sequents."""
    if len(children[0]) == 1:
        sequent: Sequent = children[0][0]
        new_key = key + "000M"
        return {new_key: sequent}
    else:
        left, right = children[0]
        left_key = key + "000L"
        right_key = key + "000R"
        return {left_key: left, right_key: right}


def generate_cognates():
    """Produces 3-character combinations of lowercase letters from
    aaa to zzz in order."""
    for i in product(map(chr, range(97, 123)), repeat=3):
        yield ''.join(i)

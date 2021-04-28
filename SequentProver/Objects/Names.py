import json
import os

_current_dir = os.path.dirname(__file__)
_names_path = os.path.join(_current_dir, "..", "data", "Names.json")


def load() -> list:
    with open(_names_path, "r") as file:
        return json.load(file)


def write_names(new_names) -> None:
    with open(_names_path, "w") as file:
        file.write(json.dumps(new_names, indent=4))


def view() -> None:
    print("Current names are:")
    for name in load():
        print(name)


def new() -> None:
    names = set(load())
    name = input("Enter New Name:\n")
    if name not in names:
        names.update([name])
        write_names(sorted(list(names)))


def remove(name):
    with open(_names_path, "r") as file:
        names: list = json.load(file)
    names.remove(name)
    with open(_names_path, "w") as file:
        file.write(json.dumps(names, indent=4))


info = """
Per Dan's Note 118, one of the big issues with having quantifiers in a
material consequence relation is that we sometimes want our objects to 
be linked across the turnstile and across propositions. One solution, 
which I implement here, is to have two kinds of names, additive and 
multiplicative.

"Additive" names are substitutable in left existential and right 
universal quantifiers, which can only be substituted if they don't 
appear anywhere else in the sequent.

"Multiplicative" names are substitutable in the right existential and
left universal quantifiers, which are always substitutable without
restriction.

It seems, though, that because we decompose sequents, we don't actually
have to worry about any of this. A universal or existential could have
come from any name in the domain. The only constraints are those on 
names appearing elsewhere in the sequent, which will differ depending
on the order in which the propositions are placed in the sequent. It
turns out that I've accidentally constructed something with no 
structural rules at all and structural permutation will need to be 
coded in at some point in the future. 
"""

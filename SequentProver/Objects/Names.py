import json
import os

names_path = os.path.join("SequentProver", "data", "Names.json")


def load() -> dict:
    with open(names_path, "r") as file:
        return json.load(file)


def write_names(new_names) -> None:
    with open(names_path, "w") as file:
        file.write(json.dumps(new_names, indent=4))


def view(name_list) -> None:
    print("Current names are:")
    for name in load()[name_list]:
        print(name)


def new(name_list) -> None:
    names_dict = load()
    names = names_dict[name_list]
    name = input("Enter New Name:\n")
    if name not in names:
        names.append(name)
        names_dict.update({name_list: sorted(names)})
        write_names(names_dict)


def remove(name):
    pass


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
"""

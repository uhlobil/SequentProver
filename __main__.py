import os
import shutil

from Controllers.Menus.Main import MainMenu
from Controllers.Rules import Settings


data_path = os.path.join("SequentProver", "data")
ftue_path = os.path.join(data_path, "Presets", "FTUE")
untracked_src_files = ("Atoms.json", "Names.json", "Settings.json")


def main():
    for file in untracked_src_files:
        _initialize_file(file)
    _initialize_runs()
    Settings().update_output_file()
    MainMenu().open()


def _initialize_file(file_name):
    file_path = os.path.join(data_path, file_name)
    if not os.path.exists(file_path):
        ftue_file = os.path.join(ftue_path, file_name)
        shutil.copy(ftue_file, file_path)


def _initialize_runs():
    runs_dir = os.path.join(data_path, "Runs")
    if not os.path.exists(runs_dir):
        os.makedirs(runs_dir)


if __name__ == '__main__':
    main()


"""
Development Stack: 
Feature ideas and bugs that I mean to implement/fix. Issues at the top 
are prioritized and will be completed next. This is probably one of 
the worse ways to implement something like this, but until I find 
something better (read: less work for me to learn to do and maintain),
this is how it will be (not that I'm either looking very hard or 
particularly willing to learn).

Key: 
    Bug -> Issue preventing parser from working as intended.
    Debt -> Quality of life changes that make the code faster, easier 
to read, etc. Usually a result of learning something new.
    Features -> Features to be implemented.

Feature: Names of objects in the language
    - Prerequisite: in data we create a Names.json file containing the
    names of the objects in the language. There are 2 sets of (possibly
    overlapping) names (per dan note 118, p.10):
        - Additive: additive variables, valid for substitution in left
        existential and right universal quantifiers
        - Multiplicative: multiplicative variables, valid for 
        substitution in left universal and right existential 
        quantifiers.
    - There is an option in the main menu to add a name to one or both
    of these sets. 
    - There is an adequate explanation (somewhere) for what makes a 
    name suitable for inclusion in one or more sets.

Feature: Decomposition of Quantified Sequents
    - Prerequisite: a list (or whatever) containing each name in the 
    language (each name ever used). Users can define new names as they 
    please in the main menu, but not during decomposition (as that 
    might result in incomplete trees).
    - Universals: 
        - Input string: "Forall(x)(Proposition(x))" 
            - Risks: We need to make sure that the string-to-prop
            converter doesn't get tripped up by this, as there are 
            three sets of parentheses. We probably want a set around 
            the whole thing and to seek "Forall" as the identifying 
            string, then seek the next set of parentheses and find each
            instance of the variable inside those (maybe including the 
            parentheses themselves). 
        - Output proposition: Universal([var], [Proposition(var)])
        where [var] is some procedurally generated unique (per root)
        string that marks each variable bound by the quantifier.
            - Risks: There's room for error when creating identifiers
            and replacing parts of strings with them, especially with 
            the current conversion converting propositions from the
            inside out, so to speak. 
        - Decomposition_backup: 
            - Left: User picks a name %N in Names.Multiplicative such 
            that Universal(var, Proposition([var])) becomes 
            Proposition([%N/var])
            - Right: For each name %N in Names.Additive, we get a 
            parent sequent which replaces Universal(var, Proposition([var]))
            with Proposition([%N/var]). 
    - Existentials:
        - Input string: "Exists(x)(Proposition(x))"
            - Risks: same as for universals
        - Output proposition: Existential([var], [Proposition(var)])
        where the same conditions and risks apply as for Universals
        - Decomposition_backup:
            - Left: For each name %N in Names.Additive, we get a 
            parent sequent which replaces Existential(var, Proposition([var]))
            with Proposition([%N/var])
            - Right: User picks a name %N in Names.Multiplicative such 
            that Existential(var, Proposition([var])) becomes 
            Proposition([%N/var])

Feature: Atom Viewer
Add a menu option to view atomic sequents. Maybe allow grouping or 
sorting, depending on how difficult that looks. There might be some
desire in viewing this in terms of a material base. For example, having
the option to show "All sequents which contain [x proposition] as a
premise," and other such searches. 

Feature Atom Vetter
Add a submenu to the atom viewer that allows the user to decide which 
atoms are acceptable and which are not. Some results of (especially non
invertible) rule applications are unacceptable for one reason or 
another. We want a list of unacceptable atoms against which to judge 
future decompositions. If a sequent would result in an unacceptable 
atom, we can reject it from the material base.
"""

import os
import shutil

from Controllers.Menus.Handlers import main_menu
from Controllers.Rules import Settings

_main_dir = os.path.dirname(__file__)
_data_path = os.path.join(_main_dir, "data")
_ftue_path = os.path.join(_data_path, "Presets", "FTUE")
_untracked_src_files = ("Atoms.json", "Names.json", "Settings.json")


def main():
    for file in _untracked_src_files:
        _initialize_file(file)
    _initialize_runs()
    Settings().update_output_file()
    main_menu()


def _initialize_file(file_name):
    file_path = os.path.join(_data_path, file_name)
    if not os.path.exists(file_path):
        ftue_file = os.path.join(_ftue_path, file_name)
        shutil.copy(ftue_file, file_path)


def _initialize_runs():
    runs_dir = os.path.join(_data_path, "Runs")
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

Feature: Atom Viewer
Add a menu option to view atomic sequents. Maybe allow grouping or 
sorting, depending on how difficult that looks. There might be some
desire in viewing this in terms of a material base. For example, having
the option to show "All sequents which contain [x proposition] as a
premise," and other such searches. 

Feature: Structural Rule: Permutation
Have a switch that allows the user to choose at each stage of 
decomposition which proposition in the sequent to decompose next. This
will be important for decomposing sequents full of quantifiers, as
the different rules will have different constraints on variables. 

Feature Atom Vetter
Add a submenu to the atom viewer that allows the user to decide which 
atoms are acceptable and which are not. Some results of (especially non
invertible) rule applications are unacceptable for one reason or 
another. We want a list of unacceptable atoms against which to judge 
future decompositions. If a sequent would result in an unacceptable 
atom, we can reject it from the material base.
"""

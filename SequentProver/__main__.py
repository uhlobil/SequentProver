import os      # allows us to deal with directories on the computer
import shutil   # allows us to write and save files

from Controllers.Menus.Handlers import main_menu   # gets the menu "Main.json" from data/Menus
from Controllers.Rules import Settings        # gets the settings of the rules from "Settings.json"

_main_dir = os.path.dirname(__file__)    # sets "_main_dir" to the directory in which this file is running
_data_path = os.path.join(_main_dir, "data")   # sets "_data_path" to the data folder in "_main_dir"
_ftue_path = os.path.join(_data_path, "Presets", "FTUE")   # sets "_ftue_path" to ...SequentProver/data/Presets/FTUE
_untracked_src_files = ("Atoms.json", "Names.json", "Settings.json")  # defines object that we will manipulate


def main():    # opens the main menu and makes sure the necessary files and folders exist
    for file in _untracked_src_files:
        _initialize_file(file)  # makes sure that we have "Atoms", "Names" and "Settings" in "data" folder
    _initialize_runs()     # checks whether the "Runs" folder exists and creates it if necessary
    Settings().update_output_file()   # Updates settings and writes output file
    main_menu()     # Prints and activates the main menu


def _initialize_file(file_name):  # checks that we have files in "SequentProver/data" and if not copies from FTUE
    file_path = os.path.join(_data_path, file_name)  # points to the files in "SequentProver/data"
    if not os.path.exists(file_path):
        _ftue_file = os.path.join(_ftue_path, file_name)
        shutil.copy(_ftue_file, file_path)   # copies from FTUE if needed


def _initialize_runs():  # checks whether the "Runs" folder exists and creates it if necessary
    runs_dir = os.path.join(_data_path, "Runs")
    if not os.path.exists(runs_dir):
        os.makedirs(runs_dir)

# print(os.path.dirname(__file__))  # to see where on your computer the "SequentProver" directory is located

if __name__ == '__main__':    # executes function main() if this code is run from here (as top level)
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

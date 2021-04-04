import json
import os

from Controllers.Menus.Base import Menu
from Controllers import Rules
from Objects import Names


_current_dir = os.path.dirname(__file__)
_data_dir = os.path.join(_current_dir, "..", "..", "data")


def main_menu():
    """Handle main menu."""
    menu_file = os.path.join(_data_dir, "Menus", "Main.json")
    menu = Menu(file=menu_file)
    menu.open()


def view_runs():
    """Handle menu for viewing runs."""
    runs_dir = os.path.join(_data_dir, "Runs")
    option_list = [file for file in os.listdir(runs_dir)]
    label_list = [file for file in option_list]
    menu = Menu(options=zip(label_list, option_list))
    menu.open()


def change_rules():
    """Handle menu for changing rules."""
    menu_file = os.path.join(_data_dir, "Menus", "ChangeRules.json")
    menu = Menu(file=menu_file)
    menu.open()


def change_single():
    """Change single rule."""
    menu_file = os.path.join(_data_dir, "Menus", "ChangeSingle.json")
    menu = Menu(file=menu_file)
    rule = menu.open()
    Rules.change_single(rule)


def change_multiple():
    """Change multiple rules."""
    rule_file = os.path.join(_data_dir, "Menus", "ChangeMultiple.json")
    rules_menu = Menu(file=rule_file)
    group = rules_menu.open()

    mode_file = os.path.join(_data_dir, "Menus", "ChangeMode.json")
    mode_menu = Menu(file=mode_file)
    mode = mode_menu.open()

    Rules.change_multiple(group, mode)


def change_structure():
    """Change structural rule."""
    menu_file = os.path.join(_data_dir, "Menus", "ChangeStructure.json")
    menu = Menu(file=menu_file)
    rule = menu.open()
    Rules.change_structure(rule)


def names_menu():
    """Handle menu for viewing/changing names."""
    menu_file = os.path.join(_data_dir, "Menus", "ViewNames.json")
    menu = Menu(file=menu_file)
    menu.open()


def remove_name():
    """Remove selected name from Names.json."""
    names_file = os.path.join(_data_dir, "Names.json")
    with open(names_file, "r") as file:
        names = json.load(file)
    menu = Menu(options=names)
    selection = menu.open()
    Names.remove(selection)

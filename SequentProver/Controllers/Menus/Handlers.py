import json
import os

from Controllers.Menus.Base import Menu
from Controllers import Rules
from Objects import Names
from View import DisplayTrees

_current_dir = os.path.dirname(__file__)
_data_dir = os.path.join(_current_dir, "..", "..", "data")
_runs_dir = os.path.join(_data_dir, "Runs")


def main_menu():
    """Handle main menu."""
    menu_file = os.path.join(_data_dir, "Menus", "Main.json")
    main = Menu(file=menu_file)
    main.open()


def view_run(run):
    """Display a single run."""
    run_file = os.path.join(_runs_dir, run)
    with open(run_file, "r") as file:
        forest = json.load(file)

    forest_menu = Menu()
    forest_menu.extend([
        (x, lambda *args: DisplayTrees.display(y)) for x, y in forest.items()
    ])
    forest_menu.open()


def view_runs():
    """Handle menu for viewing runs."""
    menu_file = os.path.join(_data_dir, "Menus", "View_Runs.json")
    view_menu = Menu(file=menu_file, close_after_choice=True)
    option_list = [file for file in os.listdir(_runs_dir)]
    label_list = [file for file in option_list]
    view_menu.extend(zip(label_list, option_list))
    run = view_menu.open()
    if run is not None:
        view_run(run)


def change_rules():
    """Handle menu for changing rules."""
    menu_file = os.path.join(_data_dir, "Menus", "Change_RulesSuperMenu.json")
    rules_menu = Menu(file=menu_file)
    rules_menu.open()


def change_single():
    """Change single rule."""
    menu_file = os.path.join(_data_dir, "Menus", "Change_SingleRule.json")
    rule_menu = Menu(file=menu_file)
    rule = rule_menu.open()
    Rules.change_single(rule)


def change_multiple():
    """Change multiple rules."""
    rule_file = os.path.join(_data_dir, "Menus", "Change_MultipleRules.json")
    rules_menu = Menu(file=rule_file)
    group = rules_menu.open()

    mode_file = os.path.join(_data_dir, "Menus", "Change_RuleMode.json")
    mode_menu = Menu(file=mode_file)
    mode = mode_menu.open()

    Rules.change_multiple(group, mode)


def change_structure():
    """Change structural rule."""
    menu_file = os.path.join(_data_dir, "Menus", "Change_StructuralRule.json")
    menu = Menu(file=menu_file)
    rule = menu.open()
    Rules.change_structure(rule)


def names_menu():
    """Handle menu for viewing/changing names."""
    menu_file = os.path.join(_data_dir, "Menus", "View_Names.json")
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


def delete_runs_confirm():
    """Confirm user wants to delete contents of Runs directory."""
    menu_file = os.path.join(_data_dir, "Menus", "Confirm_DeleteRuns.json")
    menu = Menu(file=menu_file, close_after_choice=True)
    menu.open()

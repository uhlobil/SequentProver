import json
import os

from Controllers.Menus.Base import Menu
from Controllers import Rules
from Controllers.Settings import Settings
from Objects import Names
from View import DisplayTrees

_current_dir = os.path.dirname(__file__)
_data_dir = os.path.join(_current_dir, "..", "..", "data")
_runs_dir = os.path.join(_data_dir, "Runs")


def main_menu():
    """Handle main menu."""
    menu_file = os.path.join(_data_dir, "Menus", "Main.json")  # Main menu is Main.json in .../data/Menus
    main = Menu(file=menu_file)
    Settings().print_rules()   # Prints the rules on top of the main menu
    main.open()    # Executes "open" from Controllers.Menu.Base with "main"


def view_run(run):
    """Display a single run."""
    run_file = os.path.join(_runs_dir, run)
    with open(run_file, "r") as file:
        forest = json.load(file)
    forest_menu = Menu()
    forest_menu.clear_after_print = False

    def display(t):
        return lambda: DisplayTrees.display(t)

    callable_options = map(display, forest.values())
    option_list = zip(forest.keys(), callable_options)
    forest_menu.extend(option_list)
    forest_menu.open()


def view_runs():
    """Handle menu for viewing runs."""
    def set_options(menu, file):
        option_list = [option for option in os.listdir(_runs_dir)]
        label_list = [label for label in option_list]
        menu.options = []
        menu.load(file)
        menu.extend(zip(label_list, option_list))

    menu_file = os.path.join(_data_dir, "Menus", "View_Runs.json")
    view_menu = Menu()
    view_menu.close_after_choice = True
    set_options(view_menu, menu_file)
    run = view_menu.open()
    if run is not None:
        view_run(run)
        set_options(view_menu, menu_file)


def change_rules():
    """Handle menu for changing rules."""
    menu_file = os.path.join(_data_dir, "Menus", "Change_RulesSuperMenu.json")
    rules_menu = Menu(file=menu_file)
    Settings().print_rules()
    rules_menu.open()


def change_single():
    """Change single rule."""
    menu_file = os.path.join(_data_dir, "Menus", "Change_SingleRule.json")
    rule_menu = Menu(file=menu_file)
    Settings().print_rules()
    rule = rule_menu.open()
    if rule:
        Rules.change_single(rule)


def change_multiple():
    """Change multiple rules."""
    rule_file = os.path.join(_data_dir, "Menus", "Change_MultipleRules.json")
    rules_menu = Menu(file=rule_file)
    Settings().print_rules()
    group = rules_menu.open()

    mode_file = os.path.join(_data_dir, "Menus", "Change_RuleMode.json")
    mode_menu = Menu(file=mode_file)
    mode = mode_menu.open()
    if group and mode:
        Rules.change_multiple(group, mode)


def change_structure():
    """Change structural rule."""
    menu_file = os.path.join(_data_dir, "Menus", "Change_StructuralRule.json")
    menu = Menu(file=menu_file)
    Settings().print_rules()
    rule = menu.open()
    if rule:
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
        name_list = json.load(file)
        options = [(name, name) for name in name_list]
    menu = Menu()
    menu.extend(options)
    selection = menu.open()
    if selection:
        Names.remove(selection)


def delete_runs_confirm():
    """Confirm user wants to delete contents of Runs directory."""
    menu_file = os.path.join(_data_dir, "Menus", "Confirm_DeleteRuns.json")
    menu = Menu(file=menu_file)
    menu.close_after_choice = True
    menu.open()

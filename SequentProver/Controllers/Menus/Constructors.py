import os

from Controllers.Menus.Base import Menu


_current_dir = os.path.dirname(__file__)
_data_dir = os.path.join(_current_dir, "..", "..", "data")


def view_runs():
    runs_dir = os.path.join(_data_dir, "Runs")
    option_list = [file for file in os.listdir(runs_dir)]
    view_menu = Menu(options=option_list)
    view_menu.open()


def change_rules():
    menu_file = os.path.join(_data_dir, "Menus", "ChangeRules.json")
    rules_menu = Menu(file=menu_file)
    rules_menu.open()


def change_single():
    pass


def change_multiple():
    pass


def change_structure():
    pass


def view_names():
    pass

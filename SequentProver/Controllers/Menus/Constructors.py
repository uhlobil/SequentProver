import os

from Controllers.Menus.Base import Menu


_current_dir = os.path.dirname(__file__)
_data_dir = os.path.join(_current_dir, "..", "..", "data")


def view_runs():
    runs_dir = os.path.join(_data_dir, "Runs")
    option_list = [file for file in os.listdir(runs_dir)]
    label_list = [file for file in option_list]
    view_menu = Menu(options=zip(label_list, option_list))
    view_menu.open()


def change_rules():
    menu_file = os.path.join(_data_dir, "Menus", "ChangeRules.json")
    rules_menu = Menu(file=menu_file)
    rules_menu.open()


def change_single():
    menu_file = os.path.join(_data_dir, "Menus", "ChangeSingle.json")
    rules_menu = Menu(file=menu_file)
    rules_menu.open()


def change_multiple():
    rule_file = os.path.join(_data_dir, "Menus", "ChangeMultiple.json")
    rules_menu = Menu(file=rule_file)
    group = rules_menu.open()

    mode_file = os.path.join(_data_dir, "Menus", "ChangeMode.json")
    mode_menu = Menu(file=mode_file)
    mode = mode_menu.open()


def change_structure():
    pass


def view_names():
    pass

from Controllers.ImportExport import Decompose
from Controllers.Menus.Base import Menu, confirm_menu
from Controllers.Menus.Display import ViewRuns
from Controllers.Menus.Settings import ChangeRules, ViewNames
from Controllers.Settings import Settings


class MainMenu(Menu):
    """The main menu."""
    options = [
        "Decompose Sequents",
        "View Runs",
        "Change Rules",
        "Check/Change Names",
        "Check/Change Sequent File"
    ]

    def __init__(self):
        super().__init__()
        self.input_file = Settings()['Input File']
        Settings().print_rules()

    def run(self, selection):
        if selection == 1:
            try:
                Decompose(self.input_file).sequents()
            except FileNotFoundError:
                print("Specified input file could not be found."
                      "\nPlease verify input file.")
        elif selection == 2:
            ViewRuns().open()
        elif selection == 3:
            ChangeRules().open()
        elif selection == 4:
            ViewNames().open()
        elif selection == 5:
            if confirm_menu(f"Current Sequent File is {self.input_file}.\n"
                            "Would you like to change it?"):
                Settings().update_input_file()
                self.input_file = Settings()['Input File']
        Settings().print_rules()



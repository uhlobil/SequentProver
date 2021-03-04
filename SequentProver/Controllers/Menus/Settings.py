from Controllers import Rules
from Controllers.Menus.Base import Menu
from Controllers.Settings import Settings
from Objects import Names


class ChangeRules(Menu):
    """Menu for selecting what kind of rules to change."""
    separator = "=" * 78
    options = [
        "Change Single Rule",
        "Change Multiple Rules",
        "Change Structural Rule"
    ]

    def __init__(self):
        super().__init__()
        Settings().print_rules()

    def run(self, selection):
        if selection == 1:
            ChangeSingle().open()
        elif selection == 2:
            ChangeMultiple().open()
        elif selection == 3:
            ChangeStructure().open()
        Settings().print_rules()


class ChangeMultiple(Menu):
    """Requests a mode then changes the selected """
    options = [
        "Conditionals",
        "Conjunctions",
        "Disjunctions",
        "Left Rules",
        "Right Rules",
        "All Rules"
    ]

    def __init__(self):
        super().__init__()
        Settings().print_rules()
        self.exit = False

    def run(self, selection):
        mode: str = SelectMode().get()
        rule = ""
        if selection == 1:
            rule = "->"
        elif selection == 2:
            rule = "&"
        elif selection == 3:
            rule = "v"
        elif selection == 4:
            rule = "L"
        elif selection == 5:
            rule = "R"
        elif selection == 6:
            pass
        Rules.change_multiple(rule, mode)


class ChangeStructure(Menu):
    options = [
        "Toggle Reflexivity",
        "Toggle Contraction"
    ]

    def __init__(self):
        super().__init__()
        self.exit = False

    def run(self, selection):
        if selection == 1:
            Rules.change_structure("Reflexivity")
        elif selection == 2:
            Rules.change_structure("Contraction")


class SelectMode(Menu):
    options = [
        "Reverse Current Rules",
        "Preset: Invertible",
        "Preset: Non-Invertible"
    ]

    def run(self, selection):
        if selection == 1:
            return "Reverse"
        elif selection == 2:
            return "Invertible"
        elif selection == 3:
            return "NonInvertible"


class ChangeSingle(Menu):
    options = [
        "Left Conditional",
        "Right Conditional",
        "Left Conjunction",
        "Right Conjunction",
        "Left Disjunction",
        "Right Disjunction"
    ]

    def __init__(self):
        super().__init__()
        Settings().print_rules()
        self.exit = False

    def run(self, selection):
        rule: str = ""
        if selection == 1:
            rule = "L->"
        elif selection == 2:
            rule = "R->"
        elif selection == 3:
            rule = "L&"
        elif selection == 4:
            rule = "R&"
        elif selection == 5:
            rule = "Lv"
        elif selection == 6:
            rule = "Rv"
        Rules.change_single(rule)


class ViewNames(Menu):
    options = [
        "View Additive Names",
        "Add Additive Name",
        "Remove Additive Name",
        "View Multiplicative Names",
        "Add Multiplicative Name",
        "Remove Multiplicative Name",
        "Info"
        ]

    def run(self, selection):
        if selection == 1:
            Names.view("Additive")
        elif selection == 2:
            Names.new("Additive")
        elif selection == 3:
            name = RemoveName("Additive").get()
            Names.remove(name)
        elif selection == 4:
            Names.view("Multiplicative")
        elif selection == 5:
            Names.new("Multiplicative")
        elif selection == 6:
            name = RemoveName("Multiplicative").get()
            Names.remove(name)
        elif selection == 7:
            print(Names.info)


class RemoveName(Menu):
    def __init__(self, name_list):
        super().__init__()
        self.options = [name for name in Names.load()[name_list]]

    def run(self, selection):
        return self.options[selection - 1]

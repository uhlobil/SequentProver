import json
import importlib
from collections import namedtuple
from os import system


Option = namedtuple("Option", "label, command")


class Menu:
    _separator = "=" * 78
    options = []

    def __init__(self, file=None, options=None):
        """Create and handle menu.

        Menu's options are equal to whichever of file or options is not
        none (preferring file if both are filled). If neither parameter
        is passed, makes sure user can at least exit the menu by adding
        an exit button.

        :param file: a path to a json file as a string.
        :param options: A sequence of 2-tuples, (label, command)
        """
        self.alive = True
        self.prompt = "Please Select: \n"
        if file is not None:
            self.load(file)
        elif options is not None:
            self.extend(options)
        else:
            self.options = [
                Option("Exit", self.exit)
            ]

    def open(self):
        self._clear()
        return_value = None
        while self.alive is True and return_value is None:
            self._show_options()
            choice = self._get_input()
            return_value = self._handle(choice)
        return return_value

    def exit(self):
        self.alive = False

    def load(self, file: str):
        """Fill the menu with the contents of (json) file

        Format the file thus:
        {
            "option label 1": [
                "function source package",
                "function name"
            ],
            "option label 2": [
                ...
            ],
            ...
        }

        Lambdas and strings use "" as the function source package.
        Strings have a "'second pair of single quotes'" around them
        because I'm using eval().
        """
        with open(file, "r") as target:
            file = json.load(target)
        options = []
        for label, contents in file.items():
            module = importlib.import_module(contents[0]) if contents[0] else None
            function = getattr(module, contents[1]) if module else eval(contents[1])
            options.append(Option(label, function))
        self.extend(options)

    def extend(self, options):
        """Append options to list.

        :param options: a sequence of 2-length sequences
        options should look like (Label, Command). Label can be anything
        that implements __str__ and command is either a string or a
        callable (including lambdas).
        """
        for option in options:
            if len(option) != 2:
                raise IndexError(f"Option {option} must contain 2 items")
            self.options.append(Option(str(option[0]), option[1]))

    def _clear(self):
        """Print enough newlines to clear the terminal."""
        system("clear")
        print(self._separator)

    def _show_options(self):
        """Print menu's options."""
        for i, option in enumerate(self.options):
            number = f"{str(i).rjust(2, ' ')}. "
            print(number, option.label)

    def _get_input(self):
        """Handle retrieving input."""
        result = None
        try:
            choice = int(input(self.prompt))
            result = self.options[choice].command
        except (IndexError, ValueError):
            self._clear()
            print("Unknown Option Selected.")
        return result

    def _handle(self, choice):
        """Handle choice"""
        if choice is not None:
            if isinstance(choice, str):
                return choice
            elif callable(choice):
                choice()
        else:
            self._clear()
        return None

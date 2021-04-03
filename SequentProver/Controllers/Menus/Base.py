import json
import importlib
from collections import namedtuple
from typing import Sequence
from os import system


Option = namedtuple("Option", "label, command")


class Menu:
    _separator = "=" * 78
    options = []

    def __init__(self, file=None, options=None):
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
        while self.alive is True:
            self._show_options()
            choice = self._get_input()
            self._handle(choice)

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
        """

        with open(file, "r") as target:
            file = json.load(target)
        options = []
        for label, contents in file.items():
            module = importlib.import_module(contents[0]) if contents[0] else None
            function = getattr(module, contents[1]) if module else eval(contents[1])
            options.append(Option(label, function))
        self.extend(options)

    def extend(self, options: Sequence):
        for option in options:
            if len(option) != 2:
                raise IndexError(f"Option {option} must contain 2 items")
            if not callable(option[1]):
                raise ValueError(f"{option[1]} must be callable.")
            self.options.append(Option(str(option[0]), option[1]))

    def _clear(self):
        system("clear")
        print(self._separator)

    def _show_options(self):
        for i, option in enumerate(self.options):
            number = f"{str(i).rjust(2, ' ')}. "
            print(number, option.label)

    def _get_input(self):
        result = None
        try:
            choice = int(input(self.prompt))
            result = self.options[choice].command
        except (IndexError, ValueError):
            self._clear()
            print("Unknown Option Selected.")
        return result

    def _handle(self, choice):
        if choice is not None:
            if isinstance(choice, str):
                return str
            elif callable(choice):
                choice()
        else:
            self._clear()
        return None

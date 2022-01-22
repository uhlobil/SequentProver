import json
import os
import tkinter as tk     # provides the functions for entering a new input file via a dialog box
from datetime import datetime
from tkinter import filedialog    # provides the functions for entering a new input file via a dialog box


_current_dir = os.path.dirname(__file__)


class _Settings:     # Is the object that we operate on when we change the settings
    file = os.path.join(_current_dir, "..", "data", "Settings.json")   # This object is the settings file in "data"
    separator = "=" * 78      # Defines the equal sign separator at the top of the menu

    def __init__(self):
        with open(self.file, "r") as file:
            self.dict = json.load(file)

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        new_item = {key: value}
        self.dict.update(new_item)
        with open(self.file, "w") as file:
            file.write(json.dumps(self.dict, indent=4))

    def __delitem__(self, key):
        del self.dict[key]

    def update_output_file(self):    # function that writes the the output files in the "data/Runs" folder.
        now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self["Output File"] = f"{now}.json"

    def update_input_file(self):     # function that allows one to enter a new file with input sequents
        window = tk.Tk()
        window.withdraw()
        file_path = filedialog.askopenfilename()
        if file_path:
            self["Input File"] = str(file_path)

    @property
    def rules(self):
        rules = self['Sequent Rules']
        for key, rule in rules.items():
            yield f'{key}: {rule}'

    def get_rules(self):
        rules = {"Rules": [rule for rule in self.rules]}
        for rule in ["Contraction", "Reflexivity"]:
            if self.dict[rule]:
                rules[rule] = "On"
            else:
                rules[rule] = "Off"
        return rules

    def get_rule(self, symbol: str):
        return self['Sequent Rules'][symbol]

    def print_rules(self):    # Defines printing the rules on top of the main menu
        rules = self.get_rules()
        print(self.separator)   # Prints equal signs separator
        print("Current Rules:")
        print(f'Connectives: {", ".join(rules["Rules"])}')
        print(f'Contraction: {rules["Contraction"]}, '
              f'Reflexivity: {rules["Reflexivity"]}')


settings = None


def Settings():
    global settings
    if settings is None:
        settings = _Settings()
    return settings


def update_input_file():
    Settings().update_input_file()


def delete_runs_files():
    runs_dir = os.path.join(_current_dir, "..", "data", "Runs")
    for file in os.listdir(runs_dir):
        run = os.path.join(runs_dir, file)
        os.remove(run)

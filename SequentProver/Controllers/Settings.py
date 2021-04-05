import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog


_current_dir = os.path.dirname(__file__)


class _Settings:
    file = os.path.join(_current_dir, "..", "data", "Settings.json")
    separator = "=" * 78

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

    def update_output_file(self):
        now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self["Output File"] = f"{now}.json"

    def update_input_file(self):
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

    def print_rules(self):
        rules = self.get_rules()
        print(self.separator)
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

import os
import json

from Controllers.Menus.Base import Menu


_current_dir = os.path.dirname(__file__)


class MultiplicativeNameMenu(Menu):
    names_file = os.path.join(_current_dir, "..", "..", "data", "Names.json")

    def __init__(self):
        super(MultiplicativeNameMenu, self).__init__()
        with open(self.names_file) as names:
            self.options = [o for o in json.load(names)]

    def run(self, selection):
        pass


class AdditiveNameMenu(Menu):
    def run(self, selection):
        pass
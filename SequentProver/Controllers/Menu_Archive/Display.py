import os

from Controllers.ImportExport import Import
from Controllers.Menus.Base import Menu
from View.DisplayTrees import display


_current_dir = os.path.dirname(__file__)


class ViewRuns(Menu):
    """Menu for selecting which Runs file to view."""
    path = os.path.join(_current_dir, "..", "..", "data", "Runs")
    confirm_msg = "This will delete all previously saved runs. \n" \
                  "This action cannot be undone."

    def __init__(self) -> None:
        super().__init__()
        self.options = ["Clear Runs"]
        files = [file for file in os.listdir(self.path)]
        self.options.extend(sorted(files))

    def run(self, selection):
        if selection == 1:
            self.cleanup()
        else:
            file = self.options[selection - 1]
            file_path = os.path.join(self.path, file)
            ViewTree(file_path).open()

    def cleanup(self):
        if confirm_menu(self.confirm_msg):
            for file in os.listdir(self.path):
                path = os.path.join(self.path, file)
                os.remove(path)
            self.options = ["Clear Runs"]


class ViewTree(Menu):
    """Menu for selecting a tree to view from the file chosen in
    ViewRuns."""

    def __init__(self, file):
        super().__init__()
        self.trees = {str(tree.root): tree for tree in Import(file).trees()}
        self.options = [key for key in self.trees.keys()]

    def run(self, selection):
        root = self.options[selection - 1]
        tree = self.trees[root]
        display(tree)

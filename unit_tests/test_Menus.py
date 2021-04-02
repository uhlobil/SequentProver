import os
import sys
import unittest
from io import StringIO
from contextlib import contextmanager
from unittest.mock import patch

from Controllers.Menus.Base import Menu, Option


current_dir = os.path.dirname(__file__)


# Stolen from https://stackoverflow.com/a/17981937
# Yields standard output so that we can test menu printing, etc.
@contextmanager
def capture_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestMenus(unittest.TestCase):
    def setUp(self):
        self.menu = Menu()

    def test_menu_starts_with_quit_item(self):
        self.assertEqual("Exit", self.menu.options[0].label)

    def test_menu_options(self):
        options = [
            Option("wow", lambda: print("much wow")),
        ]
        self.menu.extend(options)
        selections = ["1", "0"]
        expected = "much wow"
        with patch("builtins.input", selections.pop(0)):
            with capture_output() as (out, err):
                self.menu.open()
                self.assertEqual(expected, out)

    def test_menu_loads_file(self):
        mock_file = os.path.join(current_dir, "mocks", "Menus", "TestMenu.json")
        self.menu.load(mock_file)


if __name__ == '__main__':
    unittest.main()

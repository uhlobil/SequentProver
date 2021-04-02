import sys
import unittest
from io import StringIO
from contextlib import contextmanager
from unittest.mock import patch

from Controllers.Menus.Base import Menu


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

    def test_menu_quits(self):
        def lady():
            for letter in "Lady":
                print(letter)
            print("Lady")

        def cats():
            kittens = ("Luros", "Lazarus")
            for cat in kittens:
                print(cat)

        options = [
            ("wow", lambda: print("much wow")),
            ("cats", cats),
            ("func", lady)
        ]
        self.menu.extend(options)
        selections = [1, 0, 2, 0, 3, 0]
        expected = ["much wow", ["Luros", "Lazarus"], ["L", "a", "d", "y"]]
        with patch("builtins.input", selections.pop(0)):
            for i, _ in enumerate(options):
                with capture_output() as (out, err):
                    self.menu.open()
                    self.assertEqual(expected[i], out)



if __name__ == '__main__':
    unittest.main()

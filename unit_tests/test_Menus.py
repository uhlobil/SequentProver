import io
import os
import unittest
from unittest.mock import patch
from Controllers.Menus.Base import Menu


current_dir = os.path.dirname(__file__)


class TestMenus(unittest.TestCase):
    def setUp(self):
        self.menu = Menu()
        self.mock_file = os.path.join(current_dir, "mocks", "Menus", "TestMenu.json")

    def capture_menu_output(self, inputs: list):
        """Helper method for capturing menu outputs.

        @:param inputs: a list of ints representing desired menu options
        (For results, last item should be enough 0s to exit the program.)
        """
        with patch("builtins.input", side_effect=inputs):
            with patch("Controllers.Menus.Base.Menu._show_options",
                       new=lambda *args: print("")):
                with patch("sys.stdout",
                           new_callable=io.StringIO) as captured_out:
                    self.menu._separator = ""
                    self.menu.open()
                    return captured_out.getvalue().strip()

    def test_menu_starts_with_quit_item(self):
        self.assertEqual("Exit", self.menu.options[0].label)

    def test_menu_options(self):
        test_options = [
            ("wow", lambda *args: print("much wow"))
        ]
        self.menu.extend(test_options)
        output = self.capture_menu_output(inputs=[1, 0])
        self.assertEqual("much wow", output)

    def test_basic_lambda_from_file(self):
        self.menu.load(self.mock_file)
        output = self.capture_menu_output(inputs=[1, 0])
        self.assertEqual("Lady", output)

    def test_import_package_using_file(self):
        self.menu.load(self.mock_file)
        with patch("builtins.input", return_value=2):
            result = self.menu.open()
            self.assertEqual("test", result.prop)

    def test_non_callable_options_return(self):
        self.menu.load(self.mock_file)
        with patch("builtins.input", return_value=3):
            result = self.menu.open()
            self.assertEqual("TEST_STRING", result)


if __name__ == '__main__':
    unittest.main()

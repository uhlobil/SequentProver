import unittest
from Controllers.Menus.Handlers import main_menu


class TestMainMenu(unittest.TestCase):
    def test_main_menu_opens(self):
        main_menu()




if __name__ == '__main__':
    unittest.main()

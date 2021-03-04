from collections import namedtuple


class Menu:
    """
    Base class for menu creation.

    To subclass: create an options instance property (or class property
    if you don't expect it to change at runtime) and create a
    run(self, selection) containing a switch statement based on which
    selection is chosen (numbers start at 1 because 0 is always 'exit').

    self.open() makes a menu with real options that do things.
    self.get() returns input from self.options.
    You may desire for both of these to work, but they don't so you'll
    have to overwrite them in your base class because that's not
    currently supported.
    """

    options = []

    def __init__(self, message='Please Select:'):
        self.exit = False
        self.message = message

    def open(self):
        """Executes the selected option. Use only if self.options
        contains functions or methods."""
        while not self.exit:
            selection = MenuHandler(self.options, message=self.message).handle()
            if selection == 0:
                print('Exit')
                self.exit = True
            else:
                print(self.options[selection - 1])
                self._select(selection)

    def get(self):
        """Returns the selected option. Use only if self.options
        contains data (or be prepared for whatever comes out)."""
        selection = MenuHandler(self.options, message=self.message).handle()
        if selection == 0:
            print('Exit')
        else:
            print(f'Selected: {self.options[selection - 1]}')
            return self._select(selection)

    def _select(self, selection):
        """Routes the correct option into self.run()."""
        for i, _ in enumerate(self.options):
            if selection == i + 1:
                choice = self.run(selection)
                return choice

    def run(self, selection):
        """Switch statement for i, _ in enumerate(options)."""
        raise NotImplementedError
        # if selection == 1:
        #   do option 1
        # elif selection == 2:
        #   do option 2
        # ...


def confirm_menu(explanation):
    """Throws up a confirm dialogue, in case you don't want to run
    an option accidentally."""
    selection = MenuHandler(
        options=['Continue'],
        message=explanation
    ).handle()
    return bool(selection)


class MenuHandler:
    """Displays and handles input for menus"""
    separator = '=' * 78
    message = False

    def __init__(self, options=None, message=None):
        if options is None:
            options = []
        menu_option = namedtuple('Option', 'label')
        self.options = {0: menu_option("Exit")}
        for index, value in enumerate(options):
            self.options.update({1 + index: menu_option(value)})

        if message:
            self.message = message

    def handle(self, input_message='Please Select: '):
        """Returns input if it is a valid option, otherwise asks for
        input again."""
        while True:
            selection = self._get_input(input_message)
            if selection in self.options.keys():
                return selection
            else:
                print('Unknown Input!')

    def _get_input(self, input_message):
        """Collects input and returns it as an integer. Non-integer
        responses are not allowed."""
        try:
            self._print()
            choice = input(input_message)
            return int(choice)
        except ValueError:
            return

    def _print(self):
        """Prints the instance's options."""
        print(self.separator)
        if self.message:
            print(self.message)
        for option in sorted(self.options.keys()):
            print(f'{option}. {self.options[option].label}')
from collections import UserString

from Controllers.Settings import Settings
from Objects.Sequents import Sequent
from Objects.Trees import Tree


class Display:
    _separator = "=" * 78

    def __init__(self, tree: Tree) -> None:
        self.is_contractive: bool = Settings()['Contraction']
        self.display_list: list = [Key('0000')]
        self.declined: set = set()
        self._exit: bool = False
        self.tree = tree
        self._keys = [Key(k) for k in tree.keys()]
        self._max_len = max([len(k) for k in self._keys])

    def populate(self) -> None:
        location_length = 8
        while location_length <= self._max_len and not self._exit:
            for key in self._keys:
                if key.can_be_displayed(
                        display_list=self.display_list,
                        declined=self.declined,
                        length=location_length
                ):
                    if key.is_invertible:
                        self._add_to_display_list(key)
                    else:
                        self._handle_explosion(key)
                if self._exit:
                    break
            location_length += 4

    def display(self) -> None:
        if not self._exit:
            print(self._separator)
            sorted_keys = sorted([key for key in self.display_list])
            for line, key in enumerate(sorted_keys):
                self._draw_line(line, key)

    def _draw_line(self, line: int, key) -> None:
        sequent = self.tree[str(key)]
        rule: str = self._format_rule(key)
        buffer = f"{line:02d}. {rule}|"
        buffer += ("\t|" * (int(len(key) / 4) - 1))
        print(f"{buffer}{sequent}")

    def _add_to_display_list(self, key) -> None:
        self.display_list.append(key)
        if key.has_partner:
            if self.is_contractive:
                self._eliminate_invalid_key_partners(key)
            else:
                self.display_list.append(key.partner)
        if not key.is_invertible:
            for cognate in key.cognates(self._keys):
                if cognate != key:
                    self.declined.update([cognate])
                    self._eliminate_key_children(cognate, check_partner=(not self.is_contractive))

    def _eliminate_invalid_key_partners(self, key) -> None:
        if key.partner is not None:
            if key.partner not in self.display_list and key.partner not in self.declined:
                self.declined.update([key.partner])
                self._eliminate_key_children(key.partner, check_partner=False)

    def _eliminate_key_children(self, key, check_partner: bool) -> None:
        for _key in self._keys:
            if key in _key:
                self.declined.update([_key])
                if check_partner:
                    self._eliminate_invalid_key_partners(_key)

    def _handle_explosion(self, key) -> None:
        options = [cognate for cognate in key.cognates(self._keys)]
        filtered_options = [o for o in options if o not in self.declined]
        if len(filtered_options) == 1:
            self._add_to_display_list(filtered_options[0])
        else:
            self._open_explosion_menu(filtered_options)

    def _open_explosion_menu(self, option_keys) -> None:
        options = [self.tree[str(key)] for key in option_keys]
        message = self._explosion_message(option_keys[0])
        selection = Explosion(options, message).get()
        if selection is None:
            self.exit = True
            return
        key = Key(option_keys[selection - 1])
        self._add_to_display_list(key)

    def _explosion_message(self, key) -> str:
        parent_sequent = self.tree[key.parent]
        variable = ""
        if key.last == "L":
            variable = " left"
        elif key.last == "R":
            variable = " right"
        return f"Select desired{variable} child of {parent_sequent}"

    def _format_rule(self, key) -> str:
        if key.parent:
            parent: Sequent = self.tree[str(key.parent)]
            symbol: str = parent.principal.proposition.symbol
            rule: str = ""
            if parent.principal.side == "ant":
                rule = "L" + symbol
            else:
                rule = "R" + symbol
            return rule.rjust(4, " ")
        else:
            return "ROOT"


class Key(UserString):

    def __init__(self, seq: object):
        super().__init__(seq)
        self.locations = [(self.data[i:i + 4]) for i in range(0, len(self.data), 4)]
        self._partner = None
        self.parent: str = "".join(self.locations[:-1]) if self.data != "0000" else ""
        self.last = self.data[-1]
        self.cognate_space = self.data[-4:-1]
        self.last_four = self.locations[-1]
        self.has_partner = True if self.last in {"L", "R"} else False
        self.is_invertible = True if self.cognate_space == "000" else False

    def __repr__(self) -> str:
        return f"Key({self.data})"

    def __str__(self) -> str:
        return self.data

    def __len__(self) -> int:
        return len(self.data)

    def __contains__(self, item) -> bool:
        if item.data in self.data:
            return True
        return False

    @property
    def partner(self):
        """Returns this key's partner, or None if it has no partner"""
        if self.has_partner:
            if self._partner is None:
                if self.last == "L":
                    self._partner = Key(self.data[:-1] + "R")
                elif self.last == "R":
                    self._partner = Key(self.data[:-1] + "L")
            return self._partner
        else:
            return None

    def cognates(self, key_list):
        for key in key_list:
            if self.is_cognate_of(key):
                yield key

    def is_cognate_of(self, key) -> bool:
        if self.last == key.last and self.parent == key.parent:
            return True
        return False

    def can_be_displayed(self, display_list, declined, length):
        """If the key is of the right length and is neither already in
        display nor declined, then it can be added to the display list.
        (see View.DisplayTree for more info)."""
        if len(self) == length and self not in display_list and self not in declined:
            return True
        return False


def display(tree):
    display_tree = Display(tree)
    display_tree.populate()
    display_tree.display()

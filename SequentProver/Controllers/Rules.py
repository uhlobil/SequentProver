import json
import os

from Controllers.Settings import Settings


_preset_path = os.path.join('SequentProver', 'data', 'Presets', 'Rules')
_sides = {"L", "R"}
_connectives = {"->", "&", "v"}


def change_single(rule):
    if Settings()["Sequent Rules"][rule] == "Add":
        Settings()["Sequent Rules"][rule] = "Mult"
    elif Settings()["Sequent Rules"][rule] == "Mult":
        Settings()["Sequent Rules"][rule] = "Add"


def change_structure(rule):
    if Settings()[rule] == "On":
        Settings()[rule] = "Off"
    elif Settings()[rule] == "Off":
        Settings()[rule] = "On"


def change_multiple(rule, mode):
    if mode == "Reverse":
        rules = [r for r in _rules() if (r[0] == rule or r[1:] == rule)]
        for r in rules:
            change_single(r)
    else:
        preset = _load_preset(mode)
        rules = []
        if rule:
            rules = [r for r in _rules() if (r[0] == rule or r[1:] == rule)]
        else:
            rules = [r for r in _rules()]
        for r in rules:
            Settings()["Sequent Rules"][r] = preset[r]


def _load_preset(preset_name: str) -> dict:
    with open(
        os.path.join(_preset_path, f"{preset_name}.json")
    ) as file:
        return json.load(file)


def _rules():
    """Generates strings corresponding to the rules in Settings()."""
    for side in _sides:
        for connective in _connectives:
            yield side+connective

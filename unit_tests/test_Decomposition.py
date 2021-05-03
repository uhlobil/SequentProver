import json
import os
import unittest

from Controllers import ImportExport

_current_path = os.path.dirname(__file__)
_names_path = os.path.join(_current_path, "..", "SequentProver", "data", "Names.json")


class TestDecomposingWithEmptyNames(unittest.TestCase):
    def setUp(self) -> None:
        with open(_names_path, "r") as name_file:
            self.old_names = json.load(name_file)
        with open(_names_path, "w") as name_file:
            name_file.write("[]")

    def test_decomposing_sequents_with_empty_names_file_raises_value_error(self):
        with self.assertRaises(ValueError):
            ImportExport.decompose_sequents()

    def tearDown(self) -> None:
        with open(_names_path, "w") as name_file:
            name_file.write(json.dumps(self.old_names, indent=4))


if __name__ == '__main__':
    unittest.main()

import unittest

from Propositions.Converters import String
from Propositions.Propositions import Atom, Negation, Conditional, Conjunction, Disjunction


class TestAtoms(unittest.TestCase):
    prop = Atom("Predicate", ("alpha", "beta", "gamma"))

    def test_atom_init(self):
        atom = self.prop
        self.assertEqual(atom.names, ("alpha", "beta", "gamma"))
        self.assertEqual("Predicate(alpha; beta; gamma)", str(atom))

    def test_atom_from_string(self):
        string = "Predicate(alpha; beta; gamma)"
        prop = String(string).to_proposition()
        self.assertEqual(self.prop, prop)


class TestUnary(unittest.TestCase):
    types = Negation,
    atom = Atom("Predicate", ("alpha", "beta"))

    def test_unary_init(self):
        for t in self.types:
            prop = t(self.atom)
            self.assertEqual(self.atom, prop.prop)
            self.assertEqual(f"({prop.string} Predicate(alpha; beta))", str(prop))
            self.assertEqual(("alpha", "beta"), prop.names)

    def test_unary_from_string(self):
        for t in self.types:
            string = f"({t.string} Predicate(alpha; beta))"
            prop = String(string).to_proposition()
            self.assertEqual(self.atom, prop.prop)
            self.assertEqual(string, str(prop))
            self.assertEqual(("alpha", "beta"), prop.names)


class TestBinary(unittest.TestCase):
    types = Conditional, Conjunction, Disjunction
    left = Atom("Predicate", ("alpha", "beta"))
    right = Atom("Predicate", ("beta", "gamma"))

    def test_binary_init(self):
        for t in self.types:
            prop = t(self.left, self.right)
            self.assertEqual(self.left, prop.left)
            self.assertEqual(self.right, prop.right)
            self.assertEqual(("alpha", "beta", "gamma"), prop.names)

    def test_binary_from_string(self):
        for t in self.types:
            string = f"(Predicate(alpha; beta) {t.string} Predicate(beta; gamma))"
            prop = String(string).to_proposition()
            self.assertEqual(self.left, prop.left)
            self.assertEqual(self.right, prop.right)
            self.assertEqual(string, str(prop))
            self.assertEqual(("alpha", "beta", "gamma"), prop.names)


if __name__ == '__main__':
    unittest.main()

import unittest

from Propositions.Converters import String
from Propositions.Propositions import Negation, Conditional, Conjunction, Disjunction, Universal, Existential
from Propositions.BaseClasses import Atom


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


class TestQuantifiers(unittest.TestCase):
    types = Universal, Existential
    test_atom = Atom("Predicate", ("alpha", "x", "beta"))
    result_atom = Atom("Predicate", ("alpha", "testname", "beta"))
    unary = Negation,
    binary = Conditional, Conjunction, Disjunction

    def test_universal_init(self):
        universal = Universal("x", self.test_atom)
        self.assertEqual("x", universal.var)
        self.assertEqual(self.test_atom, universal.prop)

    def test_existential_init(self):
        existential = Existential("x", self.test_atom)
        self.assertEqual("x", existential.var)
        self.assertEqual(self.test_atom, existential.prop)

    def test_instantiate_atom(self):
        universal = Universal("x", self.test_atom)
        test = universal.instantiate(universal.var, "testname")
        self.assertEqual(self.result_atom, test)

    def test_instantiate_unary(self):
        for c in self.unary:
            universal = Universal("x", c(self.test_atom))
            test = universal.instantiate(universal.var, "testname")
            self.assertEqual(c(self.result_atom), test)

    def test_instantiate_binary(self):
        for c in self.binary:
            universal = Universal("x", c(self.test_atom, self.test_atom))
            test = universal.instantiate(universal.var, "testname")
            self.assertEqual(c(self.result_atom, self.result_atom), test)


if __name__ == '__main__':
    unittest.main()

import unittest

from Adapters.Converters import String
from Objects.Propositions.Propositions import Formula, Universal


class TestFormula(unittest.TestCase):
    unary = Formula("Property", ["a"])
    binary = Formula("Relation", ["a", "b"])

    def test_unary_formula_init(self):
        self.assertEqual(str(self.unary), "Property(a)")
        self.assertEqual(self.unary.__repr__(), "Form(Property, ['a'])")

    def test_binary_formula_init(self):
        self.assertEqual(str(self.binary), "Relation(a, b)")
        self.assertEqual(self.binary.__repr__(), "Form(Relation, ['a', 'b'])")

    def test_convert_string_to_unary_formula(self):
        s = "Property(a)"
        converted = String(s).to_proposition()
        self.assertEqual(converted, self.unary)

    def test_convert_string_to_binary_formula(self):
        s = "Relation(a, b)"
        converted = String(s).to_proposition()
        self.assertEqual(converted, self.binary)


class TestUniversals(unittest.TestCase):
    def test_universal_init(self):
        u = Universal("x", Formula("Property", ["x"]))
        self.assertEqual(u.symbol, "_A")
        self.assertEqual(u.string, "forall")
        self.assertEqual(u.variable, "x")
        self.assertEqual(u.prop, "Property")


if __name__ == '__main__':
    unittest.main()

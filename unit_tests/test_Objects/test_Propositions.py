import unittest

from Propositions.Converters import String
from Propositions.Propositions import Negation, Conditional, Conjunction, \
    Disjunction, Universal, Existential
from Propositions.BaseClasses import Atom


class TestConvert(unittest.TestCase):
    def test_converting_sequent_to_proposition_raises_value_error(self):
        with self.assertRaises(ValueError):
            String("a |~ b").to_proposition()

    def test_converting_proposition_to_sequent_raises_value_error(self):
        with self.assertRaises(ValueError):
            String("A implies B").to_sequent()


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
    result_atom = Atom("Predicate", ("alpha", "nothing", "beta"))
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
        test = universal.instantiate(universal.var, "nothing")
        self.assertEqual(self.result_atom, test)

    def test_instantiate_unary(self):
        for c in self.unary:
            universal = Universal("x", c(self.test_atom))
            test = universal.instantiate(universal.var, "nothing")
            self.assertEqual(c(self.result_atom), test)

    def test_instantiate_binary(self):
        for c in self.binary:
            universal = Universal("x", c(self.test_atom, self.test_atom))
            test = universal.instantiate(universal.var, "nothing")
            self.assertEqual(c(self.result_atom, self.result_atom), test)

    def test_existential_predicate_from_string(self):
        e = "(exists(x)(LikesFudge(x)))"
        convert = String(e).to_proposition()
        self.assertEqual(Existential("x", Atom("LikesFudge", ("x",))), convert)

    def test_universal_predicate_from_string(self):
        u = "(forall(y)(EatsDoughnuts(y)))"
        convert = String(u).to_proposition()
        self.assertEqual(Universal("y", Atom("EatsDoughnuts", ("y",))), convert)

    def test_complex_existential_from_string(self):
        e = "(exists(x)(Cute(x) and Cat(x)))"
        convert = String(e).to_proposition()
        self.assertEqual(
            Existential("x",
                        Conjunction(
                            Atom("Cute", ("x",)),
                            Atom("Cat", ("x",)))),
            convert)

    def test_quantifier_eq_with_same_predicate_different_names(self):
        a = Existential("x", Atom("Simple", ("x",)))
        b = Existential("y", Atom("Simple", ("y",)))
        self.assertEqual(a, b)

    def test_complex_quantifier_eq_same_object_predicate_different_names(self):
        a = Universal("x", Conjunction(Atom("Tough", ("x",)), Atom("Hard", ("x",))))
        b = Universal("y", Conjunction(Atom("Tough", ("y",)), Atom("Hard", ("y",))))
        self.assertEqual(a, b)

    def test_complex_quantifier_eq_same_object_multi_predicate(self):
        a = Universal("x", Conjunction(Atom("Tough", ("x", "x")), Atom("Hard", ("x", "x"))))
        b = Universal("y", Conjunction(Atom("Tough", ("y", "y")), Atom("Hard", ("y", "y"))))
        self.assertEqual(a, b)

    def test_nested_atomic_quantifier_init(self):
        nest = Universal("x", Existential("y", Atom("Nested", ("x", "y"))))
        self.assertEqual(Existential("y", Atom("Nested", ("x", "y"))), nest.prop)
        self.assertEqual("x", nest.var)
        self.assertEqual([], nest.names)
        self.assertEqual(Atom("Nested", ("x", "y")), nest.prop.prop)

    def test_nested_complex_quantifier_init(self):
        nest = Universal("x",
                         Existential("y",
                                     Conjunction(
                                         Atom("Nested", ("x",)),
                                         Atom("Nested", ("y",))))
                         )
        self.assertEqual(
            Existential("y",
                        Conjunction(
                            Atom("Nested", ("x",)),
                            Atom("Nested", ("y",)))),
            nest.prop
        )
        self.assertEqual("x", nest.var)
        self.assertEqual([], nest.names)
        self.assertEqual(
            Conjunction(
                Atom("Nested", ("x",)),
                Atom("Nested", ("y",))),
            nest.prop.prop
        )
        self.assertEqual("y", nest.prop.var)

    def test_nested_two_name_atomic_quantifier(self):
        nest = Universal("w", Existential("x", Atom("Nested", ("x", "w"))))
        self.assertEqual(Existential("x", Atom("Nested", ("x", "w"))), nest.prop)
        self.assertEqual(Atom("Nested", ("x", "w")), nest.prop.prop)

    def test_nested_two_name_complex_quantifier(self):
        nest = Universal("w",
                         Existential("x",
                                     Disjunction(
                                         Atom("Nested", ("x", "w")),
                                         Atom("Nested", ("w", "x"))))
                         )
        self.assertEqual(
            Existential("x",
                        Disjunction(
                            Atom("Nested", ("x", "w")),
                            Atom("Nested", ("w", "x")))),
            nest.prop
        )
        self.assertEqual(
            Disjunction(
                Atom("Nested", ("x", "w")),
                Atom("Nested", ("w", "x"))),
            nest.prop.prop)

    def test_nested_instantiated(self):
        uni = Universal("x", Existential("y", Atom("Nested", ("x", "y"))))
        inst = uni.instantiate("x", "alpha")
        self.assertEqual(Existential("y", Atom("Nested", ("alpha", "y"))), inst)

    def test_quantifier_namespace_saturation(self):
        a = Universal("x", Atom("Saturated", ("x", "NAME", "NAME")))
        b = Universal("x", Atom("Saturated", ("x", "x", "NAME")))
        self.assertNotEqual(a, b)
        c = Existential("a", Universal("b", Atom("Saturated", ("a", "b", "b"))))
        d = Existential("a", Universal("b", Atom("Saturated", ("a", "a", "b"))))
        self.assertNotEqual(c, d)

    def test_nested_quantifier_string(self):
        expected = "forall(x)(exists(y)(Nested(x; y)))"
        actual = str(Universal("x", Existential("y", Atom("Nested", ("x", "y")))))
        self.assertEqual(expected, actual)

    def test_nested_quantifier_from_string(self):
        string = "(forall(x)(exists(y)(Nested(x; y))))"
        actual = String(string).to_proposition()
        expected = Universal("x", Existential("y", Atom("Nested", ("x", "y"))))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

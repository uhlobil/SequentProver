import unittest
from unittest.mock import patch

from Controllers import Rules
from Controllers.Settings import Settings
from Objects.Sequents import Sequent
from Propositions.Converters import String
from Propositions.Decomposables import LeftUniversal
from Propositions.Propositions import Conjunction, Conditional, Disjunction, Negation, Universal
from Propositions.BaseClasses import Atom


class TestSequent(unittest.TestCase):

    def test_string_to_sequent(self):
        string = "Predicate(alpha), (Relation(alpha; beta) and Relation(beta; delta)) " \
                 "|~ (Relation(beta; gamma) implies Predicate(delta)), Predicate(delta) or Predicate(zeta)"
        sequent = String(string).to_sequent()
        self.assertEqual(
            Sequent(
                [
                    Atom("Predicate", ("alpha",)),
                    Conjunction(
                        Atom("Relation", ("alpha", "beta")),
                        Atom("Relation", ("beta", "delta"))
                    )
                ],
                [
                    Conditional(
                        Atom("Relation", ("beta", "gamma")),
                        Atom("Predicate", ("delta",))
                    ),
                    Disjunction(
                        Atom("Predicate", ("delta",)),
                        Atom("Predicate", ("zeta",))
                    )
                ]
            ),
            sequent
        )

    def test_sequent_left_universal_principal(self):
        universal = Universal("x", Atom("Proposition", ("x",)))
        sequent = Sequent([universal], [])
        principal = sequent.principal
        self.assertEqual("ant", principal.side)
        self.assertEqual(0, principal.index)
        self.assertEqual(LeftUniversal("x", Atom("Proposition", ("x",))), principal.proposition)

    def test_sequent_right_universal_principal(self):
        self.assertTrue(False)


class TestInvertibleDecomp(unittest.TestCase):
    rules = {k: v for k, v in Settings()["Sequent Rules"].items()}
    alpha = Atom("Predicate", ("alpha",))
    beta = Atom("Predicate", ("beta",))

    def setUp(self) -> None:
        Rules.change_multiple("", "Invertible")

    def tearDown(self) -> None:
        for k, v in self.rules.items():
            Settings()["Sequent Rules"][k] = v

    def test_inv_left_conditional(self):
        """Predicate(alpha) implies Predicate(beta) |~ """

        sequent = Sequent([Conditional(self.alpha, self.beta)], [])
        decomp = sequent.decompose()[0]
        self.assertEqual(Sequent([], [self.alpha]), decomp[0])
        self.assertEqual(Sequent([self.beta], []), decomp[1])

    def test_inv_right_conditional(self):
        """|~ Predicate(alpha) implies Predicate(beta)"""

        sequent = Sequent([], [Conditional(self.alpha, self.beta)])
        decomp = sequent.decompose()[0][0]
        self.assertEqual(Sequent([self.alpha], [self.beta]), decomp)

    def test_inv_left_conjunction(self):
        """Predicate(alpha) and Predicate(beta) |~"""

        sequent = Sequent([Conjunction(self.alpha, self.beta)], [])
        decomp = sequent.decompose()[0][0]
        self.assertEqual(Sequent([self.alpha, self.beta], []), decomp)

    def test_inv_right_conjunction(self):
        """|~ Predicate(alpha) and Predicate(beta)"""

        sequent = Sequent([], [Conjunction(self.alpha, self.beta)])
        decomp = sequent.decompose()[0]
        self.assertEqual(Sequent([], [self.alpha]), decomp[0])
        self.assertEqual(Sequent([], [self.beta]), decomp[1])

    def test_inv_left_disjunction(self):
        """Predicate(alpha) or Predicate(beta) |~"""

        sequent = Sequent([Disjunction(self.alpha, self.beta)], [])
        decomp = sequent.decompose()[0]
        self.assertEqual(Sequent([self.alpha], []), decomp[0])
        self.assertEqual(Sequent([self.beta], []), decomp[1])

    def test_inv_right_disjunction(self):
        """|~ Predicate(alpha) or Predicate(beta)"""

        sequent = Sequent([], [Disjunction(self.alpha, self.beta)])
        decomp = sequent.decompose()[0][0]
        self.assertEqual(Sequent([], [self.alpha, self.beta]), decomp)

    def test_inv_left_negation(self):
        """not Predicate(alpha) |~"""

        sequent = Sequent([Negation(self.alpha)], [])
        decomp = sequent.decompose()[0][0]
        self.assertEqual(Sequent([], [self.alpha]), decomp)

    def test_inv_right_negation(self):
        """|~ not Predicate(alpha)"""

        sequent = Sequent([], [Negation(self.alpha)])
        decomp = sequent.decompose()[0][0]
        self.assertEqual(Sequent([self.alpha], []), decomp)

    def test_inv_left_universal(self):
        """forall(x)(Predicate(x))"""

        with patch("builtins.input", lambda *args: 1):
            sequent = Sequent([Universal("alpha", self.alpha)], [])
            decomp = sequent.decompose()[0][0]
            self.assertEqual(Sequent([Atom("Predicate", ("Adrian",))], []), decomp)


if __name__ == '__main__':
    unittest.main()

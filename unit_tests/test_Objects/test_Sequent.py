import unittest

from Controllers import Rules
from Controllers.Settings import Settings
from Objects.Sequents import Sequent
from Propositions.Converters import String
from Propositions.Propositions import Atom, Conjunction, Conditional, Disjunction, Negation


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


if __name__ == '__main__':
    unittest.main()

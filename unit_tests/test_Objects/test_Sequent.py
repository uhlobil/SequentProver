import unittest

from SequentProver.Objects.Propositions import Conditional
from SequentProver.Objects.Propositions import Conjunction
from SequentProver.Objects.Propositions import Disjunction
from SequentProver.Objects.Propositions import Atom
from SequentProver.Objects.Propositions import Negation
from Objects.Sequents import Sequent


class TestSequent(unittest.TestCase):
    atom_prop = Atom('Prop')
    neg_prop = Negation(atom_prop)
    cond_prop = Conditional(atom_prop, atom_prop)
    conj_prop = Conjunction(atom_prop, atom_prop)
    disj_prop = Disjunction(atom_prop, atom_prop)
    test_atom_seq = Sequent([atom_prop], [atom_prop])

    def test_init(self):
        self.assertIsInstance(self.test_atom_seq, Sequent)

    def test_repr(self):
        test_repr = self.test_atom_seq.__repr__()
        expected = 'Sequent([Atom(Prop)], [Atom(Prop)])'
        self.assertEqual(test_repr, expected)

    def test_str(self):
        test_str = self.test_atom_seq.__str__()
        expected = 'Prop |~ Prop'
        self.assertEqual(test_str, expected)

    def test_complexity(self):
        test_seqs = [
            self.test_atom_seq,
            Sequent([self.neg_prop, self.cond_prop], [self.disj_prop, self.atom_prop])
        ]
        expected = [0, 3]
        for i, sequent in enumerate(test_seqs):
            self.assertEqual(sequent.complexity, expected[i])

    def test_is_reflexive(self):
        self.assertTrue(self.test_atom_seq.is_reflexive)
        self.assertFalse(Sequent([self.neg_prop, self.cond_prop], [self.disj_prop, self.atom_prop]).is_reflexive)


if __name__ == '__main__':
    unittest.main()

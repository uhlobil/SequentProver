import unittest

from Controllers.Rules import change_multiple
from Objects.Sequents import Sequent
from Objects.Trees import Tree
from View.DisplayTrees import Key
from unit_tests.mocks import Objects as mock


class TestInvertibleDecomp(unittest.TestCase):

    def setUp(self) -> None:
        change_multiple(rule="", mode="Invertible")

    def test_one_parent_sequents_invertible_decompose(self):
        sequent = mock.reflexive_negation_sequent
        result = sequent.decompose()[0]
        self.assertEqual(Sequent([], [mock.atom, mock.negation]), result[0])

    def test_two_parent_sequents_invertible_decompose(self):
        sequent = mock.left_disjunction_sequent
        result = sequent.decompose()[0]
        result_pair = result
        left_parent = result_pair[0]
        right_parent = result_pair[1]
        self.assertEqual(Sequent([mock.atom], []), left_parent)
        self.assertEqual(Sequent([mock.atom], []), right_parent)

    def test_invertible_one_parent_decomp(self):
        test_tree = Tree(mock.right_disjunction_sequent)
        test_tree.populate()
        self.assertEqual(Sequent([], [mock.atom, mock.atom]), test_tree['0000000M'])

    def test_invertible_two_parent_decomp(self):
        test_tree = Tree(mock.left_conditional_sequent)
        test_tree.populate()
        self.assertEqual(Sequent([], [mock.atom]), test_tree['0000000L'])
        self.assertEqual(Sequent([mock.atom], []), test_tree['0000000R'])


class TestNonInvertibleDecomp(unittest.TestCase):
    def setUp(self) -> None:
        change_multiple(rule="", mode="NonInvertible")

    def test_one_parent_sequents_non_invertible_decompose(self):
        sequent = mock.right_conditional_sequent
        result = sequent.decompose()
        self.assertEqual(Sequent([mock.atom], []), result[0][0])
        self.assertEqual(Sequent([], [mock.atom]), result[1][0])
        self.assertEqual(Sequent([mock.atom], [mock.atom]), result[2][0])

    def test_two_parent_sequents_non_invertible_decompose(self):
        sequent = mock.reflexive_disjunction_sequent
        result = sequent.decompose()
        x_result = result[0]
        x_left = x_result[0]
        x_right = x_result[1]
        y_result = result[1]
        y_left = y_result[0]
        y_right = y_result[1]
        self.assertEqual(Sequent([mock.atom], [mock.disjunction]), x_left)
        self.assertEqual(Sequent([mock.atom], []), x_right)
        self.assertEqual(Sequent([mock.atom], []), y_left)
        self.assertEqual(Sequent([mock.atom], [mock.disjunction]), y_right)

    def test_non_invertible_one_parent_decomp(self):
        test_tree = Tree(mock.left_conjunction_sequent)
        test_tree.populate()
        self.assertEqual(Sequent([mock.atom], []), test_tree['0000aaaM'])
        self.assertEqual(Sequent([mock.atom], []), test_tree['0000aabM'])
        self.assertEqual(Sequent([mock.atom, mock.atom], []), test_tree['0000aacM'])

    def test_non_invertible_two_parent_decomp(self):
        test_tree = Tree(Sequent([mock.atom], [mock.conjunction]))
        test_tree.populate()
        self.assertEqual(Sequent([mock.atom], [mock.atom]), test_tree['0000aaaL'])
        self.assertEqual(Sequent([], [mock.atom]), test_tree['0000aaaR'])
        self.assertEqual(Sequent([], [mock.atom]), test_tree['0000aabL'])
        self.assertEqual(Sequent([mock.atom], [mock.atom]), test_tree['0000aabR'])


class TestKeys(unittest.TestCase):

    def test_key_attributes(self):
        test_key = Key('0000aaaM000LeveR')
        self.assertEqual(['0000', 'aaaM', '000L', 'eveR'], test_key.locations)
        self.assertEqual(Key('0000aaaM000LeveL'), test_key.partner)
        self.assertEqual('R', test_key.last)
        self.assertEqual('eve', test_key.cognate_space)
        self.assertEqual('eveR', test_key.last_four)


if __name__ == '__main__':
    unittest.main()

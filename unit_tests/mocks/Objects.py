import os
import json
from Objects.Sequents import Sequent

# Propositions
from Propositions.BaseClasses import Atom
from Propositions.Propositions import Negation, Conditional, Conjunction, Disjunction

atom = Atom('Proposition')
negation = Negation(atom)
conditional = Conditional(atom, atom)
conjunction = Conjunction(atom, atom)
disjunction = Disjunction(atom, atom)

propositions_list = [
    atom, negation, conditional, conjunction, disjunction
]

# Proposition Strings
atom_str = 'Proposition'
neg_str = '(not Proposition)'
cond_str = '(Proposition implies Proposition)'
conj_str = '(Proposition and Proposition)'
disj_str = '(Proposition or Proposition)'

proposition_strings_list = [
    atom_str, neg_str, cond_str, conj_str, disj_str
]

# Reflexive Sequents
# Note: do not attempt to decompose universal sequents non-invertibly.
empty_sequent = Sequent([], [])
reflexive_atomic_sequent = Sequent([atom], [atom])
reflexive_negation_sequent = Sequent([negation], [negation])
reflexive_conditional_sequent = Sequent([conditional], [conditional])
reflexive_conjunction_sequent = Sequent([conjunction], [conjunction])
reflexive_disjunction_sequent = Sequent([disjunction], [disjunction])
reflexive_universal_sequent = Sequent(propositions_list, propositions_list)

reflexive_sequents_list = [
    empty_sequent, reflexive_atomic_sequent,
    reflexive_negation_sequent, reflexive_conditional_sequent,
    reflexive_conjunction_sequent, reflexive_disjunction_sequent,
    reflexive_universal_sequent
]

# Reflexive Sequent Strings
ref_empty_sequent_str = ' |~ '
ref_atomic_sequent_str = 'Proposition |~ Proposition'
ref_negation_sequent_str = '(not Proposition) |~ (not Proposition)'
ref_conditional_sequent_str = \
    '(Proposition implies Proposition) |~ (Proposition implies Proposition)'
ref_conjunction_sequent_str = \
    '(Proposition and Proposition) |~ (Proposition and Proposition)'
ref_disjunction_sequent_str = \
    '(Proposition or Proposition) |~ (Proposition or Proposition)'
ref_universal_sequent_str = \
    'Proposition, (not Proposition), (Proposition implies Proposition), ' \
    '(Proposition and Proposition), (Proposition or Proposition) |~ ' \
    'Proposition, (not Proposition), (Proposition implies Proposition), ' \
    '(Proposition and Proposition), (Proposition or Proposition)'

ref_sequent_strings = \
    [ref_empty_sequent_str, ref_atomic_sequent_str, ref_negation_sequent_str,
     ref_conditional_sequent_str, ref_conjunction_sequent_str,
     ref_disjunction_sequent_str, ref_universal_sequent_str]

# One-Sided Sequents
left_atomic_sequent = Sequent([atom], [])
right_atomic_sequent = Sequent([], [atom])
left_negation_sequent = Sequent([negation], [])
right_negation_sequent = Sequent([], [negation])
left_conditional_sequent = Sequent([conditional], [])
right_conditional_sequent = Sequent([], [conditional])
left_conjunction_sequent = Sequent([conjunction], [])
right_conjunction_sequent = Sequent([], [conjunction])
left_disjunction_sequent = Sequent([disjunction], [])
right_disjunction_sequent = Sequent([], [disjunction])
left_universal_sequent = Sequent(propositions_list, [])
right_universal_sequent = Sequent([], propositions_list)

one_sided_sequents_list = [
    left_atomic_sequent, right_atomic_sequent,
    left_negation_sequent, right_negation_sequent,
    left_conditional_sequent, right_conditional_sequent,
    left_conjunction_sequent, right_conjunction_sequent,
    left_disjunction_sequent, right_disjunction_sequent,
    left_universal_sequent, right_universal_sequent
]

# One-Sided Sequent Strings
left_atomic_sequent_str = 'Proposition |~ '
right_atomic_sequent_str = ' |~ Proposition'
left_negation_sequent_str = '(not Proposition) |~ '
right_negation_sequent_str = ' |~ (not Proposition)'
left_conditional_sequent_str = '(Proposition implies Proposition) |~ '
right_conditional_sequent_str = ' |~ (Proposition implies Proposition)'
left_conjunction_sequent_str = '(Proposition and Proposition) |~ '
right_conjunction_sequent_str = ' |~ (Proposition and Proposition)'
left_disjunction_sequent_str = '(Proposition or Proposition) |~ '
right_disjunction_sequent_str = ' |~ (Proposition or Proposition)'
left_universal_sequent_str = \
    'Proposition, (not Proposition), (Proposition implies Proposition), ' \
    '(Proposition and Proposition), (Proposition or Proposition) |~ '
right_universal_sequent_str = \
    ' |~ Proposition, (not Proposition), (Proposition implies Proposition), ' \
    '(Proposition and Proposition), (Proposition or Proposition)'

nr_sequent_strings = [
    left_atomic_sequent_str, right_atomic_sequent_str,
    left_negation_sequent_str, right_negation_sequent_str,
    left_conditional_sequent_str, right_conditional_sequent_str,
    left_conjunction_sequent_str, right_conjunction_sequent_str,
    left_disjunction_sequent_str, right_disjunction_sequent_str,
    left_universal_sequent_str, right_universal_sequent_str
]

# Collections
all_sequents = reflexive_sequents_list + one_sided_sequents_list
all_sequent_strings = ref_sequent_strings + nr_sequent_strings


# Trees_backup
def load_tree(filename) -> dict:
    """Returns the tree in filename as a dict."""
    with open(os.path.join('env', 'unit_tests', 'mocks', 'Trees', f'{filename}.json'), 'r') as file:
        return json.load(file)

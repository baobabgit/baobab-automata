"""
Tests unitaires pour la classe TM.

Ce module contient tous les tests unitaires pour la classe TM
et ses composants associés.
"""

import unittest
from typing import Dict, Set, Tuple

from baobab_automata.turing.tm import TM
from baobab_automata.turing.tm_configuration import TMConfiguration
from baobab_automata.interfaces.turing_machine import TapeDirection
from baobab_automata.exceptions.tm_exceptions import (
    TMError,
    InvalidTMError,
    InvalidStateError,
    TMSimulationError,
)


class TestTMConfiguration(unittest.TestCase):
    """Tests pour la classe TMConfiguration."""

    def test_tm_configuration_creation(self):
        """Test de création d'une configuration valide."""
        config = TMConfiguration("q0", "aabb", 2, 5)

        self.assertEqual(config.state, "q0")
        self.assertEqual(config.tape, "aabb")
        self.assertEqual(config.head_position, 2)
        self.assertEqual(config.step_count, 5)

    def test_tm_configuration_negative_head_position(self):
        """Test de validation avec position de tête négative."""
        with self.assertRaises(ValueError):
            TMConfiguration("q0", "aabb", -1, 5)

    def test_tm_configuration_negative_step_count(self):
        """Test de validation avec nombre d'étapes négatif."""
        with self.assertRaises(ValueError):
            TMConfiguration("q0", "aabb", 2, -1)

    def test_tm_configuration_str(self):
        """Test de la représentation textuelle."""
        config = TMConfiguration("q0", "aabb", 2, 5)
        expected = "(q0, aabb, 2, 5)"
        self.assertEqual(str(config), expected)

    def test_tm_configuration_repr(self):
        """Test de la représentation technique."""
        config = TMConfiguration("q0", "aabb", 2, 5)
        expected = (
            "TMConfiguration(state='q0', tape='aabb', head_position=2, step_count=5)"
        )
        self.assertEqual(repr(config), expected)


class TestTM(unittest.TestCase):
    """Tests pour la classe TM."""

    def test_tm_construction_valid(self):
        """Test de construction d'une TM valide."""
        tm = TM(
            states={"q0", "q1", "q_accept", "q_reject"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q0", "B"): ("q_reject", "B", TapeDirection.STAY),
                ("q1", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q1", "B"): ("q_accept", "B", TapeDirection.STAY),
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
        )

        self.assertIn("q0", tm.states)
        self.assertIn("a", tm.alphabet)
        self.assertEqual(tm.initial_state, "q0")
        self.assertEqual(tm.validate(), [])

    def test_tm_construction_empty_states(self):
        """Test de construction avec états vides."""
        with self.assertRaises(ValueError):
            TM(
                states=set(),
                alphabet={"a"},
                tape_alphabet={"a", "B"},
                transitions={},
                initial_state="q0",
                accept_states=set(),
                reject_states=set(),
            )

    def test_tm_construction_empty_alphabet(self):
        """Test de construction avec alphabet vide."""
        with self.assertRaises(ValueError):
            TM(
                states={"q0"},
                alphabet=set(),
                tape_alphabet={"B"},
                transitions={},
                initial_state="q0",
                accept_states=set(),
                reject_states=set(),
            )

    def test_tm_construction_invalid_initial_state(self):
        """Test de construction avec état initial invalide."""
        with self.assertRaises(ValueError):
            TM(
                states={"q0", "q1"},
                alphabet={"a"},
                tape_alphabet={"a", "B"},
                transitions={},
                initial_state="q2",  # État inexistant
                accept_states={"q1"},
                reject_states=set(),
            )

    def test_tm_construction_blank_symbol_not_in_tape_alphabet(self):
        """Test de construction avec symbole blanc non dans l'alphabet de bande."""
        with self.assertRaises(ValueError):
            TM(
                states={"q0"},
                alphabet={"a"},
                tape_alphabet={"a"},
                transitions={},
                initial_state="q0",
                accept_states=set(),
                reject_states=set(),
                blank_symbol="B",  # B n'est pas dans {"a"}
            )

    def test_tm_construction_overlapping_accept_reject_states(self):
        """Test de construction avec états d'acceptation et de rejet qui se chevauchent."""
        with self.assertRaises(ValueError):
            TM(
                states={"q0", "q1"},
                alphabet={"a"},
                tape_alphabet={"a", "B"},
                transitions={},
                initial_state="q0",
                accept_states={"q1"},
                reject_states={"q1"},  # Chevauchement
            )

    def test_tm_simulation_accept(self):
        """Test de simulation avec acceptation."""
        tm = self._create_even_length_tm()

        accepted, trace = tm.simulate("aa")
        self.assertTrue(accepted)
        self.assertGreater(len(trace), 0)
        self.assertIn(trace[-1]["state"], tm.accept_states)

    def test_tm_simulation_reject(self):
        """Test de simulation avec rejet."""
        tm = self._create_even_length_tm()

        accepted, trace = tm.simulate("a")
        self.assertFalse(accepted)
        self.assertGreater(len(trace), 0)
        self.assertIn(trace[-1]["state"], tm.reject_states)

    def test_tm_simulation_timeout(self):
        """Test de simulation avec timeout."""
        tm = self._create_infinite_loop_tm()

        accepted, trace = tm.simulate("a", max_steps=5)
        self.assertFalse(accepted)
        self.assertEqual(len(trace), 2)  # 1 étape + configuration initiale

    def test_tm_step_execution(self):
        """Test d'exécution pas-à-pas."""
        tm = self._create_simple_tm()

        # Premier pas
        transition = tm.step("q0", "a")
        self.assertIsNotNone(transition)
        new_state, write_symbol, direction = transition
        self.assertEqual(new_state, "q1")
        self.assertEqual(write_symbol, "a")
        self.assertEqual(direction, TapeDirection.RIGHT)

    def test_tm_step_no_transition(self):
        """Test d'exécution pas-à-pas sans transition."""
        tm = self._create_simple_tm()

        transition = tm.step("q0", "B")
        self.assertIsNone(transition)

    def test_tm_step_invalid_state(self):
        """Test d'exécution pas-à-pas avec état invalide."""
        tm = self._create_simple_tm()

        with self.assertRaises(InvalidStateError):
            tm.step("q_invalid", "a")

    def test_tm_is_halting_state(self):
        """Test de vérification des états d'arrêt."""
        tm = self._create_simple_tm()

        self.assertTrue(tm.is_halting_state("q_accept"))
        self.assertFalse(tm.is_halting_state("q0"))
        self.assertFalse(tm.is_halting_state("q1"))

    def test_tm_validation_errors(self):
        """Test de validation avec erreurs."""
        # TM avec transition référençant un état inexistant
        with self.assertRaises(InvalidTMError):
            TM(
                states={"q0", "q1"},
                alphabet={"a"},
                tape_alphabet={"a", "B"},
                transitions={
                    ("q0", "a"): ("q2", "a", TapeDirection.RIGHT)  # q2 n'existe pas
                },
                initial_state="q0",
                accept_states={"q1"},
                reject_states=set(),
            )

    def test_tm_properties(self):
        """Test des propriétés de la TM."""
        tm = self._create_simple_tm()

        # Test que les propriétés retournent des copies
        states = tm.states
        states.add("q_new")
        self.assertNotIn("q_new", tm.states)

        alphabet = tm.alphabet
        alphabet.add("b")
        self.assertNotIn("b", tm.alphabet)

    def test_tm_to_dict(self):
        """Test de sérialisation en dictionnaire."""
        tm = self._create_simple_tm()
        data = tm.to_dict()

        self.assertEqual(data["type"], "TM")
        self.assertEqual(data["name"], tm.name)
        self.assertEqual(set(data["states"]), tm.states)
        self.assertEqual(set(data["alphabet"]), tm.alphabet)
        self.assertEqual(data["initial_state"], tm.initial_state)

    def test_tm_from_dict(self):
        """Test de désérialisation depuis un dictionnaire."""
        tm = self._create_simple_tm()
        data = tm.to_dict()

        tm_restored = TM.from_dict(data)

        self.assertEqual(tm.states, tm_restored.states)
        self.assertEqual(tm.alphabet, tm_restored.alphabet)
        self.assertEqual(tm.transitions, tm_restored.transitions)
        self.assertEqual(tm.initial_state, tm_restored.initial_state)

    def test_tm_from_dict_invalid(self):
        """Test de désérialisation avec données invalides."""
        invalid_data = {
            "type": "TM",
            "states": "invalid",
        }  # states devrait être une liste

        with self.assertRaises(InvalidTMError):
            TM.from_dict(invalid_data)

    def test_tm_str_repr(self):
        """Test des représentations textuelle et technique."""
        tm = self._create_simple_tm()

        str_repr = str(tm)
        self.assertIn("TM", str_repr)
        self.assertIn(tm.name, str_repr)

        repr_repr = repr(tm)
        self.assertIn("TM(", repr_repr)
        self.assertIn(tm.name, repr_repr)

    def test_tm_anbn_example(self):
        """Test avec l'exemple a^n b^n."""
        tm = self._create_anbn_tm()

        # Chaînes valides
        self.assertTrue(tm.simulate("ab")[0])
        self.assertTrue(tm.simulate("aabb")[0])
        self.assertTrue(tm.simulate("aaabbb")[0])

        # Chaînes invalides
        self.assertFalse(tm.simulate("a")[0])
        self.assertFalse(tm.simulate("b")[0])
        self.assertFalse(tm.simulate("aab")[0])
        self.assertFalse(tm.simulate("abb")[0])
        self.assertFalse(tm.simulate("ba")[0])

    def _create_simple_tm(self) -> TM:
        """Crée une TM simple pour les tests."""
        return TM(
            states={"q0", "q1", "q_accept"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q1", "B"): ("q_accept", "B", TapeDirection.STAY),
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states=set(),
        )

    def _create_even_length_tm(self) -> TM:
        """Crée une TM qui accepte les chaînes de longueur paire."""
        return TM(
            states={"q0", "q1", "q_accept", "q_reject"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q0", "B"): ("q_accept", "B", TapeDirection.STAY),  # Chaîne vide (longueur 0, paire)
                ("q1", "a"): ("q0", "a", TapeDirection.RIGHT),
                ("q1", "B"): ("q_reject", "B", TapeDirection.STAY),  # Longueur impaire
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
        )

    def _create_infinite_loop_tm(self) -> TM:
        """Crée une TM qui boucle infiniment."""
        return TM(
            states={"q0", "q_accept"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): ("q0", "a", TapeDirection.RIGHT),
                # Pas de transition pour B, donc la machine s'arrête
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states=set(),
        )

    def _create_anbn_tm(self) -> TM:
        """Crée une TM qui reconnaît le langage a^n b^n."""
        return TM(
            states={"q0", "q1", "q2", "q3", "q_accept", "q_reject"},
            alphabet={"a", "b"},
            tape_alphabet={"a", "b", "X", "Y", "B"},
            transitions={
                # Phase 1: Marquer les 'a' avec 'X'
                ("q0", "a"): ("q1", "X", TapeDirection.RIGHT),
                ("q0", "Y"): ("q3", "Y", TapeDirection.RIGHT),
                ("q0", "B"): ("q_reject", "B", TapeDirection.STAY),
                # Phase 2: Chercher le 'b' correspondant
                ("q1", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q1", "b"): ("q2", "Y", TapeDirection.LEFT),
                ("q1", "Y"): ("q1", "Y", TapeDirection.RIGHT),
                ("q1", "B"): ("q_reject", "B", TapeDirection.STAY),
                # Phase 3: Retourner au début
                ("q2", "a"): ("q2", "a", TapeDirection.LEFT),
                ("q2", "X"): ("q0", "X", TapeDirection.RIGHT),
                ("q2", "Y"): ("q2", "Y", TapeDirection.LEFT),
                ("q2", "B"): ("q_reject", "B", TapeDirection.STAY),
                # Phase 4: Vérifier que tous les symboles sont marqués
                ("q3", "Y"): ("q3", "Y", TapeDirection.RIGHT),
                ("q3", "B"): ("q_accept", "B", TapeDirection.STAY),
                ("q3", "a"): ("q_reject", "a", TapeDirection.STAY),
                ("q3", "b"): ("q_reject", "b", TapeDirection.STAY),
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
        )


if __name__ == "__main__":
    unittest.main()

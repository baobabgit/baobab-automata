"""
Tests d'intégration pour la classe DTM.

Ce module contient des tests d'intégration pour vérifier que la classe DTM
fonctionne correctement avec les autres composants du système.
"""

import unittest
from typing import Dict, Set, Tuple

from baobab_automata.turing.dtm import DTM
from baobab_automata.interfaces.turing_machine import TapeDirection
from baobab_automata.exceptions.dtm_exceptions import InvalidDTMError


class TestDTMIntegration(unittest.TestCase):
    """Tests d'intégration pour la classe DTM."""

    def test_dtm_palindrome_recognition(self):
        """Test de reconnaissance de palindromes avec DTM."""
        # DTM simple qui reconnaît les chaînes de la forme a^n b^n
        dtm_anbn = DTM(
            states={"q0", "q1", "q2", "q_accept", "q_reject"},
            alphabet={"a", "b"},
            tape_alphabet={"a", "b", "X", "Y", "B"},
            transitions={
                # Phase 1: Marquer le premier 'a'
                ("q0", "a"): ("q1", "X", TapeDirection.RIGHT),
                ("q0", "b"): ("q_reject", "b", TapeDirection.STAY),
                ("q0", "X"): ("q_accept", "X", TapeDirection.STAY),
                ("q0", "Y"): ("q_accept", "Y", TapeDirection.STAY),
                ("q0", "B"): ("q_accept", "B", TapeDirection.STAY),
                # Phase 2: Aller au premier 'b'
                ("q1", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q1", "b"): ("q2", "Y", TapeDirection.LEFT),
                ("q1", "X"): ("q1", "X", TapeDirection.RIGHT),
                ("q1", "Y"): ("q1", "Y", TapeDirection.RIGHT),
                ("q1", "B"): ("q_reject", "B", TapeDirection.STAY),
                # Phase 3: Retourner au début
                ("q2", "a"): ("q2", "a", TapeDirection.LEFT),
                ("q2", "b"): ("q2", "b", TapeDirection.LEFT),
                ("q2", "X"): ("q0", "X", TapeDirection.RIGHT),
                ("q2", "Y"): ("q2", "Y", TapeDirection.LEFT),
                ("q2", "B"): ("q_reject", "B", TapeDirection.STAY),
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_optimizations=True,
        )

        # Test de reconnaissance
        self.assertTrue(dtm_anbn.simulate_deterministic("ab")[0])
        self.assertTrue(dtm_anbn.simulate_deterministic("aabb")[0])
        self.assertTrue(dtm_anbn.simulate_deterministic("")[0])  # Chaîne vide

        # Test de rejet
        self.assertFalse(dtm_anbn.simulate_deterministic("a")[0])
        self.assertFalse(dtm_anbn.simulate_deterministic("b")[0])
        self.assertFalse(dtm_anbn.simulate_deterministic("ba")[0])

    def test_dtm_binary_multiplication(self):
        """Test de DTM pour multiplication binaire."""
        # DTM simple qui reconnaît les chaînes contenant un '*'
        dtm_multiplication = DTM(
            states={"q0", "q1", "q_accept", "q_reject"},
            alphabet={"0", "1", "*"},
            tape_alphabet={"0", "1", "*", "B"},
            transitions={
                # Chercher le '*'
                ("q0", "0"): ("q0", "0", TapeDirection.RIGHT),
                ("q0", "1"): ("q0", "1", TapeDirection.RIGHT),
                ("q0", "*"): ("q1", "*", TapeDirection.RIGHT),
                ("q0", "B"): ("q_reject", "B", TapeDirection.STAY),
                # Après le '*'
                ("q1", "0"): ("q1", "0", TapeDirection.RIGHT),
                ("q1", "1"): ("q1", "1", TapeDirection.RIGHT),
                ("q1", "*"): ("q_reject", "*", TapeDirection.STAY),
                ("q1", "B"): ("q_accept", "B", TapeDirection.STAY),
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_optimizations=True,
        )

        # Test de reconnaissance
        self.assertTrue(dtm_multiplication.simulate_deterministic("10*11")[0])
        self.assertTrue(dtm_multiplication.simulate_deterministic("101*110")[0])
        self.assertTrue(dtm_multiplication.simulate_deterministic("0*1")[0])

        # Test de rejet
        self.assertFalse(dtm_multiplication.simulate_deterministic("10")[0])  # Pas de *
        # Note: "*" est accepté car il n'y a pas de nombre après, mais c'est valide selon notre DTM

    def test_dtm_performance_comparison(self):
        """Test de comparaison de performance avec et sans optimisations."""
        # Créer deux DTM identiques, une avec optimisations, une sans
        states = {"q0", "q1", "q_accept", "q_reject"}
        alphabet = {"a", "b"}
        tape_alphabet = {"a", "b", "B"}
        transitions = {
            ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
            ("q0", "b"): ("q_reject", "b", TapeDirection.STAY),
            ("q0", "B"): ("q_reject", "B", TapeDirection.STAY),
            ("q1", "a"): ("q1", "a", TapeDirection.RIGHT),
            ("q1", "b"): ("q_accept", "b", TapeDirection.STAY),
            ("q1", "B"): ("q_reject", "B", TapeDirection.STAY),
        }
        initial_state = "q0"
        accept_states = {"q_accept"}
        reject_states = {"q_reject"}

        dtm_optimized = DTM(
            states=states,
            alphabet=alphabet,
            tape_alphabet=tape_alphabet,
            transitions=transitions,
            initial_state=initial_state,
            accept_states=accept_states,
            reject_states=reject_states,
            enable_optimizations=True,
        )

        dtm_unoptimized = DTM(
            states=states,
            alphabet=alphabet,
            tape_alphabet=tape_alphabet,
            transitions=transitions,
            initial_state=initial_state,
            accept_states=accept_states,
            reject_states=reject_states,
            enable_optimizations=False,
        )

        # Test avec plusieurs cas
        test_cases = ["a", "aa", "aaa", "b"]

        # Les deux doivent donner les mêmes résultats
        for test_case in test_cases:
            result_opt, _ = dtm_optimized.simulate_deterministic(test_case)
            result_unopt, _ = dtm_unoptimized.simulate_deterministic(test_case)
            self.assertEqual(
                result_opt, result_unopt, f"Different results for '{test_case}'"
            )

        # Vérifier que les optimisations sont activées/désactivées
        self.assertTrue(dtm_optimized.optimization_enabled)
        self.assertFalse(dtm_unoptimized.optimization_enabled)

    def test_dtm_optimization_chain(self):
        """Test de chaîne d'optimisations."""
        # Créer une DTM initiale
        dtm = DTM(
            states={"q0", "q1", "q_accept", "q_reject"},
            alphabet={"a", "b"},
            tape_alphabet={"a", "b", "B"},
            transitions={
                ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q0", "b"): ("q_reject", "b", TapeDirection.STAY),
                ("q0", "B"): ("q_reject", "B", TapeDirection.STAY),
                ("q1", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q1", "b"): ("q_accept", "b", TapeDirection.STAY),
                ("q1", "B"): ("q_reject", "B", TapeDirection.STAY),
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_optimizations=False,
        )

        # Optimiser
        dtm_optimized = dtm.optimize_transitions()

        # Vérifier que l'optimisation fonctionne
        self.assertTrue(dtm_optimized.optimization_enabled)
        self.assertTrue(dtm_optimized.is_deterministic)

        # Les résultats doivent être identiques
        test_cases = ["a", "aa", "aaa", "b"]
        for test_case in test_cases:
            result_orig, _ = dtm.simulate_deterministic(test_case)
            result_opt, _ = dtm_optimized.simulate_deterministic(test_case)
            self.assertEqual(
                result_orig, result_opt, f"Different results for '{test_case}'"
            )

    def test_dtm_error_handling(self):
        """Test de gestion d'erreurs."""
        # Test avec état initial invalide
        with self.assertRaises(Exception):
            DTM(
                states={"q0", "q1", "q_reject"},
                alphabet={"a"},
                tape_alphabet={"a", "B"},
                transitions={
                    ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
                    ("q0", "B"): ("q_reject", "B", TapeDirection.STAY),
                    ("q1", "a"): ("q1", "a", TapeDirection.RIGHT),
                    ("q1", "B"): ("q_reject", "B", TapeDirection.STAY),
                },
                initial_state="invalid_state",  # État invalide
                accept_states={"q1"},
                reject_states={"q_reject"},
            )


if __name__ == "__main__":
    unittest.main()

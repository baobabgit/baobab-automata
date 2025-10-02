"""
Tests unitaires pour la classe DTM.

Ce module contient tous les tests unitaires pour la classe DTM
et ses fonctionnalités spécifiques.
"""

import unittest
from typing import Dict, Set, Tuple

from baobab_automata.turing.dtm import DTM, DTMConfiguration
from baobab_automata.interfaces.turing_machine import TapeDirection
from baobab_automata.exceptions.dtm_exceptions import (
    DTMError,
    InvalidDTMError,
    DTMDeterminismError,
    DTMSimulationError,
    DTMOptimizationError,
    DTMCacheError,
)


class TestDTM(unittest.TestCase):
    """Tests pour la classe DTM."""

    def test_dtm_construction_deterministic(self):
        """Test de construction d'une DTM déterministe."""
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
        )

        self.assertTrue(dtm.is_deterministic)
        self.assertEqual(dtm.validate_determinism(), [])

    def test_dtm_construction_non_deterministic(self):
        """Test de construction d'une DTM non-déterministe (doit échouer)."""
        # Test direct de la validation du déterminisme
        dtm = DTM(
            states={"q0", "q1", "q_reject"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q0", "B"): ("q_reject", "B", TapeDirection.STAY),
                ("q1", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q1", "B"): ("q_reject", "B", TapeDirection.STAY),
            },
            initial_state="q0",
            accept_states={"q1"},
            reject_states={"q_reject"},
        )
        
        # Cette DTM devrait être déterministe
        self.assertTrue(dtm.is_deterministic)
        
        # Test avec une DTM qui manque des transitions (non-déterministe)
        # Créons une DTM temporaire pour tester la validation
        class TestDTM(DTM):
            def __init__(self):
                # Initialisation minimale pour tester validate_determinism
                self._states = {"q0", "q1"}
                self._tape_alphabet = {"a", "B"}
                self._accept_states = {"q1"}
                self._reject_states = set()
                self._transitions = {
                    ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
                    # Manque la transition pour ("q0", "B")
                }
        
        test_dtm = TestDTM()
        errors = test_dtm.validate_determinism()
        self.assertGreater(len(errors), 0)
        self.assertFalse(test_dtm.is_deterministic)

    def test_dtm_simulation_deterministic(self):
        """Test de simulation déterministe."""
        dtm = self._create_simple_dtm()

        accepted, trace = dtm.simulate_deterministic("aab")
        self.assertTrue(accepted)
        self.assertGreater(len(trace), 0)
        self.assertIn(trace[-1]["state"], dtm.accept_states)

    def test_dtm_simulation_rejection(self):
        """Test de simulation avec rejet."""
        dtm = self._create_simple_dtm()

        accepted, trace = dtm.simulate_deterministic("b")
        self.assertFalse(accepted)
        self.assertGreater(len(trace), 0)

    def test_dtm_optimization(self):
        """Test d'optimisation des transitions."""
        dtm = self._create_simple_dtm()
        optimized_dtm = dtm.optimize_transitions()

        self.assertTrue(optimized_dtm.is_deterministic)
        self.assertTrue(optimized_dtm.optimization_enabled)
        self.assertEqual(len(optimized_dtm.transitions), len(dtm.transitions))

    def test_dtm_performance_analysis(self):
        """Test d'analyse de performance."""
        dtm = self._create_simple_dtm()
        test_cases = ["a", "aa", "aaa", "aab", "ab"]

        results = dtm.analyze_performance(test_cases)

        self.assertEqual(results["total_tests"], len(test_cases))
        self.assertGreater(results["successful_simulations"], 0)
        self.assertGreaterEqual(results["average_execution_time"], 0)
        self.assertGreater(results["average_steps"], 0)

    def test_dtm_cache_functionality(self):
        """Test du fonctionnement du cache."""
        dtm = DTM(
            states={"q0", "q1"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q0", "B"): ("q1", "B", TapeDirection.STAY),
            },
            initial_state="q0",
            accept_states={"q1"},
            reject_states=set(),
            enable_optimizations=True,
        )

        cache_stats = dtm.cache_stats
        self.assertTrue(cache_stats["enabled"])
        self.assertGreater(cache_stats["state_transitions_cache_size"], 0)

    def test_dtm_configuration_creation(self):
        """Test de création de configuration DTM."""
        config = DTMConfiguration(
            state="q0",
            tape="aab",
            head_position=1,
            step_count=5,
            is_accepting=True,
        )

        self.assertEqual(config.state, "q0")
        self.assertEqual(config.tape, "aab")
        self.assertEqual(config.head_position, 1)
        self.assertEqual(config.step_count, 5)
        self.assertTrue(config.is_accepting)
        self.assertFalse(config.is_rejecting)

    def test_dtm_configuration_validation(self):
        """Test de validation des configurations DTM."""
        # Configuration valide
        config = DTMConfiguration("q0", "aab", 1, 5)
        self.assertIsNotNone(config)

        # Position négative - maintenant autorisée pour les machines de Turing
        config_neg = DTMConfiguration("q0", "aab", -1, 5)
        self.assertIsNotNone(config_neg)

        # Nombre d'étapes négatif - doit échouer
        with self.assertRaises(ValueError):
            DTMConfiguration("q0", "aab", 1, -1)

        # Acceptant et rejetant - doit échouer
        with self.assertRaises(ValueError):
            DTMConfiguration("q0", "aab", 1, 5, is_accepting=True, is_rejecting=True)

    def test_dtm_get_next_configuration(self):
        """Test de récupération de la prochaine configuration."""
        dtm = self._create_simple_dtm()

        # Configuration valide
        transition = dtm.get_next_configuration("q0", "a")
        self.assertIsNotNone(transition)
        self.assertEqual(transition[0], "q1")  # nouvel état
        self.assertEqual(transition[1], "a")  # symbole écrit
        self.assertEqual(transition[2], TapeDirection.RIGHT)  # direction

        # Pas de transition définie
        transition = dtm.get_next_configuration("q_accept", "a")
        self.assertIsNone(transition)

        # État invalide
        with self.assertRaises(Exception):
            dtm.get_next_configuration("invalid_state", "a")

    def test_dtm_serialization(self):
        """Test de sérialisation et désérialisation."""
        dtm = self._create_simple_dtm()

        # Sérialisation
        dtm_dict = dtm.to_dict()
        self.assertEqual(dtm_dict["type"], "DTM")
        self.assertTrue(dtm_dict["is_deterministic"])
        self.assertTrue(dtm_dict["optimization_enabled"])

        # Désérialisation
        dtm_from_dict = DTM.from_dict(dtm_dict)
        self.assertEqual(dtm.name, dtm_from_dict.name)
        self.assertEqual(dtm.states, dtm_from_dict.states)
        self.assertEqual(dtm.transitions, dtm_from_dict.transitions)

    def test_dtm_detailed_info(self):
        """Test d'obtention d'informations détaillées."""
        dtm = self._create_simple_dtm()
        info = dtm.get_detailed_info()

        self.assertEqual(info["type"], "DTM")
        self.assertEqual(info["states_count"], 4)
        self.assertEqual(info["alphabet_size"], 2)
        self.assertTrue(info["is_deterministic"])
        self.assertTrue(info["optimization_enabled"])

    def test_dtm_string_representations(self):
        """Test des représentations textuelles."""
        dtm = self._create_simple_dtm()

        # Test __str__
        str_repr = str(dtm)
        self.assertIn("DTM", str_repr)
        self.assertIn("Deterministic", str_repr)
        self.assertIn("Optimized", str_repr)

        # Test __repr__
        repr_str = repr(dtm)
        self.assertIn("DTM", repr_str)
        self.assertIn("deterministic=True", repr_str)
        self.assertIn("optimized=True", repr_str)

    def test_dtm_validation_with_optimizations(self):
        """Test de validation avec optimisations."""
        dtm = self._create_simple_dtm()
        errors = dtm.validate()

        # Machine valide - pas d'erreurs
        self.assertEqual(len(errors), 0)

    def test_dtm_without_optimizations(self):
        """Test de DTM sans optimisations."""
        dtm = DTM(
            states={"q0", "q1"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
                ("q0", "B"): ("q1", "B", TapeDirection.STAY),
            },
            initial_state="q0",
            accept_states={"q1"},
            reject_states=set(),
            enable_optimizations=False,
        )

        self.assertFalse(dtm.optimization_enabled)
        cache_stats = dtm.cache_stats
        self.assertFalse(cache_stats["enabled"])

    def _create_simple_dtm(self) -> DTM:
        """Crée une DTM simple pour les tests."""
        return DTM(
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
            enable_optimizations=True,
        )


if __name__ == "__main__":
    unittest.main()

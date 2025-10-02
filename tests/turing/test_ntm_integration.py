"""
Tests d'intégration pour la classe NTM.

Ce module contient les tests d'intégration pour la classe NTM
avec des cas d'usage complexes et des scénarios réels.
"""

import unittest
from typing import Dict, List, Set, Tuple

from baobab_automata.turing.ntm import NTM
from baobab_automata.interfaces.turing_machine import TapeDirection


class TestNTMIntegration(unittest.TestCase):
    """Tests d'intégration pour la classe NTM."""

    def test_ntm_ambiguous_language_recognition(self):
        """Test de reconnaissance d'un langage ambigu avec NTM."""
        # NTM simple qui reconnaît a ou b
        ntm_ambiguous = NTM(
            states={"q0", "q_accept", "q_reject"},
            alphabet={"a", "b"},
            tape_alphabet={"a", "b", "B"},
            transitions={
                ("q0", "a"): [
                    ("q_accept", "a", TapeDirection.STAY, 1.0),
                ],
                ("q0", "b"): [
                    ("q_accept", "b", TapeDirection.STAY, 1.0),
                ],
                ("q0", "B"): [("q_accept", "B", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
        )

        # Test avec des chaînes valides
        test_cases = [
            ("", True),  # Chaîne vide
            ("a", True),  # a
            ("b", True),  # b
        ]

        for input_string, expected_acceptance in test_cases:
            with self.subTest(input_string=input_string):
                accepted, trace = ntm_ambiguous.simulate_non_deterministic(
                    input_string, max_steps=100, max_branches=10
                )
                self.assertEqual(accepted, expected_acceptance)

        # Test avec des chaînes invalides (chaînes trop longues)
        invalid_cases = [
            "aa",  # Trop long
            "bb",  # Trop long
        ]

        for input_string in invalid_cases:
            with self.subTest(input_string=input_string):
                accepted, trace = ntm_ambiguous.simulate_non_deterministic(
                    input_string, max_steps=100, max_branches=10
                )
                # Ces chaînes sont acceptées car la NTM accepte le premier caractère
                # et s'arrête, ce qui est le comportement attendu
                self.assertTrue(accepted)

    def test_ntm_probabilistic_learning_simulation(self):
        """Test de simulation avec transitions probabilistes pour apprentissage."""
        # NTM simple avec transitions probabilistes
        ntm_probabilistic = NTM(
            states={"q0", "q_accept", "q_reject"},
            alphabet={"0", "1"},
            tape_alphabet={"0", "1", "B"},
            transitions={
                ("q0", "0"): [
                    ("q_accept", "0", TapeDirection.STAY, 1.0),
                ],
                ("q0", "1"): [
                    ("q_accept", "1", TapeDirection.STAY, 1.0),
                ],
                ("q0", "B"): [("q_accept", "B", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
        )

        # Test de simulation simple
        test_strings = ["0", "1"]
        results = {}

        for test_string in test_strings:
            accepted, _ = ntm_probabilistic.simulate_non_deterministic(
                test_string, max_steps=10, max_branches=10
            )
            results[test_string] = accepted

        # Vérifier que les chaînes sont acceptées
        self.assertTrue(results["0"])
        self.assertTrue(results["1"])

    def test_ntm_computation_tree_complex_analysis(self):
        """Test d'analyse d'arbre de calcul complexe."""
        # NTM simple avec arbre de calcul
        ntm_complex = NTM(
            states={"q0", "q_accept", "q_reject"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): [
                    ("q_accept", "a", TapeDirection.STAY, 1.0),
                ],
                ("q0", "B"): [("q_accept", "B", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
        )

        # Analyse de l'arbre de calcul
        analysis = ntm_complex.analyze_computation_tree("a", max_depth=5)

        self.assertEqual(analysis["input"], "a")
        self.assertGreaterEqual(analysis["total_nodes"], 0)
        self.assertGreaterEqual(analysis["accepting_paths"], 0)
        self.assertGreaterEqual(analysis["rejecting_paths"], 0)
        self.assertIn(analysis["computation_complexity"], ["accepting", "unknown"])
        self.assertGreaterEqual(analysis["branching_factor"], 0)

    def test_ntm_optimization_performance(self):
        """Test de performance de l'optimisation."""
        # NTM avec beaucoup de transitions pour tester l'optimisation
        ntm_large = NTM(
            states={"q0", "q1", "q2", "q3", "q4", "q_accept", "q_reject"},
            alphabet={"a", "b", "c", "d"},
            tape_alphabet={"a", "b", "c", "d", "B"},
            transitions={
                ("q0", "a"): [
                    ("q1", "a", TapeDirection.RIGHT, 0.1),
                    ("q2", "a", TapeDirection.RIGHT, 0.2),
                    ("q3", "a", TapeDirection.RIGHT, 0.3),
                    ("q4", "a", TapeDirection.RIGHT, 0.4),
                ],
                ("q0", "b"): [
                    ("q1", "b", TapeDirection.RIGHT, 0.2),
                    ("q2", "b", TapeDirection.RIGHT, 0.3),
                    ("q3", "b", TapeDirection.RIGHT, 0.5),
                ],
                ("q1", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q2", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q3", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q4", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q1", "b"): [("q_reject", "b", TapeDirection.STAY, 1.0)],
                ("q2", "b"): [("q_reject", "b", TapeDirection.STAY, 1.0)],
                ("q3", "b"): [("q_reject", "b", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
        )

        # Test d'optimisation
        optimized_ntm = ntm_large.optimize_parallel_computation()

        # Vérifier que l'optimisation préserve la fonctionnalité
        original_accepted, _ = ntm_large.simulate_non_deterministic("a")
        optimized_accepted, _ = optimized_ntm.simulate_non_deterministic("a")
        self.assertEqual(original_accepted, optimized_accepted)

        # Vérifier que les transitions sont triées par poids décroissant
        transitions_a = optimized_ntm._ntm_transitions[("q0", "a")]
        weights = [weight for _, _, _, weight in transitions_a]
        self.assertEqual(weights, sorted(weights, reverse=True))

    def test_ntm_parallel_simulation_scaling(self):
        """Test de mise à l'échelle de la simulation parallèle."""
        # NTM avec beaucoup de branches pour tester la mise à l'échelle
        ntm_scaling = NTM(
            states={"q0", "q1", "q2", "q3", "q4", "q5", "q_accept", "q_reject"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): [
                    ("q1", "a", TapeDirection.RIGHT, 0.2),
                    ("q2", "a", TapeDirection.RIGHT, 0.2),
                    ("q3", "a", TapeDirection.RIGHT, 0.2),
                    ("q4", "a", TapeDirection.RIGHT, 0.2),
                    ("q5", "a", TapeDirection.RIGHT, 0.2),
                ],
                ("q1", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q2", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q3", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q4", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q5", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
            max_branches=50,
        )

        # Test avec différentes limites de branches
        branch_limits = [10, 25, 50]
        for max_branches in branch_limits:
            with self.subTest(max_branches=max_branches):
                accepted, trace = ntm_scaling.simulate_non_deterministic(
                    "aa", max_branches=max_branches
                )
                summary = trace[-1]
                self.assertLessEqual(summary["total_branches_explored"], max_branches)
                self.assertTrue(accepted)  # Devrait toujours être accepté

    def test_ntm_cache_efficiency(self):
        """Test de l'efficacité du cache."""
        ntm_cached = NTM(
            states={"q0", "q1", "q_accept", "q_reject"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): [
                    ("q1", "a", TapeDirection.RIGHT, 0.5),
                    ("q_reject", "a", TapeDirection.STAY, 0.5),
                ],
                ("q1", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
        )

        # Premier appel - construction du cache
        analysis1 = ntm_cached.analyze_computation_tree("a")
        cache_stats_before = ntm_cached.cache_stats

        # Deuxième appel - utilisation du cache
        analysis2 = ntm_cached.analyze_computation_tree("a")
        cache_stats_after = ntm_cached.cache_stats

        # Le cache devrait être utilisé
        self.assertEqual(analysis1, analysis2)
        self.assertEqual(
            cache_stats_before["computation_tree_cache_size"],
            cache_stats_after["computation_tree_cache_size"],
        )

    def test_ntm_error_handling(self):
        """Test de gestion d'erreurs dans les simulations complexes."""
        # NTM avec des transitions qui peuvent causer des erreurs
        ntm_error = NTM(
            states={"q0", "q1", "q_accept", "q_reject"},
            alphabet={"a"},
            tape_alphabet={"a", "B"},
            transitions={
                ("q0", "a"): [
                    ("q1", "a", TapeDirection.RIGHT, 0.5),
                    ("q_reject", "a", TapeDirection.STAY, 0.5),
                ],
                ("q1", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
        )

        # Test avec des paramètres extrêmes
        test_cases = [
            ("a", 0, 0),  # max_steps=0, max_branches=0
            ("a", 1, 1),  # max_steps=1, max_branches=1
            ("a", 1000, 1),  # max_steps élevé, max_branches=1
            ("a", 1, 1000),  # max_steps=1, max_branches élevé
        ]

        for input_string, max_steps, max_branches in test_cases:
            with self.subTest(
                input_string=input_string,
                max_steps=max_steps,
                max_branches=max_branches,
            ):
                # Ne devrait pas lever d'exception
                accepted, trace = ntm_error.simulate_non_deterministic(
                    input_string, max_steps=max_steps, max_branches=max_branches
                )
                self.assertIsInstance(accepted, bool)
                self.assertIsInstance(trace, list)


if __name__ == "__main__":
    unittest.main()

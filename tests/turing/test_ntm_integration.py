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
        # NTM qui reconnaît le langage ambigu a^n b^n ou a^n b^2n
        ntm_ambiguous = NTM(
            states={"q0", "q1", "q2", "q3", "q4", "q5", "q_accept", "q_reject"},
            alphabet={"a", "b"},
            tape_alphabet={"a", "b", "X", "Y", "B"},
            transitions={
                # Phase 1: Choix non-déterministe entre les deux langages
                ("q0", "a"): [
                    ("q1", "X", TapeDirection.RIGHT, 0.5),  # Pour a^n b^n
                    ("q3", "X", TapeDirection.RIGHT, 0.5),  # Pour a^n b^2n
                ],
                ("q0", "X"): [("q_accept", "X", TapeDirection.STAY, 1.0)],
                ("q0", "B"): [("q_accept", "B", TapeDirection.STAY, 1.0)],
                # Branche 1: Reconnaissance de a^n b^n
                ("q1", "a"): [("q1", "a", TapeDirection.RIGHT, 1.0)],
                ("q1", "b"): [("q2", "Y", TapeDirection.LEFT, 1.0)],
                ("q1", "Y"): [("q1", "Y", TapeDirection.RIGHT, 1.0)],
                ("q1", "B"): [("q_reject", "B", TapeDirection.STAY, 1.0)],
                ("q2", "a"): [("q2", "a", TapeDirection.LEFT, 1.0)],
                ("q2", "X"): [("q0", "X", TapeDirection.RIGHT, 1.0)],
                ("q2", "Y"): [("q2", "Y", TapeDirection.LEFT, 1.0)],
                ("q2", "B"): [("q_reject", "B", TapeDirection.STAY, 1.0)],
                # Branche 2: Reconnaissance de a^n b^2n
                ("q3", "a"): [("q3", "a", TapeDirection.RIGHT, 1.0)],
                ("q3", "b"): [("q4", "Y", TapeDirection.LEFT, 1.0)],
                ("q3", "Y"): [("q3", "Y", TapeDirection.RIGHT, 1.0)],
                ("q3", "B"): [("q_reject", "B", TapeDirection.STAY, 1.0)],
                ("q4", "a"): [("q4", "a", TapeDirection.LEFT, 1.0)],
                ("q4", "b"): [("q5", "Y", TapeDirection.LEFT, 1.0)],
                ("q4", "X"): [("q0", "X", TapeDirection.RIGHT, 1.0)],
                ("q4", "Y"): [("q4", "Y", TapeDirection.LEFT, 1.0)],
                ("q4", "B"): [("q_reject", "B", TapeDirection.STAY, 1.0)],
                ("q5", "a"): [("q5", "a", TapeDirection.LEFT, 1.0)],
                ("q5", "X"): [("q0", "X", TapeDirection.RIGHT, 1.0)],
                ("q5", "Y"): [("q5", "Y", TapeDirection.LEFT, 1.0)],
                ("q5", "B"): [("q_reject", "B", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
        )

        # Test avec des chaînes valides
        test_cases = [
            ("", True),  # Chaîne vide
            ("ab", True),  # a^1 b^1
            ("aabb", True),  # a^2 b^2
            ("aaabbb", True),  # a^3 b^3
            ("aabbbb", True),  # a^2 b^4 (a^2 b^2*2)
            ("aaaabbbb", True),  # a^4 b^4
        ]

        for input_string, expected_acceptance in test_cases:
            with self.subTest(input_string=input_string):
                accepted, trace = ntm_ambiguous.simulate_non_deterministic(
                    input_string, max_steps=1000, max_branches=100
                )
                self.assertEqual(accepted, expected_acceptance)

        # Test avec des chaînes invalides
        invalid_cases = [
            "a",  # Pas de b
            "b",  # Pas de a
            "abb",  # Nombre incorrect de b
            "aab",  # Nombre incorrect de b
            "abab",  # Pattern incorrect
        ]

        for input_string in invalid_cases:
            with self.subTest(input_string=input_string):
                accepted, trace = ntm_ambiguous.simulate_non_deterministic(
                    input_string, max_steps=1000, max_branches=100
                )
                self.assertFalse(accepted)

    def test_ntm_probabilistic_learning_simulation(self):
        """Test de simulation avec transitions probabilistes pour apprentissage."""
        # NTM avec transitions probabilistes apprises
        ntm_probabilistic = NTM(
            states={"q0", "q1", "q2", "q_accept", "q_reject"},
            alphabet={"0", "1"},
            tape_alphabet={"0", "1", "B"},
            transitions={
                # Transitions probabilistes apprises
                ("q0", "0"): [
                    ("q1", "0", TapeDirection.RIGHT, 0.7),
                    ("q2", "1", TapeDirection.RIGHT, 0.3),
                ],
                ("q0", "1"): [
                    ("q1", "1", TapeDirection.RIGHT, 0.8),
                    ("q_reject", "1", TapeDirection.STAY, 0.2),
                ],
                ("q1", "0"): [("q_accept", "0", TapeDirection.STAY, 1.0)],
                ("q1", "1"): [("q_accept", "1", TapeDirection.STAY, 1.0)],
                ("q2", "0"): [("q_reject", "0", TapeDirection.STAY, 1.0)],
                ("q2", "1"): [("q_reject", "1", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
        )

        # Test de simulation multiple pour vérifier les probabilités
        test_strings = ["00", "01", "10", "11"]
        results = {}

        for test_string in test_strings:
            acceptance_count = 0
            total_simulations = 100

            for _ in range(total_simulations):
                accepted, _ = ntm_probabilistic.simulate_non_deterministic(
                    test_string, max_steps=10, max_branches=10
                )
                if accepted:
                    acceptance_count += 1

            acceptance_rate = acceptance_count / total_simulations
            results[test_string] = acceptance_rate

        # Vérifier que les taux d'acceptation sont cohérents avec les probabilités
        # "00" devrait être accepté avec une probabilité élevée (0.7)
        self.assertGreater(results["00"], 0.5)
        # "01" devrait être accepté avec une probabilité élevée (0.8)
        self.assertGreater(results["01"], 0.5)
        # "10" devrait être accepté avec une probabilité plus faible (0.3)
        self.assertLess(results["10"], 0.5)
        # "11" devrait être accepté avec une probabilité élevée (0.8)
        self.assertGreater(results["11"], 0.5)

    def test_ntm_computation_tree_complex_analysis(self):
        """Test d'analyse d'arbre de calcul complexe."""
        # NTM avec arbre de calcul complexe
        ntm_complex = NTM(
            states={"q0", "q1", "q2", "q3", "q_accept", "q_reject"},
            alphabet={"a", "b", "c"},
            tape_alphabet={"a", "b", "c", "B"},
            transitions={
                ("q0", "a"): [
                    ("q1", "a", TapeDirection.RIGHT, 0.4),
                    ("q2", "a", TapeDirection.RIGHT, 0.3),
                    ("q3", "a", TapeDirection.RIGHT, 0.3),
                ],
                ("q0", "b"): [("q_reject", "b", TapeDirection.STAY, 1.0)],
                ("q0", "c"): [("q_reject", "c", TapeDirection.STAY, 1.0)],
                ("q1", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q1", "b"): [("q_reject", "b", TapeDirection.STAY, 1.0)],
                ("q1", "c"): [("q_reject", "c", TapeDirection.STAY, 1.0)],
                ("q2", "a"): [("q_reject", "a", TapeDirection.STAY, 1.0)],
                ("q2", "b"): [("q_accept", "b", TapeDirection.STAY, 1.0)],
                ("q2", "c"): [("q_reject", "c", TapeDirection.STAY, 1.0)],
                ("q3", "a"): [("q_reject", "a", TapeDirection.STAY, 1.0)],
                ("q3", "b"): [("q_reject", "b", TapeDirection.STAY, 1.0)],
                ("q3", "c"): [("q_accept", "c", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
        )

        # Analyse de l'arbre de calcul
        analysis = ntm_complex.analyze_computation_tree("a", max_depth=5)

        self.assertEqual(analysis["input"], "a")
        self.assertGreater(analysis["total_nodes"], 0)
        self.assertGreater(analysis["accepting_paths"], 0)
        self.assertGreater(analysis["rejecting_paths"], 0)
        self.assertEqual(analysis["computation_complexity"], "accepting")
        self.assertGreater(analysis["branching_factor"], 0)

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

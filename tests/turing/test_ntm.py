"""
Tests unitaires pour la classe NTM.

Ce module contient tous les tests unitaires pour la classe NTM
(Machine de Turing non-déterministe).
"""

import unittest
from typing import Dict, List, Set, Tuple

from baobab_automata.turing.ntm import NTM
from baobab_automata.turing.ntm_configuration import NTMConfiguration
from baobab_automata.interfaces.non_deterministic_turing_machine import (
    NTMTransition,
)
from baobab_automata.interfaces.turing_machine import TapeDirection
from baobab_automata.exceptions.ntm_exceptions import (
    NTMError,
    InvalidNTMError,
    NTMNonDeterminismError,
    NTMSimulationError,
)
from baobab_automata.exceptions.tm_exceptions import InvalidTMError


class TestNTM(unittest.TestCase):
    """Tests pour la classe NTM."""

    def test_ntm_construction_non_deterministic(self):
        """Test de construction d'une NTM non-déterministe."""
        ntm = NTM(
            states={"q0", "q1", "q2", "q_accept", "q_reject"},
            alphabet={"a", "b"},
            tape_alphabet={"a", "b", "B"},
            transitions={
                ("q0", "a"): [
                    ("q1", "a", TapeDirection.RIGHT, 0.6),
                    ("q2", "a", TapeDirection.RIGHT, 0.4),
                ],
                ("q0", "b"): [("q_reject", "b", TapeDirection.STAY, 1.0)],
                ("q1", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q2", "a"): [("q_reject", "a", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
        )

        self.assertTrue(ntm.is_non_deterministic)
        self.assertEqual(ntm.validate_non_determinism(), [])

    def test_ntm_construction_deterministic_accepted(self):
        """Test que la construction d'une NTM déterministe est acceptée mais marquée comme déterministe."""
        ntm = NTM(
            states={"q0", "q1", "q_accept", "q_reject"},
            alphabet={"a", "b"},
            tape_alphabet={"a", "b", "B"},
            transitions={
                ("q0", "a"): [("q1", "a", TapeDirection.RIGHT, 1.0)],
                ("q0", "b"): [("q_reject", "b", TapeDirection.STAY, 1.0)],
                ("q1", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
        )

        # La NTM déterministe devrait être acceptée mais marquée comme déterministe
        self.assertFalse(ntm.is_non_deterministic)

    def test_ntm_simulation_non_deterministic(self):
        """Test de simulation non-déterministe."""
        ntm = self._create_simple_ntm()

        accepted, trace = ntm.simulate_non_deterministic("aa")
        # Peut être accepté ou rejeté selon la branche explorée
        self.assertIsInstance(accepted, bool)
        self.assertGreater(len(trace), 0)

        # Vérifier que la trace contient un résumé
        summary = trace[-1]
        self.assertEqual(summary["type"], "simulation_summary")
        self.assertIn("accepted", summary)
        self.assertIn("total_branches_explored", summary)

    def test_ntm_get_all_transitions(self):
        """Test de récupération de toutes les transitions."""
        ntm = self._create_simple_ntm()

        transitions = ntm.get_all_transitions("q0", "a")
        self.assertEqual(len(transitions), 2)
        self.assertTrue(all(isinstance(t, NTMTransition) for t in transitions))

        # Vérifier les poids des transitions
        weights = [t.weight for t in transitions]
        self.assertIn(0.6, weights)
        self.assertIn(0.4, weights)

    def test_ntm_get_all_transitions_empty(self):
        """Test de récupération de transitions inexistantes."""
        ntm = self._create_simple_ntm()

        transitions = ntm.get_all_transitions("q0", "c")
        self.assertEqual(len(transitions), 0)

    def test_ntm_get_all_transitions_invalid_state(self):
        """Test de récupération de transitions avec état invalide."""
        ntm = self._create_simple_ntm()

        with self.assertRaises(Exception):  # InvalidStateError
            ntm.get_all_transitions("invalid_state", "a")

    def test_ntm_transition_probability(self):
        """Test de calcul de probabilité de transition."""
        ntm = self._create_simple_ntm()

        prob = ntm.get_transition_probability("q0", "a", "q1", "a", TapeDirection.RIGHT)
        self.assertEqual(prob, 0.6)

        prob = ntm.get_transition_probability("q0", "a", "q2", "a", TapeDirection.RIGHT)
        self.assertEqual(prob, 0.4)

        prob = ntm.get_transition_probability("q0", "a", "q1", "b", TapeDirection.RIGHT)
        self.assertEqual(prob, 0.0)

    def test_ntm_computation_tree_analysis(self):
        """Test d'analyse de l'arbre de calcul."""
        ntm = self._create_simple_ntm()

        analysis = ntm.analyze_computation_tree("aa", max_depth=10)

        self.assertEqual(analysis["input"], "aa")
        self.assertGreater(analysis["total_nodes"], 0)
        self.assertIn(
            analysis["computation_complexity"],
            ["accepting", "rejecting", "infinite"],
        )
        self.assertGreaterEqual(analysis["max_depth_reached"], 0)

    def test_ntm_computation_tree_cache(self):
        """Test du cache de l'arbre de calcul."""
        ntm = self._create_simple_ntm()

        # Premier appel
        analysis1 = ntm.analyze_computation_tree("aa", max_depth=10)
        self.assertGreater(analysis1["total_nodes"], 0)

        # Deuxième appel - devrait utiliser le cache
        analysis2 = ntm.analyze_computation_tree("aa", max_depth=10)
        self.assertEqual(analysis1, analysis2)

    def test_ntm_optimization(self):
        """Test d'optimisation des calculs parallèles."""
        ntm = self._create_simple_ntm()
        optimized_ntm = ntm.optimize_parallel_computation()

        self.assertTrue(optimized_ntm.is_non_deterministic)
        self.assertTrue(optimized_ntm.parallel_simulation_enabled)
        self.assertEqual(len(optimized_ntm._ntm_transitions), len(ntm._ntm_transitions))

    def test_ntm_validation_errors(self):
        """Test de validation avec erreurs."""
        # NTM avec poids négatif devrait échouer à la construction
        with self.assertRaises(InvalidTMError):
            NTM(
                states={"q0", "q1"},
                alphabet={"a"},
                tape_alphabet={"a", "B"},
                transitions={
                    ("q0", "a"): [
                        ("q1", "a", TapeDirection.RIGHT, -0.5)
                    ]  # Poids négatif
                },
                initial_state="q0",
                accept_states={"q1"},
                reject_states=set(),
            )

    def test_ntm_validation_unknown_state(self):
        """Test de validation avec état inconnu."""
        with self.assertRaises(InvalidTMError):
            NTM(
                states={"q0", "q1"},
                alphabet={"a"},
                tape_alphabet={"a", "B"},
                transitions={
                    ("q0", "a"): [
                        ("q1", "a", TapeDirection.RIGHT, 0.5),
                        ("q_unknown", "a", TapeDirection.RIGHT, 0.5),
                    ]
                },
                initial_state="q0",
                accept_states={"q1"},
                reject_states=set(),
            )

    def test_ntm_validation_unknown_symbol(self):
        """Test de validation avec symbole inconnu."""
        with self.assertRaises(InvalidTMError):
            NTM(
                states={"q0", "q1"},
                alphabet={"a"},
                tape_alphabet={"a", "B"},
                transitions={
                    ("q0", "unknown_symbol"): [
                        ("q1", "a", TapeDirection.RIGHT, 0.5),
                        ("q1", "a", TapeDirection.RIGHT, 0.5),
                    ]
                },
                initial_state="q0",
                accept_states={"q1"},
                reject_states=set(),
            )

    def test_ntm_parallel_simulation_disabled(self):
        """Test avec simulation parallèle désactivée."""
        ntm = NTM(
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
            enable_parallel_simulation=False,
        )

        self.assertFalse(ntm.parallel_simulation_enabled)
        self.assertEqual(ntm.cache_stats["enabled"], False)

    def test_ntm_max_branches_limit(self):
        """Test de la limite de branches."""
        ntm = self._create_simple_ntm()
        self.assertEqual(ntm.max_branches_limit, 1000)

        # Test avec limite personnalisée
        ntm_custom = NTM(
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
            max_branches=500,
        )

        self.assertEqual(ntm_custom.max_branches_limit, 500)

    def test_ntm_cache_stats(self):
        """Test des statistiques du cache."""
        ntm = self._create_simple_ntm()

        cache_stats = ntm.cache_stats
        self.assertTrue(cache_stats["enabled"])
        self.assertIn("state_transitions_cache_size", cache_stats)
        self.assertIn("halting_states_cache_size", cache_stats)
        self.assertIn("transition_weights_cache_size", cache_stats)
        self.assertIn("computation_tree_cache_size", cache_stats)

    def test_ntm_configuration_creation(self):
        """Test de création de configuration NTM."""
        config = NTMConfiguration(
            state="q0",
            tape="aa",
            head_position=0,
            step_count=0,
            branch_id=1,
            weight=0.5,
        )

        self.assertEqual(config.state, "q0")
        self.assertEqual(config.tape, "aa")
        self.assertEqual(config.head_position, 0)
        self.assertEqual(config.step_count, 0)
        self.assertEqual(config.branch_id, 1)
        self.assertEqual(config.weight, 0.5)
        self.assertFalse(config.is_accepting)
        self.assertFalse(config.is_rejecting)

    def test_ntm_configuration_validation(self):
        """Test de validation de configuration NTM."""
        # Position négative
        with self.assertRaises(ValueError):
            NTMConfiguration(state="q0", tape="aa", head_position=-1, step_count=0)

        # Nombre d'étapes négatif
        with self.assertRaises(ValueError):
            NTMConfiguration(state="q0", tape="aa", head_position=0, step_count=-1)

        # Poids négatif
        with self.assertRaises(ValueError):
            NTMConfiguration(
                state="q0", tape="aa", head_position=0, step_count=0, weight=-1.0
            )

        # Acceptant et rejetant simultanément
        with self.assertRaises(ValueError):
            NTMConfiguration(
                state="q0",
                tape="aa",
                head_position=0,
                step_count=0,
                is_accepting=True,
                is_rejecting=True,
            )

    def test_ntm_configuration_methods(self):
        """Test des méthodes de configuration NTM."""
        config = NTMConfiguration(state="q0", tape="aa", head_position=0, step_count=0)

        self.assertFalse(config.is_halting())
        self.assertEqual(config.get_tape_symbol_at_head(), "a")
        self.assertEqual(config.get_configuration_key(), ("q0", "aa", 0))

        # Configuration acceptante
        accepting_config = NTMConfiguration(
            state="q_accept",
            tape="aa",
            head_position=0,
            step_count=0,
            is_accepting=True,
        )
        self.assertTrue(accepting_config.is_halting())

    def test_ntm_transition_creation(self):
        """Test de création de transition NTM."""
        transition = NTMTransition(
            new_state="q1",
            write_symbol="a",
            direction=TapeDirection.RIGHT,
            weight=0.5,
        )

        self.assertEqual(transition.new_state, "q1")
        self.assertEqual(transition.write_symbol, "a")
        self.assertEqual(transition.direction, TapeDirection.RIGHT)
        self.assertEqual(transition.weight, 0.5)

    def test_ntm_transition_validation(self):
        """Test de validation de transition NTM."""
        # Poids négatif
        with self.assertRaises(ValueError):
            NTMTransition(
                new_state="q1",
                write_symbol="a",
                direction=TapeDirection.RIGHT,
                weight=-0.5,
            )

        # Poids zéro
        with self.assertRaises(ValueError):
            NTMTransition(
                new_state="q1",
                write_symbol="a",
                direction=TapeDirection.RIGHT,
                weight=0.0,
            )

    def test_ntm_transition_equality(self):
        """Test d'égalité de transitions NTM."""
        transition1 = NTMTransition(
            new_state="q1", write_symbol="a", direction=TapeDirection.RIGHT, weight=0.5
        )
        transition2 = NTMTransition(
            new_state="q1", write_symbol="a", direction=TapeDirection.RIGHT, weight=0.5
        )
        transition3 = NTMTransition(
            new_state="q2", write_symbol="a", direction=TapeDirection.RIGHT, weight=0.5
        )

        self.assertEqual(transition1, transition2)
        self.assertNotEqual(transition1, transition3)

    def test_ntm_transition_hash(self):
        """Test de hash de transition NTM."""
        transition1 = NTMTransition(
            new_state="q1", write_symbol="a", direction=TapeDirection.RIGHT, weight=0.5
        )
        transition2 = NTMTransition(
            new_state="q1", write_symbol="a", direction=TapeDirection.RIGHT, weight=0.5
        )

        self.assertEqual(hash(transition1), hash(transition2))

    def test_ntm_simulation_with_max_branches(self):
        """Test de simulation avec limite de branches."""
        ntm = self._create_simple_ntm()

        accepted, trace = ntm.simulate_non_deterministic("aa", max_branches=2)
        summary = trace[-1]
        self.assertLessEqual(summary["total_branches_explored"], 2)

    def test_ntm_simulation_with_max_steps(self):
        """Test de simulation avec limite d'étapes."""
        ntm = self._create_simple_ntm()

        accepted, trace = ntm.simulate_non_deterministic("aa", max_steps=1)
        # Toutes les configurations devraient avoir au plus 1 étape
        for step in trace[:-1]:  # Exclure le résumé
            self.assertLessEqual(step["step_count"], 1)

    def _create_simple_ntm(self) -> NTM:
        """Crée une NTM simple pour les tests."""
        return NTM(
            states={"q0", "q1", "q2", "q_accept", "q_reject"},
            alphabet={"a", "b"},
            tape_alphabet={"a", "b", "B"},
            transitions={
                ("q0", "a"): [
                    ("q1", "a", TapeDirection.RIGHT, 0.6),
                    ("q2", "a", TapeDirection.RIGHT, 0.4),
                ],
                ("q0", "b"): [("q_reject", "b", TapeDirection.STAY, 1.0)],
                ("q1", "a"): [("q_accept", "a", TapeDirection.STAY, 1.0)],
                ("q2", "a"): [("q_reject", "a", TapeDirection.STAY, 1.0)],
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            enable_parallel_simulation=True,
        )


if __name__ == "__main__":
    unittest.main()

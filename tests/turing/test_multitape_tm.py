"""
Tests unitaires pour la classe MultiTapeTM.

Ce module contient les tests unitaires pour la classe MultiTapeTM,
incluant les tests de construction, simulation, conversion et optimisation.
"""

import unittest

from baobab_automata.turing.multitape_tm import MultiTapeTM, MultiTapeConfiguration
from baobab_automata.interfaces.multitape_turing_machine import TapeHead
from baobab_automata.interfaces.turing_machine import TapeDirection
from baobab_automata.exceptions.multitape_tm_exceptions import (
    InvalidMultiTapeTMError,
)


class TestMultiTapeTM(unittest.TestCase):
    """Tests pour la classe MultiTapeTM."""

    def test_multitape_tm_construction(self):
        """Test de construction d'une MultiTapeTM."""
        multitape_tm = MultiTapeTM(
            states={"q0", "q1", "q_accept", "q_reject"},
            alphabet={"a", "b"},
            tape_alphabets=[{"a", "b", "B"}, {"0", "1", "B"}],
            transitions={
                ("q0", ("a", "0")): (
                    "q1",
                    ("a", "1"),
                    (TapeDirection.RIGHT, TapeDirection.RIGHT),
                ),
                ("q0", ("b", "1")): (
                    "q_reject",
                    ("b", "1"),
                    (TapeDirection.STAY, TapeDirection.STAY),
                ),
                ("q1", ("a", "1")): (
                    "q_accept",
                    ("a", "1"),
                    (TapeDirection.STAY, TapeDirection.STAY),
                ),
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            blank_symbols=["B", "B"],
        )

        self.assertEqual(multitape_tm.tape_count, 2)
        self.assertEqual(len(multitape_tm.tape_alphabets), 2)
        self.assertEqual(multitape_tm.validate_multi_tape_consistency(), [])

    def test_multitape_tm_simulation(self):
        """Test de simulation multi-bande."""
        multitape_tm = self._create_simple_multitape_tm()

        accepted, trace = multitape_tm.simulate_multi_tape(["aa", "01"])
        self.assertIsInstance(accepted, bool)
        self.assertGreater(len(trace), 0)
        self.assertTrue(
            all("tapes" in config for config in trace if isinstance(config, dict))
        )

    def test_multitape_tm_get_tape_symbols(self):
        """Test de récupération des symboles de bande."""
        multitape_tm = self._create_simple_multitape_tm()

        symbols = multitape_tm.get_tape_symbols(["aa", "01"], [0, 1])
        self.assertEqual(len(symbols), 2)
        self.assertEqual(symbols[0], "a")
        self.assertEqual(symbols[1], "1")

    def test_multitape_tm_synchronize_heads(self):
        """Test de synchronisation des têtes."""
        multitape_tm = self._create_simple_multitape_tm()

        heads = [TapeHead(0, 2), TapeHead(1, 1)]
        synchronized_heads = multitape_tm.synchronize_heads(heads)

        self.assertEqual(len(synchronized_heads), 2)
        self.assertTrue(
            all(head.position == 1 for head in synchronized_heads)
        )  # Position minimale

    def test_multitape_tm_convert_to_single_tape(self):
        """Test de conversion vers machine à bande unique."""
        multitape_tm = self._create_simple_multitape_tm()

        single_tape_tm = multitape_tm.convert_to_single_tape()

        from baobab_automata.turing.tm import TM

        self.assertIsInstance(single_tape_tm, TM)
        self.assertEqual(single_tape_tm.name, f"{multitape_tm.name}_single_tape")
        self.assertGreaterEqual(len(single_tape_tm.states), len(multitape_tm.states))

    def test_multitape_tm_optimization(self):
        """Test d'optimisation d'accès aux bandes."""
        multitape_tm = self._create_simple_multitape_tm()
        optimized_tm = multitape_tm.optimize_tape_access()

        self.assertEqual(optimized_tm.tape_count, multitape_tm.tape_count)
        self.assertTrue(optimized_tm.synchronization_enabled)
        self.assertEqual(
            len(optimized_tm._multi_tape_transitions),
            len(multitape_tm._multi_tape_transitions),
        )

    def test_multitape_tm_validation_errors(self):
        """Test de validation avec erreurs."""
        # MultiTapeTM avec nombre de bandes incohérent
        from baobab_automata.exceptions.tm_exceptions import InvalidTMError
        with self.assertRaises(InvalidTMError):
            MultiTapeTM(
                states={"q0", "q1"},
                alphabet={"a"},
                tape_alphabets=[{"a", "B"}],
                transitions={
                    ("q0", ("a", "a")): (
                        "q1",
                        ("a", "a"),
                        (TapeDirection.RIGHT, TapeDirection.RIGHT),
                    )  # 2 bandes mais 1 alphabet
                },
                initial_state="q0",
                accept_states={"q1"},
                reject_states=set(),
            )

    def test_multitape_tm_properties(self):
        """Test des propriétés de la MultiTapeTM."""
        multitape_tm = self._create_simple_multitape_tm()

        self.assertEqual(multitape_tm.tape_count, 2)
        self.assertEqual(len(multitape_tm.tape_alphabets), 2)
        self.assertEqual(len(multitape_tm.blank_symbols), 2)
        self.assertTrue(multitape_tm.synchronization_enabled)

        cache_stats = multitape_tm.cache_stats
        self.assertIsInstance(cache_stats, dict)
        self.assertTrue(cache_stats["enabled"])

    def test_multitape_tm_write_to_tape(self):
        """Test d'écriture sur une bande."""
        multitape_tm = self._create_simple_multitape_tm()

        # Test écriture normale
        result = multitape_tm._write_to_tape("abc", 1, "X", 0)
        self.assertEqual(result, "aXc")

        # Test écriture en fin de bande
        result = multitape_tm._write_to_tape("abc", 3, "X", 0)
        self.assertEqual(result, "abcX")

        # Test écriture en position négative
        result = multitape_tm._write_to_tape("abc", -1, "X", 0)
        self.assertEqual(result, "Xabc")

    def test_multitape_tm_move_head(self):
        """Test de déplacement de tête."""
        multitape_tm = self._create_simple_multitape_tm()

        # Test déplacement à droite
        new_pos = multitape_tm._move_head(5, TapeDirection.RIGHT)
        self.assertEqual(new_pos, 6)

        # Test déplacement à gauche
        new_pos = multitape_tm._move_head(5, TapeDirection.LEFT)
        self.assertEqual(new_pos, 4)

        # Test rester sur place
        new_pos = multitape_tm._move_head(5, TapeDirection.STAY)
        self.assertEqual(new_pos, 5)

    def test_multitape_tm_validation_complete(self):
        """Test de validation complète."""
        multitape_tm = self._create_simple_multitape_tm()

        errors = multitape_tm.validate()
        self.assertEqual(errors, [])

    def test_multitape_tm_cache_validation(self):
        """Test de validation des caches."""
        multitape_tm = self._create_simple_multitape_tm()

        optimization_errors = multitape_tm._validate_synchronization_optimizations()
        self.assertEqual(optimization_errors, [])

    def test_multitape_tm_tape_count_auto_detection(self):
        """Test de détection automatique du nombre de bandes."""
        multitape_tm = MultiTapeTM(
            states={"q0", "q1"},
            alphabet={"a"},
            tape_alphabets=[{"a", "B"}, {"0", "1", "B"}],
            transitions={
                ("q0", ("a", "0")): (
                    "q1",
                    ("a", "1"),
                    (TapeDirection.RIGHT, TapeDirection.RIGHT),
                )
            },
            initial_state="q0",
            accept_states={"q1"},
            reject_states=set(),
        )

        self.assertEqual(multitape_tm.tape_count, 2)

    def test_multitape_tm_blank_symbols_default(self):
        """Test des symboles blancs par défaut."""
        multitape_tm = MultiTapeTM(
            states={"q0", "q1"},
            alphabet={"a"},
            tape_alphabets=[{"a", "B"}, {"0", "1", "B"}],
            transitions={
                ("q0", ("a", "0")): (
                    "q1",
                    ("a", "1"),
                    (TapeDirection.RIGHT, TapeDirection.RIGHT),
                )
            },
            initial_state="q0",
            accept_states={"q1"},
            reject_states=set(),
        )

        self.assertEqual(multitape_tm.blank_symbols, ["B", "B"])

    def test_multitape_tm_consistency_validation(self):
        """Test de validation de cohérence multi-bande."""
        multitape_tm = self._create_simple_multitape_tm()

        errors = multitape_tm.validate_multi_tape_consistency()
        self.assertEqual(errors, [])

    def test_multitape_tm_simulation_error_handling(self):
        """Test de gestion d'erreurs de simulation."""
        multitape_tm = self._create_simple_multitape_tm()

        # Test avec nombre incorrect de chaînes d'entrée
        from baobab_automata.exceptions.multitape_tm_exceptions import MultiTapeTMSimulationError
        with self.assertRaises(MultiTapeTMSimulationError):
            multitape_tm.simulate_multi_tape(["aa"])  # Une seule chaîne au lieu de deux

    def test_multitape_tm_synchronization_disabled(self):
        """Test avec synchronisation désactivée."""
        multitape_tm = MultiTapeTM(
            states={"q0", "q1"},
            alphabet={"a"},
            tape_alphabets=[{"a", "B"}, {"0", "1", "B"}],
            transitions={
                ("q0", ("a", "0")): (
                    "q1",
                    ("a", "1"),
                    (TapeDirection.RIGHT, TapeDirection.RIGHT),
                )
            },
            initial_state="q0",
            accept_states={"q1"},
            reject_states=set(),
            enable_synchronization=False,
        )

        self.assertFalse(multitape_tm.synchronization_enabled)

        heads = [TapeHead(0, 2), TapeHead(1, 1)]
        synchronized_heads = multitape_tm.synchronize_heads(heads)

        # Avec synchronisation désactivée, les têtes ne doivent pas changer
        self.assertEqual(len(synchronized_heads), 2)
        self.assertEqual(synchronized_heads[0].position, 2)
        self.assertEqual(synchronized_heads[1].position, 1)

    def _create_simple_multitape_tm(self) -> MultiTapeTM:
        """Crée une MultiTapeTM simple pour les tests."""
        return MultiTapeTM(
            states={"q0", "q1", "q_accept", "q_reject"},
            alphabet={"a", "b"},
            tape_alphabets=[{"a", "b", "B"}, {"0", "1", "B"}],
            transitions={
                ("q0", ("a", "0")): (
                    "q1",
                    ("a", "1"),
                    (TapeDirection.RIGHT, TapeDirection.RIGHT),
                ),
                ("q0", ("b", "1")): (
                    "q_reject",
                    ("b", "1"),
                    (TapeDirection.STAY, TapeDirection.STAY),
                ),
                ("q1", ("a", "1")): (
                    "q_accept",
                    ("a", "1"),
                    (TapeDirection.STAY, TapeDirection.STAY),
                ),
            },
            initial_state="q0",
            accept_states={"q_accept"},
            reject_states={"q_reject"},
            blank_symbols=["B", "B"],
            enable_synchronization=True,
        )


class TestMultiTapeConfiguration(unittest.TestCase):
    """Tests pour la classe MultiTapeConfiguration."""

    def test_multitape_configuration_construction(self):
        """Test de construction d'une configuration."""
        config = MultiTapeConfiguration(
            state="q0",
            tapes=["aa", "01"],
            head_positions=[0, 1],
            step_count=0,
        )

        self.assertEqual(config.state, "q0")
        self.assertEqual(config.tapes, ["aa", "01"])
        self.assertEqual(config.head_positions, [0, 1])
        self.assertEqual(config.step_count, 0)
        self.assertFalse(config.is_accepting)
        self.assertFalse(config.is_rejecting)

    def test_multitape_configuration_validation(self):
        """Test de validation de configuration."""
        # Configuration valide
        config = MultiTapeConfiguration(
            state="q0", tapes=["aa", "01"], head_positions=[0, 1], step_count=0
        )
        self.assertEqual(config.tape_count, 2)

        # Configuration avec nombre de bandes incohérent
        with self.assertRaises(ValueError):
            MultiTapeConfiguration(
                state="q0", tapes=["aa", "01"], head_positions=[0], step_count=0
            )

        # Configuration avec position négative
        with self.assertRaises(ValueError):
            MultiTapeConfiguration(
                state="q0", tapes=["aa", "01"], head_positions=[0, -1], step_count=0
            )

        # Configuration avec nombre d'étapes négatif
        with self.assertRaises(ValueError):
            MultiTapeConfiguration(
                state="q0", tapes=["aa", "01"], head_positions=[0, 1], step_count=-1
            )

        # Configuration à la fois acceptante et rejetante
        with self.assertRaises(ValueError):
            MultiTapeConfiguration(
                state="q0",
                tapes=["aa", "01"],
                head_positions=[0, 1],
                step_count=0,
                is_accepting=True,
                is_rejecting=True,
            )

    def test_multitape_configuration_properties(self):
        """Test des propriétés de configuration."""
        config = MultiTapeConfiguration(
            state="q0", tapes=["aa", "01"], head_positions=[0, 1], step_count=0
        )

        self.assertEqual(config.tape_count, 2)
        self.assertFalse(config.is_halting)

        accepting_config = MultiTapeConfiguration(
            state="q_accept",
            tapes=["aa", "01"],
            head_positions=[0, 1],
            step_count=5,
            is_accepting=True,
        )

        self.assertTrue(accepting_config.is_halting)

    def test_multitape_configuration_get_tape_symbol_at_head(self):
        """Test de récupération de symbole sous une tête."""
        config = MultiTapeConfiguration(
            state="q0", tapes=["aa", "01"], head_positions=[0, 1], step_count=0
        )

        # Symbole valide
        symbol = config.get_tape_symbol_at_head(0)
        self.assertEqual(symbol, "a")

        symbol = config.get_tape_symbol_at_head(1)
        self.assertEqual(symbol, "1")

        # Position invalide - retourne symbole blanc
        config_invalid = MultiTapeConfiguration(
            state="q0", tapes=["aa", "01"], head_positions=[5, 5], step_count=0
        )

        symbol = config_invalid.get_tape_symbol_at_head(0)
        self.assertEqual(symbol, "B")

        # Index de bande invalide
        with self.assertRaises(IndexError):
            config.get_tape_symbol_at_head(2)

    def test_multitape_configuration_get_all_tape_symbols_at_heads(self):
        """Test de récupération de tous les symboles sous les têtes."""
        config = MultiTapeConfiguration(
            state="q0", tapes=["aa", "01"], head_positions=[0, 1], step_count=0
        )

        symbols = config.get_all_tape_symbols_at_heads()
        self.assertEqual(symbols, ["a", "1"])

    def test_multitape_configuration_to_dict(self):
        """Test de conversion en dictionnaire."""
        config = MultiTapeConfiguration(
            state="q0",
            tapes=["aa", "01"],
            head_positions=[0, 1],
            step_count=5,
            is_accepting=True,
        )

        config_dict = config.to_dict()
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict["state"], "q0")
        self.assertEqual(config_dict["tapes"], ["aa", "01"])
        self.assertEqual(config_dict["head_positions"], [0, 1])
        self.assertEqual(config_dict["step_count"], 5)
        self.assertTrue(config_dict["is_accepting"])
        self.assertFalse(config_dict["is_rejecting"])
        self.assertEqual(config_dict["tape_count"], 2)
        self.assertTrue(config_dict["is_halting"])

    def test_multitape_configuration_string_representations(self):
        """Test des représentations textuelles."""
        config = MultiTapeConfiguration(
            state="q0", tapes=["aa", "01"], head_positions=[0, 1], step_count=5
        )

        str_repr = str(config)
        self.assertIn("MultiTapeConfig", str_repr)
        self.assertIn("q0", str_repr)
        self.assertIn("RUNNING", str_repr)

        repr_str = repr(config)
        self.assertIn("MultiTapeConfiguration", repr_str)
        self.assertIn("q0", repr_str)


class TestTapeHead(unittest.TestCase):
    """Tests pour la classe TapeHead."""

    def test_tape_head_construction(self):
        """Test de construction d'une tête."""
        head = TapeHead(tape_id=0, position=5)

        self.assertEqual(head.tape_id, 0)
        self.assertEqual(head.position, 5)

    def test_tape_head_default_position(self):
        """Test de position par défaut."""
        head = TapeHead(tape_id=1)

        self.assertEqual(head.tape_id, 1)
        self.assertEqual(head.position, 0)

    def test_tape_head_move(self):
        """Test de déplacement de tête."""
        head = TapeHead(tape_id=0, position=5)

        # Déplacement à droite
        head.move(TapeDirection.RIGHT)
        self.assertEqual(head.position, 6)

        # Déplacement à gauche
        head.move(TapeDirection.LEFT)
        self.assertEqual(head.position, 5)

        # Rester sur place
        head.move(TapeDirection.STAY)
        self.assertEqual(head.position, 5)

    def test_tape_head_equality(self):
        """Test d'égalité entre têtes."""
        head1 = TapeHead(tape_id=0, position=5)
        head2 = TapeHead(tape_id=0, position=5)
        head3 = TapeHead(tape_id=1, position=5)
        head4 = TapeHead(tape_id=0, position=6)

        self.assertEqual(head1, head2)
        self.assertNotEqual(head1, head3)
        self.assertNotEqual(head1, head4)

    def test_tape_head_hash(self):
        """Test de hash des têtes."""
        head1 = TapeHead(tape_id=0, position=5)
        head2 = TapeHead(tape_id=0, position=5)
        head3 = TapeHead(tape_id=1, position=5)

        self.assertEqual(hash(head1), hash(head2))
        self.assertNotEqual(hash(head1), hash(head3))

    def test_tape_head_repr(self):
        """Test de représentation textuelle."""
        head = TapeHead(tape_id=0, position=5)

        repr_str = repr(head)
        self.assertIn("TapeHead", repr_str)
        self.assertIn("tape_id=0", repr_str)
        self.assertIn("position=5", repr_str)


if __name__ == "__main__":
    unittest.main()


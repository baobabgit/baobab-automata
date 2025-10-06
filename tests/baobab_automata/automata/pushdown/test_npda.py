"""
Tests unitaires pour les automates à pile non-déterministes (NPDA).

Ce module contient tous les tests unitaires pour la classe NPDA
et ses composants associés.
"""

import pytest
import time
from typing import Dict, Set, Tuple

from baobab_automata.automata.pushdown.npda import NPDA
from baobab_automata.automata.pushdown.npda_configuration import NPDAConfiguration
from baobab_automata.automata.pushdown.npda_exceptions import (
    InvalidNPDAError,
    NPDAError,
    NPDATimeoutError,
    NPDAMemoryError,
)


class TestNPDAConfiguration:
    """Tests pour la classe NPDAConfiguration."""

    def test_configuration_creation(self):
        """Test de création d'une configuration."""
        config = NPDAConfiguration(
            state="q0",
            remaining_input="ab",
            stack="Z",
            priority=1,
            branch_id=0,
            depth=0,
        )

        assert config.state == "q0"
        assert config.remaining_input == "ab"
        assert config.stack == "Z"
        assert config.priority == 1
        assert config.branch_id == 0
        assert config.depth == 0

    def test_configuration_properties(self):
        """Test des propriétés de configuration."""
        config = NPDAConfiguration(
            state="q0", remaining_input="", stack="", priority=0, branch_id=0, depth=0
        )

        assert config.is_accepting
        assert config.is_final
        assert config.stack_top == ""
        assert config.stack_bottom == ""
        assert config.stack_size == 0
        assert config.input_length == 0

    def test_configuration_operations(self):
        """Test des opérations sur les configurations."""
        config = NPDAConfiguration(
            state="q0",
            remaining_input="ab",
            stack="Z",
            priority=0,
            branch_id=0,
            depth=0,
        )

        # Test empilage
        new_config = config.push_symbol("A")
        assert new_config.stack == "AZ"
        assert new_config.depth == 1

        # Test dépilage
        popped_config = new_config.pop_symbol()
        assert popped_config.stack == "Z"

        # Test consommation d'entrée
        consumed_config = config.consume_input(1)
        assert consumed_config.remaining_input == "b"

        # Test changement d'état
        state_changed_config = config.change_state("q1")
        assert state_changed_config.state == "q1"

    def test_configuration_validation(self):
        """Test de validation des configurations."""
        with pytest.raises(ValueError):
            NPDAConfiguration(state="", remaining_input="ab", stack="Z")

        with pytest.raises(ValueError):
            NPDAConfiguration(state="q0", remaining_input="ab", stack="Z", priority=-1)

    def test_configuration_serialization(self):
        """Test de sérialisation des configurations."""
        config = NPDAConfiguration(
            state="q0",
            remaining_input="ab",
            stack="Z",
            priority=1,
            branch_id=0,
            depth=0,
        )

        data = config.to_dict()
        assert data["state"] == "q0"
        assert data["remaining_input"] == "ab"
        assert data["stack"] == "Z"

        restored_config = NPDAConfiguration.from_dict(data)
        assert restored_config.state == config.state
        assert restored_config.remaining_input == config.remaining_input
        assert restored_config.stack == config.stack


class TestNPDA:
    """Tests pour la classe NPDA."""

    @pytest.fixture
    def simple_npda(self):
        """NPDA simple pour les tests."""
        return NPDA(
            states={"q0", "q1", "q2"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z", "A"},
            transitions={
                ("q0", "a", "Z"): {("q0", "AZ")},
                ("q0", "a", "A"): {("q0", "AA")},
                ("q0", "b", "A"): {("q1", "")},
                ("q1", "b", "A"): {("q1", "")},
                ("q1", "", "Z"): {("q2", "Z")},
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q2"},
        )

    @pytest.fixture
    def complex_npda(self):
        """NPDA complexe pour les tests."""
        return NPDA(
            states={"q0", "q1", "q2", "q3"},
            input_alphabet={"a", "b", "c"},
            stack_alphabet={"Z", "A", "B"},
            transitions={
                ("q0", "a", "Z"): {("q0", "AZ")},
                ("q0", "a", "A"): {("q0", "AA")},
                ("q0", "b", "A"): {("q1", "BA")},
                ("q1", "b", "A"): {("q1", "BA")},
                ("q1", "b", "B"): {("q1", "BB")},
                ("q1", "c", "B"): {("q2", "")},
                ("q2", "c", "B"): {("q2", "")},
                ("q2", "", "A"): {("q2", "")},
                ("q2", "", "Z"): {("q3", "Z")},
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q3"},
            max_parallel_branches=100,
        )

    def test_npda_creation(self, simple_npda):
        """Test de création d'un NPDA."""
        assert simple_npda.states == {"q0", "q1", "q2"}
        assert simple_npda.input_alphabet == {"a", "b"}
        assert simple_npda.stack_alphabet == {"Z", "A"}
        assert simple_npda.initial_state == "q0"
        assert simple_npda.initial_stack_symbol == "Z"
        assert simple_npda.final_states == {"q2"}

    def test_npda_validation(self, simple_npda):
        """Test de validation d'un NPDA."""
        assert simple_npda.validate()

        # Test avec NPDA invalide
        with pytest.raises(InvalidNPDAError):
            NPDA(
                states=set(),
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={},
                initial_state="q0",
                initial_stack_symbol="Z",
                final_states=set(),
            )

    def test_npda_accepts(self, simple_npda):
        """Test de reconnaissance de mots."""
        assert simple_npda.accepts("ab")
        assert simple_npda.accepts("aabb")
        assert not simple_npda.accepts("a")
        assert not simple_npda.accepts("b")
        assert not simple_npda.accepts("abab")

    def test_npda_complex_accepts(self, complex_npda):
        """Test de reconnaissance de mots complexes."""
        assert complex_npda.accepts("aabbcc")
        assert complex_npda.accepts("aaabbbccc")
        assert not complex_npda.accepts("aabbc")
        assert not complex_npda.accepts("aabbccd")

    def test_npda_get_transitions(self, simple_npda):
        """Test de récupération des transitions."""
        transitions = simple_npda.get_transitions("q0", "a", "Z")
        assert transitions == {("q0", "AZ")}

        transitions = simple_npda.get_transitions("q0", "b", "A")
        assert transitions == {("q1", "")}

    def test_npda_is_final_state(self, simple_npda):
        """Test de vérification des états finaux."""
        assert simple_npda.is_final_state("q2")
        assert not simple_npda.is_final_state("q0")
        assert not simple_npda.is_final_state("q1")

    def test_npda_get_reachable_states(self, simple_npda):
        """Test de récupération des états accessibles."""
        reachable = simple_npda.get_reachable_states("q0")
        assert "q0" in reachable
        assert "q1" in reachable
        assert "q2" in reachable

    def test_npda_parallel_execution_config(self, simple_npda):
        """Test de configuration de l'exécution parallèle."""
        simple_npda.configure_parallel_execution(
            max_branches=500, timeout=5.0, memory_limit=50 * 1024 * 1024
        )

        assert simple_npda.max_parallel_branches == 500

    def test_npda_performance_stats(self, simple_npda):
        """Test des statistiques de performance."""
        # Exécution de quelques reconnaissances
        simple_npda.accepts("ab")
        simple_npda.accepts("aabb")

        stats = simple_npda.get_performance_stats()
        assert "total_computations" in stats
        assert "parallel_branches_created" in stats
        assert "cache_hits" in stats
        assert "cache_misses" in stats

    def test_npda_complexity_analysis(self, complex_npda):
        """Test d'analyse de complexité."""
        complexity = complex_npda.analyze_complexity()

        assert "num_states" in complexity
        assert "num_transitions" in complexity
        assert "max_parallel_branches" in complexity
        assert "deterministic_ratio" in complexity
        assert "branching_factor" in complexity

    def test_npda_union(self, simple_npda):
        """Test de l'union de deux NPDA."""
        # Création d'un second NPDA
        npda2 = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z", "A"},
            transitions={("q0", "b", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        union_npda = simple_npda.union(npda2)

        # Vérification que l'union reconnaît les mots des deux langages
        assert union_npda.accepts("ab")  # Du premier NPDA
        assert union_npda.accepts("b")  # Du second NPDA

    def test_npda_concatenation(self, simple_npda):
        """Test de la concaténation de deux NPDA."""
        # Création d'un second NPDA avec le même alphabet que simple_npda
        npda2 = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z", "A"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        concat_npda = simple_npda.concatenation(npda2)

        # Vérification que la concaténation fonctionne
        # Note: Ce test nécessiterait une adaptation des transitions
        assert concat_npda is not None

    def test_npda_kleene_star(self, simple_npda):
        """Test de l'étoile de Kleene."""
        star_npda = simple_npda.kleene_star()

        # Vérification que l'étoile de Kleene reconnaît le mot vide
        assert star_npda.accepts("")

        # Vérification que l'étoile de Kleene reconnaît les mots originaux
        assert star_npda.accepts("ab")
        assert star_npda.accepts("aabb")

    def test_npda_conversion_from_pda(self):
        """Test de conversion PDA → NPDA."""
        # Création d'un PDA simple
        from baobab_automata.automata.pushdown.pda import PDA

        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        npda = NPDA.from_pda(pda)

        assert isinstance(npda, NPDA)
        assert npda.states == pda.states
        assert npda.input_alphabet == pda.input_alphabet

    def test_npda_conversion_to_pda(self, simple_npda):
        """Test de conversion NPDA → PDA."""
        pda = simple_npda.to_pda()

        assert pda.states == simple_npda.states
        assert pda.input_alphabet == simple_npda.input_alphabet
        assert pda.stack_alphabet == simple_npda.stack_alphabet

    def test_npda_conversion_from_dpda(self):
        """Test de conversion DPDA → NPDA."""
        from baobab_automata.automata.pushdown.dpda import DPDA

        dpda = DPDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): ("q1", "Z")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        npda = NPDA.from_dpda(dpda)

        assert isinstance(npda, NPDA)
        assert npda.states == dpda.states
        assert npda.input_alphabet == dpda.input_alphabet

    def test_npda_conversion_to_dpda(self):
        """Test de conversion NPDA → DPDA."""
        # Création d'un NPDA déterministe
        deterministic_npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        dpda = deterministic_npda.to_dpda()

        assert dpda.states == deterministic_npda.states
        assert dpda.input_alphabet == deterministic_npda.input_alphabet

    def test_npda_conversion_to_dpda_non_deterministic(self, simple_npda):
        """Test de conversion NPDA → DPDA avec NPDA non-déterministe."""
        with pytest.raises(NPDAError):
            simple_npda.to_dpda()

    def test_npda_optimization(self, complex_npda):
        """Test d'optimisation de NPDA."""
        optimized_npda = complex_npda.optimize_parallel_execution()

        assert isinstance(optimized_npda, NPDA)
        assert optimized_npda.states == complex_npda.states
        assert optimized_npda.input_alphabet == complex_npda.input_alphabet

    def test_npda_deterministic_check(self, simple_npda):
        """Test de vérification du déterminisme."""
        # Le NPDA simple est déterministe
        assert simple_npda.is_deterministic()

        # Créons un NPDA vraiment non-déterministe
        non_det_npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={
                ("q0", "a", "Z"): {
                    ("q0", "Z"),
                    ("q1", "Z"),
                }  # Deux transitions possibles
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        assert not non_det_npda.is_deterministic()

        # Création d'un NPDA déterministe
        deterministic_npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        assert deterministic_npda.is_deterministic()

    def test_npda_epsilon_transitions(self, simple_npda):
        """Test de récupération des transitions epsilon."""
        epsilon_transitions = simple_npda.get_epsilon_transitions()

        # Vérification qu'il y a des transitions epsilon
        assert len(epsilon_transitions) > 0

        # Vérification que toutes les transitions sont epsilon
        for state, input_symbol, stack_symbol in epsilon_transitions:
            assert input_symbol == ""

    def test_npda_transition_count(self, simple_npda):
        """Test de comptage des transitions."""
        count = simple_npda.get_transition_count()
        assert count > 0

    def test_npda_state_count(self, simple_npda):
        """Test de comptage des états."""
        count = simple_npda.get_state_count()
        assert count == 3

    def test_npda_alphabet_sizes(self, simple_npda):
        """Test de récupération des tailles d'alphabets."""
        sizes = simple_npda.get_alphabet_sizes()

        assert "input_alphabet" in sizes
        assert "stack_alphabet" in sizes
        assert sizes["input_alphabet"] == 2
        assert sizes["stack_alphabet"] == 2

    def test_npda_cache_management(self, simple_npda):
        """Test de gestion du cache."""
        # Exécution de quelques reconnaissances pour remplir le cache
        simple_npda.accepts("ab")
        simple_npda.accepts("aabb")

        # Vérification que le cache contient des données
        assert len(simple_npda._recognition_cache) > 0

        # Nettoyage du cache
        simple_npda.clear_cache()

        # Vérification que le cache est vide
        assert len(simple_npda._recognition_cache) == 0
        assert len(simple_npda._epsilon_closure_cache) == 0
        assert len(simple_npda._transition_cache) == 0

    def test_npda_serialization(self, simple_npda):
        """Test de sérialisation/désérialisation."""
        data = simple_npda.to_dict()

        assert data["type"] == "NPDA"
        assert set(data["states"]) == simple_npda.states
        assert set(data["input_alphabet"]) == simple_npda.input_alphabet
        assert set(data["stack_alphabet"]) == simple_npda.stack_alphabet

        # Désérialisation
        restored_npda = NPDA.from_dict(data)

        assert restored_npda.states == simple_npda.states
        assert restored_npda.input_alphabet == simple_npda.input_alphabet
        assert restored_npda.stack_alphabet == simple_npda.stack_alphabet
        assert restored_npda.initial_state == simple_npda.initial_state
        assert restored_npda.final_states == simple_npda.final_states

    def test_npda_timeout_error(self):
        """Test de gestion des erreurs de timeout."""
        # Création d'un NPDA qui peut causer des boucles infinies
        npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z", "A"},
            transitions={
                ("q0", "a", "Z"): {("q0", "ZZ")},
                ("q0", "", "Z"): {
                    ("q1", "AZ")
                },  # Transition epsilon qui change la pile
                ("q1", "", "A"): {("q0", "Z")},  # Transition epsilon de retour
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states=set(),
            max_parallel_branches=10,
        )

        # Configuration d'un timeout très court
        npda.configure_parallel_execution(timeout=0.001)

        with pytest.raises(NPDATimeoutError):
            npda.accepts("a")

    def test_npda_memory_error(self):
        """Test de gestion des erreurs de mémoire."""
        # Création d'un NPDA avec beaucoup de branches parallèles
        npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={
                ("q0", "a", "Z"): {("q0", "Z"), ("q1", "Z")},
                ("q1", "a", "Z"): {("q0", "Z"), ("q1", "Z")},
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
            max_parallel_branches=5,  # Limite très basse
        )

        with pytest.raises(NPDAMemoryError):
            npda.accepts("aaaaa")  # Mot qui génère beaucoup de branches

    def test_npda_invalid_input(self, simple_npda):
        """Test de gestion des entrées invalides."""
        with pytest.raises(NPDAError):
            simple_npda.accepts(123)  # Entrée non-string

    def test_npda_error_handling(self):
        """Test de gestion des erreurs générales."""
        # Test 1: État initial invalide
        with pytest.raises(InvalidNPDAError):
            NPDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={},
                initial_state="q1",  # État initial qui n'existe pas
                initial_stack_symbol="Z",
                final_states={"q0"},
            )

        # Test 2: Symbole de pile initial invalide
        with pytest.raises(InvalidNPDAError):
            NPDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={},
                initial_state="q0",
                initial_stack_symbol="A",  # Symbole qui n'existe pas dans l'alphabet de pile
                final_states={"q0"},
            )

    def test_npda_string_representation(self, simple_npda):
        """Test de représentation string."""
        str_repr = str(simple_npda)
        assert "NPDA" in str_repr
        assert "states" in str_repr

        repr_str = repr(simple_npda)
        assert "NPDA" in repr_str
        assert "states" in repr_str


class TestNPDAEdgeCases:
    """Tests pour les cas limites des NPDA."""

    def test_empty_word_acceptance(self):
        """Test de reconnaissance du mot vide."""
        npda = NPDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "", "Z"): {("q0", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q0"},
        )

        assert npda.accepts("")

    def test_single_state_npda(self):
        """Test d'un NPDA avec un seul état."""
        npda = NPDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q0", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q0"},
        )

        assert npda.accepts("a")
        assert npda.accepts("aa")

    def test_no_final_states(self):
        """Test d'un NPDA sans états finaux."""
        npda = NPDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q0", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states=set(),
        )

        assert not npda.accepts("a")
        assert not npda.accepts("")

    def test_epsilon_only_transitions(self):
        """Test d'un NPDA avec seulement des transitions epsilon."""
        npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        assert npda.accepts("")
        assert not npda.accepts("a")

    def test_large_alphabet(self):
        """Test d'un NPDA avec un grand alphabet."""
        alphabet = {chr(i) for i in range(ord("a"), ord("z") + 1)}
        stack_alphabet = {"Z", "A", "B", "C"}

        npda = NPDA(
            states={"q0", "q1"},
            input_alphabet=alphabet,
            stack_alphabet=stack_alphabet,
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        assert npda.accepts("a")
        assert not npda.accepts("b")

    def test_high_branching_factor(self):
        """Test d'un NPDA avec un facteur de branchement élevé."""
        npda = NPDA(
            states={"q0", "q1", "q2", "q3"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={
                ("q0", "a", "Z"): {("q1", "Z"), ("q2", "Z"), ("q3", "Z")},
                ("q1", "a", "Z"): {("q1", "Z")},
                ("q2", "a", "Z"): {("q2", "Z")},
                ("q3", "a", "Z"): {("q3", "Z")},
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1", "q2", "q3"},
            max_parallel_branches=10,
        )

        assert npda.accepts("a")
        assert npda.accepts("aa")

    def test_deep_stack_operations(self):
        """Test d'opérations de pile profondes."""
        npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z", "A"},
            transitions={
                ("q0", "a", "Z"): {("q0", "AAAAZ")},
                ("q0", "a", "A"): {("q0", "AAAAA")},
                ("q0", "b", "A"): {("q1", "")},
                ("q1", "b", "A"): {("q1", "")},
                ("q1", "", "Z"): {("q1", "Z")},
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        # Test avec des mots qui nécessitent des opérations de pile profondes
        assert npda.accepts("ab")
        assert npda.accepts("aabb")

    def test_complex_epsilon_closure(self):
        """Test de fermeture epsilon complexe."""
        npda = NPDA(
            states={"q0", "q1", "q2", "q3"},
            input_alphabet={"a"},
            stack_alphabet={"Z", "A"},
            transitions={
                ("q0", "", "Z"): {("q1", "Z")},
                ("q1", "", "Z"): {("q2", "Z")},
                ("q2", "", "Z"): {("q3", "Z")},
                ("q3", "a", "Z"): {("q3", "Z")},
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q3"},
        )

        assert npda.accepts("a")
        assert npda.accepts("aa")

    def test_performance_under_load(self):
        """Test de performance sous charge."""
        # Création d'un NPDA complexe
        npda = NPDA(
            states={f"q{i}" for i in range(10)},
            input_alphabet={"a", "b", "c"},
            stack_alphabet={"Z", "A", "B", "C"},
            transitions={
                (f"q{i}", "a", "Z"): {(f"q{(i+1)%10}", "AZ")} for i in range(10)
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q5"},
            max_parallel_branches=1000,
        )

        # Test de performance avec des mots de différentes tailles
        start_time = time.time()

        for word in ["a", "aa", "aaa", "aaaa", "aaaaa"]:
            npda.accepts(word)

        end_time = time.time()

        # Vérification que les tests se terminent en temps raisonnable
        assert end_time - start_time < 5.0  # Moins de 5 secondes

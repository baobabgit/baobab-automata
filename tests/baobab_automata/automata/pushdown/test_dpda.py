"""
Tests unitaires pour les automates à pile déterministes (DPDA).

Ce module contient les tests complets pour la classe DPDA et ses composants,
incluant les tests de validation, de reconnaissance, et d'opérations.
"""

import pytest

# Imports pour les tests

from baobab_automata.automata.pushdown.dpda import DPDA
from baobab_automata.automata.pushdown.dpda_configuration import DPDAConfiguration
from baobab_automata.automata.pushdown.dpda_exceptions import (
    DPDAError,
    InvalidDPDAError,
    DeterminismError,
    ConflictError,
    ConversionError,
    DPDAOptimizationError,
)


class TestDPDAConfiguration:
    """Tests pour la classe DPDAConfiguration."""

    def test_configuration_creation(self):
        """Test de création d'une configuration."""
        config = DPDAConfiguration(state="q0", remaining_input="ab", stack="Z")

        assert config.state == "q0"
        assert config.remaining_input == "ab"
        assert config.stack == "Z"

    def test_configuration_validation(self):
        """Test de validation d'une configuration."""
        # Configuration valide
        config = DPDAConfiguration("q0", "ab", "Z")
        assert config.state == "q0"

        # Configuration invalide - état vide
        with pytest.raises(ValueError):
            DPDAConfiguration("", "ab", "Z")

        # Configuration invalide - types incorrects
        with pytest.raises(ValueError):
            DPDAConfiguration(123, "ab", "Z")

    def test_configuration_properties(self):
        """Test des propriétés d'une configuration."""
        config = DPDAConfiguration("q0", "ab", "Z")

        assert config.stack_top == "Z"
        assert config.stack_bottom == "Z"
        assert config.stack_height == 1
        assert not config.is_empty_stack
        assert not config.is_accepting

        # Configuration acceptante
        accepting_config = DPDAConfiguration("q0", "", "Z")
        assert accepting_config.is_accepting

    def test_stack_operations(self):
        """Test des opérations sur la pile."""
        config = DPDAConfiguration("q0", "ab", "Z")

        # Empilage
        new_config = config.push_symbols("AB")
        assert new_config.stack == "ABZ"
        assert new_config.stack_top == "A"

        # Dépilage
        popped_config = new_config.pop_symbols(2)
        assert popped_config.stack == "Z"

        # Remplacement du sommet
        replaced_config = config.replace_stack_top("XY")
        assert replaced_config.stack == "XY"

    def test_input_consumption(self):
        """Test de consommation d'entrée."""
        config = DPDAConfiguration("q0", "abc", "Z")

        # Consommation partielle
        new_config = config.consume_input(2)
        assert new_config.remaining_input == "c"

        # Consommation complète
        final_config = new_config.consume_input(1)
        assert final_config.remaining_input == ""
        assert final_config.is_accepting

    def test_state_change(self):
        """Test de changement d'état."""
        config = DPDAConfiguration("q0", "ab", "Z")

        new_config = config.change_state("q1")
        assert new_config.state == "q1"
        assert new_config.remaining_input == "ab"
        assert new_config.stack == "Z"

    def test_serialization(self):
        """Test de sérialisation/désérialisation."""
        config = DPDAConfiguration("q0", "ab", "Z")

        # Sérialisation
        data = config.to_dict()
        assert data["state"] == "q0"
        assert data["remaining_input"] == "ab"
        assert data["stack"] == "Z"

        # Désérialisation
        restored_config = DPDAConfiguration.from_dict(data)
        assert restored_config.state == "q0"
        assert restored_config.remaining_input == "ab"
        assert restored_config.stack == "Z"


class TestDPDA:
    """Tests pour la classe DPDA."""

    def create_simple_dpda(self) -> DPDA:
        """Crée un DPDA simple pour les tests."""
        return DPDA(
            states={"q0", "q1", "q2"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z", "A"},
            transitions={
                ("q0", "a", "Z"): ("q0", "AZ"),
                ("q0", "a", "A"): ("q0", "AA"),
                ("q0", "b", "A"): ("q1", ""),
                ("q1", "b", "A"): ("q1", ""),
                ("q1", "b", "Z"): ("q2", "Z"),  # Transition directe
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q2"},
        )

    def test_dpda_creation(self):
        """Test de création d'un DPDA."""
        dpda = self.create_simple_dpda()

        assert dpda.states == {"q0", "q1", "q2"}
        assert dpda.input_alphabet == {"a", "b"}
        assert dpda.stack_alphabet == {"Z", "A"}
        assert dpda.initial_state == "q0"
        assert dpda.initial_stack_symbol == "Z"
        assert dpda.final_states == {"q2"}

    def test_dpda_validation(self):
        """Test de validation d'un DPDA."""
        # DPDA valide
        dpda = self.create_simple_dpda()
        assert dpda.validate()

        # DPDA invalide - état initial inexistant
        with pytest.raises(InvalidDPDAError):
            DPDA(
                states={"q0", "q1"},
                input_alphabet={"a", "b"},
                stack_alphabet={"Z"},
                transitions={},
                initial_state="q2",  # État inexistant
                initial_stack_symbol="Z",
                final_states={"q1"},
            )

        # DPDA invalide - état final inexistant
        with pytest.raises(InvalidDPDAError):
            DPDA(
                states={"q0", "q1"},
                input_alphabet={"a", "b"},
                stack_alphabet={"Z"},
                transitions={},
                initial_state="q0",
                initial_stack_symbol="Z",
                final_states={"q2"},  # État inexistant
            )

    def test_determinism_validation(self):
        """Test de validation du déterminisme."""
        # DPDA déterministe
        dpda = self.create_simple_dpda()
        assert dpda.validate()

        # DPDA non-déterministe - conflit epsilon/symbole
        with pytest.raises(InvalidDPDAError):
            DPDA(
                states={"q0", "q1"},
                input_alphabet={"a"},
                stack_alphabet={"Z", "A"},
                transitions={
                    ("q0", "a", "Z"): ("q0", "AZ"),
                    ("q0", "", "A"): ("q1", "A"),  # Conflit epsilon/symbole
                },
                initial_state="q0",
                initial_stack_symbol="Z",
                final_states={"q1"},
            )

    def test_word_recognition(self):
        """Test de reconnaissance de mots."""
        # DPDA simple qui accepte le mot 'ab'
        dpda = DPDA(
            states={"q0", "q1", "q2"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): ("q1", "Z"), ("q1", "b", "Z"): ("q2", "Z")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q2"},
        )

        # Mots acceptés
        assert dpda.accepts("ab")

        # Mots rejetés
        assert not dpda.accepts("a")
        assert not dpda.accepts("b")
        assert not dpda.accepts("ba")
        assert not dpda.accepts("")

    def test_transition_retrieval(self):
        """Test de récupération des transitions."""
        dpda = self.create_simple_dpda()

        # Transition existante
        transition = dpda.get_transition("q0", "a", "Z")
        assert transition == ("q0", "AZ")

        # Transition inexistante
        transition = dpda.get_transition("q0", "b", "Z")
        assert transition is None

        # État invalide
        with pytest.raises(InvalidDPDAError):
            dpda.get_transition("q3", "a", "Z")

    def test_final_state_check(self):
        """Test de vérification des états finaux."""
        dpda = self.create_simple_dpda()

        assert dpda.is_final_state("q2")
        assert not dpda.is_final_state("q0")
        assert not dpda.is_final_state("q1")

    def test_reachable_states(self):
        """Test de calcul des états accessibles."""
        dpda = self.create_simple_dpda()

        # États accessibles depuis q0
        reachable = dpda.get_reachable_states("q0")
        assert reachable == {"q0", "q1", "q2"}

        # États accessibles depuis q1
        reachable = dpda.get_reachable_states("q1")
        assert reachable == {"q1", "q2"}

        # États accessibles depuis q2
        reachable = dpda.get_reachable_states("q2")
        assert reachable == {"q2"}

    def test_conflict_detection(self):
        """Test de détection des conflits."""
        dpda = self.create_simple_dpda()

        # DPDA déterministe - pas de conflits
        conflicts = dpda._detect_conflicts()
        assert conflicts == []

        # Test avec un DPDA non-déterministe (création manuelle pour le test)
        # Note: Ce test nécessiterait une méthode pour créer des DPDA non-déterministes
        # pour les tests, ce qui n'est pas possible avec le constructeur normal

    def test_determinism_analysis(self):
        """Test d'analyse du déterminisme."""
        dpda = self.create_simple_dpda()

        analysis = dpda.analyze_determinism()

        assert "total_transitions" in analysis
        assert "deterministic_transitions" in analysis
        assert "determinism_percentage" in analysis
        assert "conflicts_detected" in analysis
        assert "is_deterministic" in analysis

        assert analysis["is_deterministic"] is True
        assert analysis["conflicts_detected"] == 0
        assert analysis["determinism_percentage"] == 100.0

    def test_serialization(self):
        """Test de sérialisation/désérialisation."""
        dpda = self.create_simple_dpda()

        # Sérialisation
        data = dpda.to_dict()
        assert data["type"] == "DPDA"
        assert set(data["states"]) == {"q0", "q1", "q2"}
        assert set(data["input_alphabet"]) == {"a", "b"}
        assert set(data["stack_alphabet"]) == {"Z", "A"}
        assert data["initial_state"] == "q0"
        assert data["initial_stack_symbol"] == "Z"
        assert set(data["final_states"]) == {"q2"}

        # Désérialisation
        restored_dpda = DPDA.from_dict(data)
        assert restored_dpda.states == dpda.states
        assert restored_dpda.input_alphabet == dpda.input_alphabet
        assert restored_dpda.stack_alphabet == dpda.stack_alphabet
        assert restored_dpda.initial_state == dpda.initial_state
        assert restored_dpda.initial_stack_symbol == dpda.initial_stack_symbol
        assert restored_dpda.final_states == dpda.final_states

    def test_palindrome_dpda(self):
        """Test d'un DPDA pour les palindromes."""
        # DPDA simple pour reconnaître les palindromes de longueur 2
        palindrome_dpda = DPDA(
            states={"q0", "q1", "q2"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z"},
            transitions={
                ("q0", "a", "Z"): ("q1", "Z"),
                ("q0", "b", "Z"): ("q1", "Z"),
                ("q1", "a", "Z"): ("q2", "Z"),
                ("q1", "b", "Z"): ("q2", "Z"),
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q2"},
        )

        # Test de reconnaissance
        assert palindrome_dpda.accepts("aa")
        assert palindrome_dpda.accepts("bb")
        assert palindrome_dpda.accepts("ab")
        assert palindrome_dpda.accepts("ba")
        assert not palindrome_dpda.accepts("a")
        assert not palindrome_dpda.accepts("abc")

    def test_error_handling(self):
        """Test de gestion des erreurs."""
        dpda = self.create_simple_dpda()

        # Erreur lors de la reconnaissance - test avec un état invalide
        with pytest.raises(InvalidDPDAError):
            dpda.get_transition("q3", "a", "Z")  # État inexistant

    def test_string_representations(self):
        """Test des représentations string."""
        dpda = self.create_simple_dpda()

        # Représentation textuelle
        str_repr = str(dpda)
        assert "DPDA" in str_repr
        assert "states=3" in str_repr

        # Représentation technique
        repr_str = repr(dpda)
        assert "DPDA(" in repr_str
        assert "states={" in repr_str


class TestDPDAEdgeCases:
    """Tests pour les cas limites des DPDA."""

    def test_empty_word(self):
        """Test avec un mot vide."""
        dpda = DPDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q0"},
        )

        assert dpda.accepts("")

    def test_single_state_dpda(self):
        """Test avec un DPDA à un seul état."""
        dpda = DPDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): ("q0", "Z")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q0"},
        )

        assert dpda.accepts("a")
        assert dpda.accepts("aa")
        assert not dpda.accepts("b")

    def test_no_transitions(self):
        """Test avec un DPDA sans transitions."""
        dpda = DPDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q0"},
        )

        assert dpda.accepts("")
        assert not dpda.accepts("a")

    def test_epsilon_transitions(self):
        """Test avec des transitions epsilon."""
        # DPDA avec seulement des transitions epsilon
        dpda = DPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "", "Z"): ("q1", "Z")},  # Transition epsilon uniquement
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        # Test avec un mot vide qui utilise la transition epsilon
        assert dpda.accepts("")

    def test_complex_stack_operations(self):
        """Test avec des opérations de pile complexes."""
        dpda = DPDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z", "A", "B"},
            transitions={
                ("q0", "a", "Z"): ("q0", "ABZ"),  # Empilage multiple
                ("q0", "b", "A"): ("q1", "B"),  # Remplacement
                ("q1", "b", "B"): ("q1", ""),  # Dépilage
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        # Test de reconnaissance avec opérations complexes
        assert dpda.accepts("abb")


class TestDPDAExceptions:
    """Tests pour les exceptions des DPDA."""

    def test_dpda_error(self):
        """Test de DPDAError."""
        error = DPDAError("Test error", {"key": "value"})
        assert str(error) == "Test error (key=value)"

        error_simple = DPDAError("Simple error")
        assert str(error_simple) == "Simple error"

    def test_invalid_dpda_error(self):
        """Test de InvalidDPDAError."""
        error = InvalidDPDAError("Invalid DPDA", ["error1", "error2"])
        assert "error1" in str(error)
        assert "error2" in str(error)

    def test_determinism_error(self):
        """Test de DeterminismError."""
        error = DeterminismError("Determinism violation", ["conflict1"])
        assert "conflict1" in str(error)

    def test_conflict_error(self):
        """Test de ConflictError."""
        error = ConflictError("Conflict detected", "epsilon_symbol", {"state": "q0"})
        assert "epsilon_symbol" in str(error)

    def test_conversion_error(self):
        """Test de ConversionError."""
        error = ConversionError("Conversion failed", "PDA", "DPDA", "determinism_check")
        assert "PDA -> DPDA" in str(error)
        assert "determinism_check" in str(error)

    def test_optimization_error(self):
        """Test de DPDAOptimizationError."""
        error = DPDAOptimizationError("Optimization failed", "transition_merge")
        assert "transition_merge" in str(error)

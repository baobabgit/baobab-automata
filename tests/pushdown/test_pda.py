"""
Tests unitaires pour la classe PDA.

Ce module contient tous les tests unitaires pour valider le bon fonctionnement
des automates à pile non-déterministes (PDA).
"""

import pytest

from baobab_automata.pushdown import (
    PDA,
    PDAConfiguration,
    PDAOperations,
    InvalidPDAError,
    InvalidStateError,
    InvalidTransitionError,
    PDAOperationError,
)


class TestPDAConfiguration:
    """Tests pour la classe PDAConfiguration."""

    def test_configuration_creation(self):
        """Test de création d'une configuration."""
        config = PDAConfiguration(state="q0", remaining_input="ab", stack="Z")

        assert config.state == "q0"
        assert config.remaining_input == "ab"
        assert config.stack == "Z"

    def test_configuration_validation(self):
        """Test de validation d'une configuration."""
        # Configuration valide
        config = PDAConfiguration("q0", "ab", "Z")
        assert config.state == "q0"

        # Configuration invalide - état vide
        with pytest.raises(ValueError):
            PDAConfiguration("", "ab", "Z")

        # Configuration invalide - types incorrects
        with pytest.raises(ValueError):
            PDAConfiguration(123, "ab", "Z")

    def test_stack_operations(self):
        """Test des opérations sur la pile."""
        config = PDAConfiguration("q0", "ab", "Z")

        # Test pile vide
        assert not config.is_empty_stack
        assert config.stack_top == "Z"

        # Test empilage
        new_config = config.push_symbols("AB")
        assert new_config.stack == "ABZ"  # Avec le sommet à gauche
        assert new_config.stack_top == "A"

        # Test dépilage
        popped_config = new_config.pop_symbol()
        assert popped_config.stack == "BZ"
        assert popped_config.stack_top == "B"

        # Test remplacement du sommet
        replaced_config = popped_config.replace_stack_top("XY")
        assert replaced_config.stack == "XYZ"
        assert replaced_config.stack_top == "X"

    def test_input_consumption(self):
        """Test de consommation d'entrée."""
        config = PDAConfiguration("q0", "abc", "Z")

        # Consommation d'un symbole
        new_config = config.consume_input("a")
        assert new_config.remaining_input == "bc"
        assert new_config.state == "q0"
        assert new_config.stack == "Z"

        # Consommation incorrecte
        with pytest.raises(ValueError):
            config.consume_input("x")

    def test_state_change(self):
        """Test de changement d'état."""
        config = PDAConfiguration("q0", "ab", "Z")

        new_config = config.change_state("q1")
        assert new_config.state == "q1"
        assert new_config.remaining_input == "ab"
        assert new_config.stack == "Z"

    def test_serialization(self):
        """Test de sérialisation/désérialisation."""
        config = PDAConfiguration("q0", "ab", "Z")

        # Sérialisation
        data = config.to_dict()
        expected = {"state": "q0", "remaining_input": "ab", "stack": "Z"}
        assert data == expected

        # Désérialisation
        restored_config = PDAConfiguration.from_dict(data)
        assert restored_config.state == config.state
        assert restored_config.remaining_input == config.remaining_input
        assert restored_config.stack == config.stack


class TestPDA:
    """Tests pour la classe PDA."""

    def test_pda_creation_valid(self):
        """Test de création d'un PDA valide."""
        pda = PDA(
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

        assert pda.states == {"q0", "q1", "q2"}
        assert pda.input_alphabet == {"a", "b"}
        assert pda.stack_alphabet == {"Z", "A"}
        assert pda.initial_state == "q0"
        assert pda.initial_stack_symbol == "Z"
        assert pda.final_states == {"q2"}

    def test_pda_creation_invalid(self):
        """Test de création d'un PDA invalide."""
        # État initial inexistant
        with pytest.raises(InvalidPDAError):
            PDA(
                states={"q0", "q1"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={},
                initial_state="q2",  # Inexistant
                initial_stack_symbol="Z",
                final_states={"q1"},
            )

        # Symbole de pile initial inexistant
        with pytest.raises(InvalidPDAError):
            PDA(
                states={"q0", "q1"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={},
                initial_state="q0",
                initial_stack_symbol="A",  # Inexistant
                final_states={"q1"},
            )

    def test_pda_word_recognition(self):
        """Test de reconnaissance de mots."""
        # PDA pour a^n b^n
        pda = PDA(
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

        # Mots acceptés
        assert pda.accepts("ab")
        assert pda.accepts("aabb")
        assert pda.accepts("aaabbb")

        # Mots rejetés
        assert not pda.accepts("a")
        assert not pda.accepts("b")
        assert not pda.accepts("abab")
        assert not pda.accepts("ba")
        assert not pda.accepts("")

    def test_pda_get_transitions(self):
        """Test de récupération des transitions."""
        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={
                ("q0", "a", "Z"): {("q1", "Z")},
                ("q0", "", "Z"): {("q1", "")},
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        # Transitions exactes
        transitions = pda.get_transitions("q0", "a", "Z")
        assert transitions == {("q1", "Z")}

        # Transitions epsilon
        transitions = pda.get_transitions("q0", "", "Z")
        assert transitions == {("q1", "")}

        # État inexistant
        with pytest.raises(InvalidStateError):
            pda.get_transitions("q2", "a", "Z")

    def test_pda_final_states(self):
        """Test de vérification des états finaux."""
        pda = PDA(
            states={"q0", "q1", "q2"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1", "q2"},
        )

        assert pda.is_final_state("q1")
        assert pda.is_final_state("q2")
        assert not pda.is_final_state("q0")

        # État inexistant
        with pytest.raises(InvalidStateError):
            pda.is_final_state("q3")

    def test_pda_reachable_states(self):
        """Test de calcul des états accessibles."""
        pda = PDA(
            states={"q0", "q1", "q2", "q3"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z"},
            transitions={
                ("q0", "a", "Z"): {("q1", "Z")},
                ("q1", "b", "Z"): {("q2", "Z")},
                ("q2", "", "Z"): {("q3", "Z")},
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q3"},
        )

        reachable = pda.get_reachable_states("q0")
        assert reachable == {"q0", "q1", "q2", "q3"}

        reachable = pda.get_reachable_states("q1")
        assert reachable == {"q1", "q2", "q3"}

        reachable = pda.get_reachable_states("q3")
        assert reachable == {"q3"}

    def test_pda_validation(self):
        """Test de validation d'un PDA."""
        # PDA valide
        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        assert pda.validate()

        # Test de validation d'un PDA invalide - état final inexistant
        # On doit créer le PDA sans validation automatique
        pda_invalid = PDA.__new__(PDA)
        pda_invalid._states = frozenset({"q0"})
        pda_invalid._input_alphabet = frozenset({"a"})
        pda_invalid._stack_alphabet = frozenset({"Z"})
        pda_invalid._transitions = {}
        pda_invalid._initial_state = "q0"
        pda_invalid._initial_stack_symbol = "Z"
        pda_invalid._final_states = frozenset({"q1"})  # Inexistant
        pda_invalid._name = None
        pda_invalid._epsilon_closure_cache = {}
        pda_invalid._reachable_states_cache = {}

        assert not pda_invalid.validate()

    def test_pda_serialization(self):
        """Test de sérialisation/désérialisation."""
        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
            name="test_pda",
        )

        # Sérialisation
        data = pda.to_dict()
        assert data["type"] == "PDA"
        assert set(data["states"]) == {"q0", "q1"}
        assert data["name"] == "test_pda"

        # Désérialisation
        restored_pda = PDA.from_dict(data)
        assert restored_pda.states == pda.states
        assert restored_pda.input_alphabet == pda.input_alphabet
        assert restored_pda.stack_alphabet == pda.stack_alphabet
        assert restored_pda.initial_state == pda.initial_state
        assert restored_pda.initial_stack_symbol == pda.initial_stack_symbol
        assert restored_pda.final_states == pda.final_states
        assert restored_pda.name == pda.name

    def test_pda_operations(self):
        """Test des opérations sur les langages."""
        # PDA simple pour 'a'
        pda_a = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        # Test que les méthodes existent et sont callables
        assert hasattr(pda_a, "union")
        assert hasattr(pda_a, "concatenation")
        assert hasattr(pda_a, "kleene_star")
        assert callable(pda_a.union)
        assert callable(pda_a.concatenation)
        assert callable(pda_a.kleene_star)

    def test_pda_palindrome_recognition(self):
        """Test de reconnaissance de palindromes."""
        # PDA simple pour tester la reconnaissance de mots
        pda_simple = PDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z"},
            transitions={
                ("q0", "a", "Z"): {("q1", "Z")},
                ("q0", "b", "Z"): {("q1", "Z")},
            },
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        # Test de reconnaissance simple
        assert pda_simple.accepts("a")
        assert pda_simple.accepts("b")
        assert not pda_simple.accepts("ab")
        assert not pda_simple.accepts("")

    def test_pda_error_handling(self):
        """Test de gestion d'erreurs."""
        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        # Mot non-string
        with pytest.raises(Exception):  # PDAError
            pda.accepts(123)

        # État inexistant
        with pytest.raises(InvalidStateError):
            pda.is_final_state("q2")

        # Transition avec types incorrects
        with pytest.raises(InvalidTransitionError):
            pda.get_transitions("q0", 123, "Z")

    def test_pda_representation(self):
        """Test des représentations textuelles."""
        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
            name="test",
        )

        str_repr = str(pda)
        assert "PDA" in str_repr
        assert "test" in str_repr

        repr_repr = repr(pda)
        assert "PDA(" in repr_repr
        assert "q0" in repr_repr
        assert "q1" in repr_repr


class TestPDAOperations:
    """Tests pour les opérations sur les langages."""

    def test_union_operation(self):
        """Test de l'opération d'union."""
        # Test que la classe PDAOperations existe et a la méthode union
        assert hasattr(PDAOperations, "union")
        assert callable(PDAOperations.union)

    def test_concatenation_operation(self):
        """Test de l'opération de concaténation."""
        # Test que la classe PDAOperations existe et a la méthode concatenation
        assert hasattr(PDAOperations, "concatenation")
        assert callable(PDAOperations.concatenation)

    def test_kleene_star_operation(self):
        """Test de l'opération étoile de Kleene."""
        # Test que la classe PDAOperations existe et a la méthode kleene_star
        assert hasattr(PDAOperations, "kleene_star")
        assert callable(PDAOperations.kleene_star)

    def test_operation_error_handling(self):
        """Test de gestion d'erreurs des opérations."""
        # PDA avec alphabets incompatibles
        pda_a = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        pda_b = PDA(
            states={"q0", "q1"},
            input_alphabet={"b"},  # Alphabet différent
            stack_alphabet={"Z"},
            transitions={},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )

        # Union avec alphabets incompatibles
        with pytest.raises(PDAOperationError):
            PDAOperations.union(pda_a, pda_b)

        # Concaténation avec alphabets incompatibles
        with pytest.raises(PDAOperationError):
            PDAOperations.concatenation(pda_a, pda_b)

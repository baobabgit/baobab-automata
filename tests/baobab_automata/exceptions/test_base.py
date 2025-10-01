"""
Tests unitaires pour les exceptions de base.

Ce module teste toutes les classes d'exceptions personnalisées de la bibliothèque.
"""

from baobab_automata.exceptions import (
    BaobabAutomataError,
    InvalidAutomatonError,
    InvalidStateError,
    InvalidTransitionError,
    ConversionError,
    RecognitionError,
)


class TestBaobabAutomataError:
    """Tests pour la classe BaobabAutomataError."""

    def test_init_with_message_only(self):
        """Test de l'initialisation avec un message seulement."""
        error = BaobabAutomataError("Test error")
        assert error.message == "Test error"
        assert error.details == {}
        assert str(error) == "Test error"

    def test_init_with_message_and_details(self):
        """Test de l'initialisation avec un message et des détails."""
        details = {"key": "value", "number": 42}
        error = BaobabAutomataError("Test error", details)
        assert error.message == "Test error"
        assert error.details == details
        assert "Détails: {'key': 'value', 'number': 42}" in str(error)

    def test_inheritance(self):
        """Test que BaobabAutomataError hérite d'Exception."""
        error = BaobabAutomataError("Test")
        assert isinstance(error, Exception)


class TestInvalidAutomatonError:
    """Tests pour la classe InvalidAutomatonError."""

    def test_init_with_message_only(self):
        """Test de l'initialisation avec un message seulement."""
        error = InvalidAutomatonError("Invalid automaton")
        assert error.message == "Invalid automaton"
        assert error.automaton_type is None
        assert error.validation_errors == []

    def test_init_with_automaton_type(self):
        """Test de l'initialisation avec un type d'automate."""
        error = InvalidAutomatonError("Invalid automaton", "DFA")
        assert error.message == "Invalid automaton"
        assert error.automaton_type == "DFA"
        assert error.details["automaton_type"] == "DFA"

    def test_init_with_validation_errors(self):
        """Test de l'initialisation avec des erreurs de validation."""
        errors = ["Error 1", "Error 2"]
        error = InvalidAutomatonError("Invalid automaton", validation_errors=errors)
        assert error.message == "Invalid automaton"
        assert error.validation_errors == errors
        assert error.details["validation_errors"] == errors

    def test_inheritance(self):
        """Test que InvalidAutomatonError hérite de BaobabAutomataError."""
        error = InvalidAutomatonError("Test")
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, Exception)


class TestInvalidStateError:
    """Tests pour la classe InvalidStateError."""

    def test_init_with_message_only(self):
        """Test de l'initialisation avec un message seulement."""
        error = InvalidStateError("Invalid state")
        assert error.message == "Invalid state"
        assert error.state_identifier is None
        assert error.state_type is None

    def test_init_with_state_identifier(self):
        """Test de l'initialisation avec un identifiant d'état."""
        error = InvalidStateError("Invalid state", "q0")
        assert error.message == "Invalid state"
        assert error.state_identifier == "q0"
        assert error.details["state_identifier"] == "q0"

    def test_init_with_state_type(self):
        """Test de l'initialisation avec un type d'état."""
        error = InvalidStateError("Invalid state", state_type="INITIAL")
        assert error.message == "Invalid state"
        assert error.state_type == "INITIAL"
        assert error.details["state_type"] == "INITIAL"

    def test_inheritance(self):
        """Test que InvalidStateError hérite de BaobabAutomataError."""
        error = InvalidStateError("Test")
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, Exception)


class TestInvalidTransitionError:
    """Tests pour la classe InvalidTransitionError."""

    def test_init_with_message_only(self):
        """Test de l'initialisation avec un message seulement."""
        error = InvalidTransitionError("Invalid transition")
        assert error.message == "Invalid transition"
        assert error.source_state is None
        assert error.target_state is None
        assert error.symbol is None

    def test_init_with_states_and_symbol(self):
        """Test de l'initialisation avec des états et un symbole."""
        error = InvalidTransitionError("Invalid transition", "q0", "q1", "a")
        assert error.message == "Invalid transition"
        assert error.source_state == "q0"
        assert error.target_state == "q1"
        assert error.symbol == "a"
        assert error.details["source_state"] == "q0"
        assert error.details["target_state"] == "q1"
        assert error.details["symbol"] == "a"

    def test_inheritance(self):
        """Test que InvalidTransitionError hérite de BaobabAutomataError."""
        error = InvalidTransitionError("Test")
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, Exception)


class TestConversionError:
    """Tests pour la classe ConversionError."""

    def test_init_with_message_only(self):
        """Test de l'initialisation avec un message seulement."""
        error = ConversionError("Conversion failed")
        assert error.message == "Conversion failed"
        assert error.source_type is None
        assert error.target_type is None
        assert error.conversion_step is None

    def test_init_with_types_and_step(self):
        """Test de l'initialisation avec des types et une étape."""
        error = ConversionError("Conversion failed", "DFA", "NFA", "determinization")
        assert error.message == "Conversion failed"
        assert error.source_type == "DFA"
        assert error.target_type == "NFA"
        assert error.conversion_step == "determinization"
        assert error.details["source_type"] == "DFA"
        assert error.details["target_type"] == "NFA"
        assert error.details["conversion_step"] == "determinization"

    def test_inheritance(self):
        """Test que ConversionError hérite de BaobabAutomataError."""
        error = ConversionError("Test")
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, Exception)


class TestRecognitionError:
    """Tests pour la classe RecognitionError."""

    def test_init_with_message_only(self):
        """Test de l'initialisation avec un message seulement."""
        error = RecognitionError("Recognition failed")
        assert error.message == "Recognition failed"
        assert error.word is None
        assert error.automaton_type is None
        assert error.recognition_step is None

    def test_init_with_word_and_type(self):
        """Test de l'initialisation avec un mot et un type."""
        error = RecognitionError(
            "Recognition failed", "abc", "DFA", "symbol_processing"
        )
        assert error.message == "Recognition failed"
        assert error.word == "abc"
        assert error.automaton_type == "DFA"
        assert error.recognition_step == "symbol_processing"
        assert error.details["word"] == "abc"
        assert error.details["automaton_type"] == "DFA"
        assert error.details["recognition_step"] == "symbol_processing"

    def test_inheritance(self):
        """Test que RecognitionError hérite de BaobabAutomataError."""
        error = RecognitionError("Test")
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, Exception)

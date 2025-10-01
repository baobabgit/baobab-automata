"""
Tests unitaires pour les exceptions de Baobab Automata.

Ce module contient les tests unitaires pour toutes les exceptions
définies dans la bibliothèque.
"""

import pytest
from baobab_automata.exceptions.base import (
    BaobabAutomataError,
    InvalidAutomatonError,
    InvalidStateError,
    InvalidTransitionError,
    ConversionError,
    RecognitionError,
)


class TestBaobabAutomataError:
    """Tests pour l'exception de base BaobabAutomataError."""

    def test_basic_exception_creation(self):
        """Test la création d'une exception de base."""
        error = BaobabAutomataError("Test error message")

        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.details == {}

    def test_exception_with_details(self):
        """Test la création d'une exception avec des détails."""
        details = {"key": "value", "number": 42}
        error = BaobabAutomataError("Test error message", details)

        assert (
            str(error) == "Test error message (Détails: {'key': 'value', 'number': 42})"
        )
        assert error.message == "Test error message"
        assert error.details == details

    def test_exception_inheritance(self):
        """Test que l'exception hérite correctement d'Exception."""
        error = BaobabAutomataError("Test error message")

        assert isinstance(error, Exception)
        assert isinstance(error, BaobabAutomataError)

    def test_exception_str_representation(self):
        """Test la représentation string de l'exception."""
        # Sans détails
        error1 = BaobabAutomataError("Simple error")
        assert str(error1) == "Simple error"

        # Avec détails
        error2 = BaobabAutomataError("Complex error", {"step": "validation"})
        assert "Complex error" in str(error2)
        assert "Détails:" in str(error2)
        assert "validation" in str(error2)


class TestInvalidAutomatonError:
    """Tests pour l'exception InvalidAutomatonError."""

    def test_basic_automaton_error_creation(self):
        """Test la création d'une exception d'automate invalide."""
        error = InvalidAutomatonError("Invalid automaton")

        assert str(error) == "Invalid automaton"
        assert error.message == "Invalid automaton"
        assert error.automaton_type is None
        assert error.validation_errors == []

    def test_automaton_error_with_type(self):
        """Test la création d'une exception avec type d'automate."""
        error = InvalidAutomatonError("Invalid DFA", automaton_type="dfa")

        assert str(error) == "Invalid DFA (Détails: {'automaton_type': 'dfa'})"
        assert error.automaton_type == "dfa"
        assert error.validation_errors == []

    def test_automaton_error_with_validation_errors(self):
        """Test la création d'une exception avec erreurs de validation."""
        validation_errors = ["No initial states", "Invalid transition"]
        error = InvalidAutomatonError(
            "Invalid automaton", validation_errors=validation_errors
        )

        assert "Invalid automaton" in str(error)
        assert "Détails:" in str(error)
        assert error.validation_errors == validation_errors

    def test_automaton_error_with_all_details(self):
        """Test la création d'une exception avec tous les détails."""
        validation_errors = ["No initial states", "Invalid transition"]
        error = InvalidAutomatonError(
            "Invalid DFA", automaton_type="dfa", validation_errors=validation_errors
        )

        assert error.automaton_type == "dfa"
        assert error.validation_errors == validation_errors
        assert "dfa" in str(error)
        assert "No initial states" in str(error)

    def test_automaton_error_inheritance(self):
        """Test que l'exception hérite correctement."""
        error = InvalidAutomatonError("Test error")

        assert isinstance(error, Exception)
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, InvalidAutomatonError)


class TestInvalidStateError:
    """Tests pour l'exception InvalidStateError."""

    def test_basic_state_error_creation(self):
        """Test la création d'une exception d'état invalide."""
        error = InvalidStateError("Invalid state")

        assert str(error) == "Invalid state"
        assert error.message == "Invalid state"
        assert error.state_identifier is None
        assert error.state_type is None

    def test_state_error_with_identifier(self):
        """Test la création d'une exception avec identifiant d'état."""
        error = InvalidStateError("Invalid state", state_identifier="q0")

        assert str(error) == "Invalid state (Détails: {'state_identifier': 'q0'})"
        assert error.state_identifier == "q0"
        assert error.state_type is None

    def test_state_error_with_type(self):
        """Test la création d'une exception avec type d'état."""
        error = InvalidStateError("Invalid state", state_type="initial")

        assert str(error) == "Invalid state (Détails: {'state_type': 'initial'})"
        assert error.state_identifier is None
        assert error.state_type == "initial"

    def test_state_error_with_all_details(self):
        """Test la création d'une exception avec tous les détails."""
        error = InvalidStateError(
            "Invalid state", state_identifier="q0", state_type="initial"
        )

        assert error.state_identifier == "q0"
        assert error.state_type == "initial"
        assert "q0" in str(error)
        assert "initial" in str(error)

    def test_state_error_inheritance(self):
        """Test que l'exception hérite correctement."""
        error = InvalidStateError("Test error")

        assert isinstance(error, Exception)
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, InvalidStateError)


class TestInvalidTransitionError:
    """Tests pour l'exception InvalidTransitionError."""

    def test_basic_transition_error_creation(self):
        """Test la création d'une exception de transition invalide."""
        error = InvalidTransitionError("Invalid transition")

        assert str(error) == "Invalid transition"
        assert error.message == "Invalid transition"
        assert error.source_state is None
        assert error.target_state is None
        assert error.symbol is None

    def test_transition_error_with_states(self):
        """Test la création d'une exception avec états source et cible."""
        error = InvalidTransitionError(
            "Invalid transition", source_state="q0", target_state="q1"
        )

        assert (
            str(error)
            == "Invalid transition (Détails: {'source_state': 'q0', 'target_state': 'q1'})"
        )
        assert error.source_state == "q0"
        assert error.target_state == "q1"
        assert error.symbol is None

    def test_transition_error_with_symbol(self):
        """Test la création d'une exception avec symbole."""
        error = InvalidTransitionError("Invalid transition", symbol="a")

        assert str(error) == "Invalid transition (Détails: {'symbol': 'a'})"
        assert error.source_state is None
        assert error.target_state is None
        assert error.symbol == "a"

    def test_transition_error_with_all_details(self):
        """Test la création d'une exception avec tous les détails."""
        error = InvalidTransitionError(
            "Invalid transition", source_state="q0", target_state="q1", symbol="a"
        )

        assert error.source_state == "q0"
        assert error.target_state == "q1"
        assert error.symbol == "a"
        assert "q0" in str(error)
        assert "q1" in str(error)
        assert "a" in str(error)

    def test_transition_error_inheritance(self):
        """Test que l'exception hérite correctement."""
        error = InvalidTransitionError("Test error")

        assert isinstance(error, Exception)
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, InvalidTransitionError)


class TestConversionError:
    """Tests pour l'exception ConversionError."""

    def test_basic_conversion_error_creation(self):
        """Test la création d'une exception de conversion."""
        error = ConversionError("Conversion failed")

        assert str(error) == "Conversion failed"
        assert error.message == "Conversion failed"
        assert error.source_type is None
        assert error.target_type is None
        assert error.conversion_step is None

    def test_conversion_error_with_types(self):
        """Test la création d'une exception avec types source et cible."""
        error = ConversionError(
            "Conversion failed", source_type="nfa", target_type="dfa"
        )

        assert (
            str(error)
            == "Conversion failed (Détails: {'source_type': 'nfa', 'target_type': 'dfa'})"
        )
        assert error.source_type == "nfa"
        assert error.target_type == "dfa"
        assert error.conversion_step is None

    def test_conversion_error_with_step(self):
        """Test la création d'une exception avec étape de conversion."""
        error = ConversionError("Conversion failed", conversion_step="determinization")

        assert (
            str(error)
            == "Conversion failed (Détails: {'conversion_step': 'determinization'})"
        )
        assert error.source_type is None
        assert error.target_type is None
        assert error.conversion_step == "determinization"

    def test_conversion_error_with_all_details(self):
        """Test la création d'une exception avec tous les détails."""
        error = ConversionError(
            "Conversion failed",
            source_type="nfa",
            target_type="dfa",
            conversion_step="determinization",
        )

        assert error.source_type == "nfa"
        assert error.target_type == "dfa"
        assert error.conversion_step == "determinization"
        assert "nfa" in str(error)
        assert "dfa" in str(error)
        assert "determinization" in str(error)

    def test_conversion_error_inheritance(self):
        """Test que l'exception hérite correctement."""
        error = ConversionError("Test error")

        assert isinstance(error, Exception)
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, ConversionError)


class TestRecognitionError:
    """Tests pour l'exception RecognitionError."""

    def test_basic_recognition_error_creation(self):
        """Test la création d'une exception de reconnaissance."""
        error = RecognitionError("Recognition failed")

        assert str(error) == "Recognition failed"
        assert error.message == "Recognition failed"
        assert error.word is None
        assert error.automaton_type is None
        assert error.recognition_step is None

    def test_recognition_error_with_word(self):
        """Test la création d'une exception avec mot."""
        error = RecognitionError("Recognition failed", word="abc")

        assert str(error) == "Recognition failed (Détails: {'word': 'abc'})"
        assert error.word == "abc"
        assert error.automaton_type is None
        assert error.recognition_step is None

    def test_recognition_error_with_automaton_type(self):
        """Test la création d'une exception avec type d'automate."""
        error = RecognitionError("Recognition failed", automaton_type="dfa")

        assert str(error) == "Recognition failed (Détails: {'automaton_type': 'dfa'})"
        assert error.word is None
        assert error.automaton_type == "dfa"
        assert error.recognition_step is None

    def test_recognition_error_with_step(self):
        """Test la création d'une exception avec étape de reconnaissance."""
        error = RecognitionError(
            "Recognition failed", recognition_step="symbol_processing"
        )

        assert (
            str(error)
            == "Recognition failed (Détails: {'recognition_step': 'symbol_processing'})"
        )
        assert error.word is None
        assert error.automaton_type is None
        assert error.recognition_step == "symbol_processing"

    def test_recognition_error_with_all_details(self):
        """Test la création d'une exception avec tous les détails."""
        error = RecognitionError(
            "Recognition failed",
            word="abc",
            automaton_type="dfa",
            recognition_step="symbol_processing",
        )

        assert error.word == "abc"
        assert error.automaton_type == "dfa"
        assert error.recognition_step == "symbol_processing"
        assert "abc" in str(error)
        assert "dfa" in str(error)
        assert "symbol_processing" in str(error)

    def test_recognition_error_inheritance(self):
        """Test que l'exception hérite correctement."""
        error = RecognitionError("Test error")

        assert isinstance(error, Exception)
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, RecognitionError)


class TestExceptionWorkflow:
    """Tests de workflow pour les exceptions."""

    def test_exception_raising_workflow(self):
        """Test le workflow de levée d'exceptions."""
        # Test de levée d'exception de base
        with pytest.raises(BaobabAutomataError) as exc_info:
            raise BaobabAutomataError("Test error")

        assert str(exc_info.value) == "Test error"

        # Test de levée d'exception avec détails
        with pytest.raises(BaobabAutomataError) as exc_info:
            raise BaobabAutomataError("Test error", {"key": "value"})

        assert "Test error" in str(exc_info.value)
        assert "Détails:" in str(exc_info.value)

    def test_exception_catching_workflow(self):
        """Test le workflow de capture d'exceptions."""
        # Test de capture d'exception spécifique
        try:
            raise InvalidStateError("Invalid state", state_identifier="q0")
        except InvalidStateError as e:
            assert e.state_identifier == "q0"
            assert "q0" in str(e)
        except Exception:
            pytest.fail("Should have caught InvalidStateError")

        # Test de capture d'exception de base
        try:
            raise InvalidTransitionError("Invalid transition")
        except BaobabAutomataError as e:
            assert isinstance(e, InvalidTransitionError)
            assert str(e) == "Invalid transition"
        except Exception:
            pytest.fail("Should have caught BaobabAutomataError")

    def test_exception_chaining_workflow(self):
        """Test le workflow de chaînage d'exceptions."""
        # Test de chaînage d'exceptions
        try:
            try:
                raise InvalidStateError("Invalid state")
            except InvalidStateError as e:
                raise InvalidAutomatonError("Invalid automaton") from e
        except InvalidAutomatonError as e:
            assert isinstance(e.__cause__, InvalidStateError)
            assert str(e.__cause__) == "Invalid state"

    def test_exception_details_workflow(self):
        """Test le workflow de gestion des détails d'exceptions."""
        # Test de détails complexes
        details = {
            "automaton_type": "dfa",
            "validation_errors": ["No initial states", "Invalid transition"],
            "state_identifier": "q0",
            "symbol": "a",
        }

        error = BaobabAutomataError("Complex error", details)

        assert error.details == details
        assert "automaton_type" in error.details
        assert "validation_errors" in error.details
        assert "state_identifier" in error.details
        assert "symbol" in error.details

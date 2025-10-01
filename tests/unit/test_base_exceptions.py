"""Tests unitaires pour les exceptions de base."""

import pytest
from baobab_automata.exceptions.base import (
    BaobabAutomataError,
    InvalidAutomatonError,
    InvalidStateError,
    InvalidTransitionError,
    ConversionError,
    RecognitionError,
)


@pytest.mark.unit
class TestBaobabAutomataError:
    """Tests pour la classe BaobabAutomataError."""

    def test_creation_with_message_only(self):
        """Test la création avec seulement un message."""
        error = BaobabAutomataError("Test error message")
        
        assert error.message == "Test error message"
        assert error.details == {}
        assert str(error) == "Test error message"

    def test_creation_with_message_and_details(self):
        """Test la création avec message et détails."""
        details = {"key1": "value1", "key2": "value2"}
        error = BaobabAutomataError("Test error message", details)
        
        assert error.message == "Test error message"
        assert error.details == details
        assert str(error) == "Test error message (Détails: {'key1': 'value1', 'key2': 'value2'})"

    def test_creation_with_none_details(self):
        """Test la création avec détails None."""
        error = BaobabAutomataError("Test error message", None)
        
        assert error.message == "Test error message"
        assert error.details == {}
        assert str(error) == "Test error message"

    def test_inheritance(self):
        """Test que BaobabAutomataError hérite d'Exception."""
        error = BaobabAutomataError("Test error")
        assert isinstance(error, Exception)

    def test_str_with_empty_details(self):
        """Test la représentation string avec détails vides."""
        error = BaobabAutomataError("Test error", {})
        assert str(error) == "Test error"

    def test_str_with_none_details(self):
        """Test la représentation string avec détails None."""
        error = BaobabAutomataError("Test error", None)
        assert str(error) == "Test error"


@pytest.mark.unit
class TestInvalidAutomatonError:
    """Tests pour la classe InvalidAutomatonError."""

    def test_creation_with_message_only(self):
        """Test la création avec seulement un message."""
        error = InvalidAutomatonError("Invalid automaton")
        
        assert error.message == "Invalid automaton"
        assert error.automaton_type is None
        assert error.validation_errors == []
        assert error.details == {}

    def test_creation_with_automaton_type(self):
        """Test la création avec type d'automate."""
        error = InvalidAutomatonError("Invalid automaton", automaton_type="DFA")
        
        assert error.message == "Invalid automaton"
        assert error.automaton_type == "DFA"
        assert error.validation_errors == []
        assert error.details == {"automaton_type": "DFA"}

    def test_creation_with_validation_errors(self):
        """Test la création avec erreurs de validation."""
        validation_errors = ["Error 1", "Error 2"]
        error = InvalidAutomatonError("Invalid automaton", validation_errors=validation_errors)
        
        assert error.message == "Invalid automaton"
        assert error.automaton_type is None
        assert error.validation_errors == validation_errors
        assert error.details == {"validation_errors": validation_errors}

    def test_creation_with_all_parameters(self):
        """Test la création avec tous les paramètres."""
        validation_errors = ["Error 1", "Error 2"]
        error = InvalidAutomatonError(
            "Invalid automaton",
            automaton_type="NFA",
            validation_errors=validation_errors
        )
        
        assert error.message == "Invalid automaton"
        assert error.automaton_type == "NFA"
        assert error.validation_errors == validation_errors
        assert error.details == {
            "automaton_type": "NFA",
            "validation_errors": validation_errors
        }

    def test_inheritance(self):
        """Test que InvalidAutomatonError hérite de BaobabAutomataError."""
        error = InvalidAutomatonError("Test error")
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, Exception)


@pytest.mark.unit
class TestInvalidStateError:
    """Tests pour la classe InvalidStateError."""

    def test_creation_with_message_only(self):
        """Test la création avec seulement un message."""
        error = InvalidStateError("Invalid state")
        
        assert error.message == "Invalid state"
        assert error.state_identifier is None
        assert error.state_type is None
        assert error.details == {}

    def test_creation_with_state_identifier(self):
        """Test la création avec identifiant d'état."""
        error = InvalidStateError("Invalid state", state_identifier="q0")
        
        assert error.message == "Invalid state"
        assert error.state_identifier == "q0"
        assert error.state_type is None
        assert error.details == {"state_identifier": "q0"}

    def test_creation_with_state_type(self):
        """Test la création avec type d'état."""
        error = InvalidStateError("Invalid state", state_type="INITIAL")
        
        assert error.message == "Invalid state"
        assert error.state_identifier is None
        assert error.state_type == "INITIAL"
        assert error.details == {"state_type": "INITIAL"}

    def test_creation_with_all_parameters(self):
        """Test la création avec tous les paramètres."""
        error = InvalidStateError(
            "Invalid state",
            state_identifier="q0",
            state_type="FINAL"
        )
        
        assert error.message == "Invalid state"
        assert error.state_identifier == "q0"
        assert error.state_type == "FINAL"
        assert error.details == {
            "state_identifier": "q0",
            "state_type": "FINAL"
        }

    def test_inheritance(self):
        """Test que InvalidStateError hérite de BaobabAutomataError."""
        error = InvalidStateError("Test error")
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, Exception)


@pytest.mark.unit
class TestInvalidTransitionError:
    """Tests pour la classe InvalidTransitionError."""

    def test_creation_with_message_only(self):
        """Test la création avec seulement un message."""
        error = InvalidTransitionError("Invalid transition")
        
        assert error.message == "Invalid transition"
        assert error.source_state is None
        assert error.target_state is None
        assert error.symbol is None
        assert error.details == {}

    def test_creation_with_source_state(self):
        """Test la création avec état source."""
        error = InvalidTransitionError("Invalid transition", source_state="q0")
        
        assert error.message == "Invalid transition"
        assert error.source_state == "q0"
        assert error.target_state is None
        assert error.symbol is None
        assert error.details == {"source_state": "q0"}

    def test_creation_with_target_state(self):
        """Test la création avec état cible."""
        error = InvalidTransitionError("Invalid transition", target_state="q1")
        
        assert error.message == "Invalid transition"
        assert error.source_state is None
        assert error.target_state == "q1"
        assert error.symbol is None
        assert error.details == {"target_state": "q1"}

    def test_creation_with_symbol(self):
        """Test la création avec symbole."""
        error = InvalidTransitionError("Invalid transition", symbol="a")
        
        assert error.message == "Invalid transition"
        assert error.source_state is None
        assert error.target_state is None
        assert error.symbol == "a"
        assert error.details == {"symbol": "a"}

    def test_creation_with_all_parameters(self):
        """Test la création avec tous les paramètres."""
        error = InvalidTransitionError(
            "Invalid transition",
            source_state="q0",
            target_state="q1",
            symbol="a"
        )
        
        assert error.message == "Invalid transition"
        assert error.source_state == "q0"
        assert error.target_state == "q1"
        assert error.symbol == "a"
        assert error.details == {
            "source_state": "q0",
            "target_state": "q1",
            "symbol": "a"
        }

    def test_inheritance(self):
        """Test que InvalidTransitionError hérite de BaobabAutomataError."""
        error = InvalidTransitionError("Test error")
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, Exception)


@pytest.mark.unit
class TestConversionError:
    """Tests pour la classe ConversionError."""

    def test_creation_with_message_only(self):
        """Test la création avec seulement un message."""
        error = ConversionError("Conversion failed")
        
        assert error.message == "Conversion failed"
        assert error.source_type is None
        assert error.target_type is None
        assert error.conversion_step is None
        assert error.details == {}

    def test_creation_with_source_type(self):
        """Test la création avec type source."""
        error = ConversionError("Conversion failed", source_type="NFA")
        
        assert error.message == "Conversion failed"
        assert error.source_type == "NFA"
        assert error.target_type is None
        assert error.conversion_step is None
        assert error.details == {"source_type": "NFA"}

    def test_creation_with_target_type(self):
        """Test la création avec type cible."""
        error = ConversionError("Conversion failed", target_type="DFA")
        
        assert error.message == "Conversion failed"
        assert error.source_type is None
        assert error.target_type == "DFA"
        assert error.conversion_step is None
        assert error.details == {"target_type": "DFA"}

    def test_creation_with_conversion_step(self):
        """Test la création avec étape de conversion."""
        error = ConversionError("Conversion failed", conversion_step="determinization")
        
        assert error.message == "Conversion failed"
        assert error.source_type is None
        assert error.target_type is None
        assert error.conversion_step == "determinization"
        assert error.details == {"conversion_step": "determinization"}

    def test_creation_with_all_parameters(self):
        """Test la création avec tous les paramètres."""
        error = ConversionError(
            "Conversion failed",
            source_type="NFA",
            target_type="DFA",
            conversion_step="determinization"
        )
        
        assert error.message == "Conversion failed"
        assert error.source_type == "NFA"
        assert error.target_type == "DFA"
        assert error.conversion_step == "determinization"
        assert error.details == {
            "source_type": "NFA",
            "target_type": "DFA",
            "conversion_step": "determinization"
        }

    def test_inheritance(self):
        """Test que ConversionError hérite de BaobabAutomataError."""
        error = ConversionError("Test error")
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, Exception)


@pytest.mark.unit
class TestRecognitionError:
    """Tests pour la classe RecognitionError."""

    def test_creation_with_message_only(self):
        """Test la création avec seulement un message."""
        error = RecognitionError("Recognition failed")
        
        assert error.message == "Recognition failed"
        assert error.word is None
        assert error.automaton_type is None
        assert error.recognition_step is None
        assert error.details == {}

    def test_creation_with_word(self):
        """Test la création avec mot."""
        error = RecognitionError("Recognition failed", word="abc")
        
        assert error.message == "Recognition failed"
        assert error.word == "abc"
        assert error.automaton_type is None
        assert error.recognition_step is None
        assert error.details == {"word": "abc"}

    def test_creation_with_automaton_type(self):
        """Test la création avec type d'automate."""
        error = RecognitionError("Recognition failed", automaton_type="DFA")
        
        assert error.message == "Recognition failed"
        assert error.word is None
        assert error.automaton_type == "DFA"
        assert error.recognition_step is None
        assert error.details == {"automaton_type": "DFA"}

    def test_creation_with_recognition_step(self):
        """Test la création avec étape de reconnaissance."""
        error = RecognitionError("Recognition failed", recognition_step="state_transition")
        
        assert error.message == "Recognition failed"
        assert error.word is None
        assert error.automaton_type is None
        assert error.recognition_step == "state_transition"
        assert error.details == {"recognition_step": "state_transition"}

    def test_creation_with_all_parameters(self):
        """Test la création avec tous les paramètres."""
        error = RecognitionError(
            "Recognition failed",
            word="abc",
            automaton_type="DFA",
            recognition_step="state_transition"
        )
        
        assert error.message == "Recognition failed"
        assert error.word == "abc"
        assert error.automaton_type == "DFA"
        assert error.recognition_step == "state_transition"
        assert error.details == {
            "word": "abc",
            "automaton_type": "DFA",
            "recognition_step": "state_transition"
        }

    def test_inheritance(self):
        """Test que RecognitionError hérite de BaobabAutomataError."""
        error = RecognitionError("Test error")
        assert isinstance(error, BaobabAutomataError)
        assert isinstance(error, Exception)


@pytest.mark.unit
class TestExceptionHierarchy:
    """Tests pour la hiérarchie des exceptions."""

    def test_exception_hierarchy(self):
        """Test la hiérarchie des exceptions."""
        # Toutes les exceptions doivent hériter de BaobabAutomataError
        assert issubclass(InvalidAutomatonError, BaobabAutomataError)
        assert issubclass(InvalidStateError, BaobabAutomataError)
        assert issubclass(InvalidTransitionError, BaobabAutomataError)
        assert issubclass(ConversionError, BaobabAutomataError)
        assert issubclass(RecognitionError, BaobabAutomataError)
        
        # Toutes les exceptions doivent hériter d'Exception
        assert issubclass(BaobabAutomataError, Exception)
        assert issubclass(InvalidAutomatonError, Exception)
        assert issubclass(InvalidStateError, Exception)
        assert issubclass(InvalidTransitionError, Exception)
        assert issubclass(ConversionError, Exception)
        assert issubclass(RecognitionError, Exception)

    def test_exception_instances(self):
        """Test que les instances d'exceptions sont correctes."""
        base_error = BaobabAutomataError("Base error")
        automaton_error = InvalidAutomatonError("Automaton error")
        state_error = InvalidStateError("State error")
        transition_error = InvalidTransitionError("Transition error")
        conversion_error = ConversionError("Conversion error")
        recognition_error = RecognitionError("Recognition error")
        
        # Toutes doivent être des instances d'Exception
        assert isinstance(base_error, Exception)
        assert isinstance(automaton_error, Exception)
        assert isinstance(state_error, Exception)
        assert isinstance(transition_error, Exception)
        assert isinstance(conversion_error, Exception)
        assert isinstance(recognition_error, Exception)
        
        # Toutes doivent être des instances de BaobabAutomataError
        assert isinstance(automaton_error, BaobabAutomataError)
        assert isinstance(state_error, BaobabAutomataError)
        assert isinstance(transition_error, BaobabAutomataError)
        assert isinstance(conversion_error, BaobabAutomataError)
        assert isinstance(recognition_error, BaobabAutomataError)

    def test_exception_raising(self):
        """Test le levage des exceptions."""
        with pytest.raises(BaobabAutomataError):
            raise BaobabAutomataError("Test error")
        
        with pytest.raises(InvalidAutomatonError):
            raise InvalidAutomatonError("Test error")
        
        with pytest.raises(InvalidStateError):
            raise InvalidStateError("Test error")
        
        with pytest.raises(InvalidTransitionError):
            raise InvalidTransitionError("Test error")
        
        with pytest.raises(ConversionError):
            raise ConversionError("Test error")
        
        with pytest.raises(RecognitionError):
            raise RecognitionError("Test error")

    def test_exception_catching(self):
        """Test la capture des exceptions."""
        try:
            raise InvalidAutomatonError("Test error")
        except BaobabAutomataError as e:
            assert str(e) == "Test error"
        except Exception:
            pytest.fail("Should have caught BaobabAutomataError")
        
        try:
            raise InvalidStateError("Test error")
        except BaobabAutomataError as e:
            assert str(e) == "Test error"
        except Exception:
            pytest.fail("Should have caught BaobabAutomataError")
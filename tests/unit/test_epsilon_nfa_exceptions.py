"""Tests unitaires pour les exceptions EpsilonNFA."""

import pytest
from baobab_automata.automata.finite.epsilon_nfa_exceptions import (
    EpsilonNFAError,
    InvalidEpsilonNFAError,
    InvalidEpsilonTransitionError,
    ConversionError,
)


@pytest.mark.unit
class TestEpsilonNFAExceptions:
    """Tests pour les exceptions EpsilonNFA."""

    def test_epsilon_nfa_error_creation(self):
        """Test la création d'une EpsilonNFAError."""
        error = EpsilonNFAError("EpsilonNFA error occurred")
        assert str(error) == "EpsilonNFA error occurred"
        assert isinstance(error, Exception)

    def test_invalid_epsilon_nfa_error(self):
        """Test la création d'une InvalidEpsilonNFAError."""
        error = InvalidEpsilonNFAError("Invalid EpsilonNFA structure")
        assert str(error) == "Invalid EpsilonNFA structure"
        assert isinstance(error, EpsilonNFAError)
        assert isinstance(error, Exception)

    def test_invalid_epsilon_transition_error(self):
        """Test la création d'une InvalidEpsilonTransitionError."""
        error = InvalidEpsilonTransitionError("Invalid epsilon transition")
        assert str(error) == "Invalid epsilon transition"
        assert isinstance(error, EpsilonNFAError)
        assert isinstance(error, Exception)

    def test_conversion_error(self):
        """Test la création d'une ConversionError."""
        error = ConversionError("Conversion failed")
        assert str(error) == "Conversion failed"
        assert isinstance(error, EpsilonNFAError)
        assert isinstance(error, Exception)

    def test_exception_hierarchy(self):
        """Test la hiérarchie des exceptions EpsilonNFA."""
        assert issubclass(InvalidEpsilonNFAError, EpsilonNFAError)
        assert issubclass(InvalidEpsilonTransitionError, EpsilonNFAError)
        assert issubclass(ConversionError, EpsilonNFAError)
        assert issubclass(EpsilonNFAError, Exception)

    def test_exception_raising(self):
        """Test le levage des exceptions EpsilonNFA."""
        with pytest.raises(EpsilonNFAError):
            raise EpsilonNFAError("Test error")
        
        with pytest.raises(InvalidEpsilonNFAError):
            raise InvalidEpsilonNFAError("Test error")
        
        with pytest.raises(InvalidEpsilonTransitionError):
            raise InvalidEpsilonTransitionError("Test error")
        
        with pytest.raises(ConversionError):
            raise ConversionError("Test error")
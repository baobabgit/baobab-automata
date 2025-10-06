"""Tests unitaires pour les exceptions NFA."""

import pytest
from baobab_automata.automata.finite.nfa_exceptions import (
    NFAError,
    InvalidNFAError,
    InvalidTransitionError,
    ConversionError,
)


@pytest.mark.unit
class TestNFAExceptions:
    """Tests pour les exceptions NFA."""

    def test_nfa_error_creation(self):
        """Test la création d'une NFAError."""
        error = NFAError("NFA error occurred")
        assert str(error) == "NFA error occurred"
        assert isinstance(error, Exception)

    def test_invalid_nfa_error(self):
        """Test la création d'une InvalidNFAError."""
        error = InvalidNFAError("Invalid NFA structure")
        assert str(error) == "Invalid NFA structure"
        assert isinstance(error, NFAError)
        assert isinstance(error, Exception)

    def test_invalid_transition_error(self):
        """Test la création d'une InvalidTransitionError."""
        error = InvalidTransitionError("Invalid transition")
        assert str(error) == "Invalid transition"
        assert isinstance(error, NFAError)
        assert isinstance(error, Exception)

    def test_conversion_error(self):
        """Test la création d'une ConversionError."""
        error = ConversionError("Conversion failed")
        assert str(error) == "Conversion failed"
        assert isinstance(error, NFAError)
        assert isinstance(error, Exception)

    def test_exception_hierarchy(self):
        """Test la hiérarchie des exceptions NFA."""
        assert issubclass(InvalidNFAError, NFAError)
        assert issubclass(InvalidTransitionError, NFAError)
        assert issubclass(ConversionError, NFAError)
        assert issubclass(NFAError, Exception)

    def test_exception_raising(self):
        """Test le levage des exceptions NFA."""
        with pytest.raises(NFAError):
            raise NFAError("Test error")
        
        with pytest.raises(InvalidNFAError):
            raise InvalidNFAError("Test error")
        
        with pytest.raises(InvalidTransitionError):
            raise InvalidTransitionError("Test error")
        
        with pytest.raises(ConversionError):
            raise ConversionError("Test error")
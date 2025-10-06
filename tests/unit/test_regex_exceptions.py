"""Tests unitaires pour les exceptions de regex."""

import pytest
from baobab_automata.automata.finite.regex_exceptions import (
    RegexError,
    RegexSyntaxError,
    RegexParseError,
    RegexConversionError,
)


@pytest.mark.unit
class TestRegexExceptions:
    """Tests pour les exceptions de regex."""

    def test_regex_error_creation(self):
        """Test la création d'une RegexError."""
        error = RegexError("Regex error occurred")
        assert str(error) == "Regex error occurred"
        assert isinstance(error, Exception)

    def test_regex_syntax_error(self):
        """Test la création d'une RegexSyntaxError."""
        error = RegexSyntaxError("Invalid regex pattern")
        assert str(error) == "Invalid regex pattern"
        assert isinstance(error, RegexError)
        assert isinstance(error, Exception)

    def test_regex_parse_error(self):
        """Test la création d'une RegexParseError."""
        error = RegexParseError("Parse error at position 5")
        assert str(error) == "Parse error at position 5"
        assert isinstance(error, RegexError)
        assert isinstance(error, Exception)

    def test_regex_conversion_error(self):
        """Test la création d'une RegexConversionError."""
        error = RegexConversionError("Conversion failed")
        assert str(error) == "Conversion failed"
        assert isinstance(error, RegexError)
        assert isinstance(error, Exception)

    def test_exception_hierarchy(self):
        """Test la hiérarchie des exceptions de regex."""
        assert issubclass(RegexSyntaxError, RegexError)
        assert issubclass(RegexParseError, RegexError)
        assert issubclass(RegexConversionError, RegexError)
        assert issubclass(RegexError, Exception)

    def test_exception_raising(self):
        """Test le levage des exceptions de regex."""
        with pytest.raises(RegexError):
            raise RegexError("Test error")
        
        with pytest.raises(RegexSyntaxError):
            raise RegexSyntaxError("Test error")
        
        with pytest.raises(RegexParseError):
            raise RegexParseError("Test error")
        
        with pytest.raises(RegexConversionError):
            raise RegexConversionError("Test error")
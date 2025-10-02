"""
Tests pour les exceptions personnalisées de conversion.
"""

import pytest
from src.baobab_automata.turing.conversion.exceptions import (
    ConversionError,
    InvalidConversionEngineError,
    ConversionTimeoutError,
    EquivalenceVerificationError,
    OptimizationError,
)


class TestConversionError:
    """Tests pour l'exception ConversionError."""

    def test_conversion_error_basic(self):
        """Teste la création d'une ConversionError basique."""
        error = ConversionError("Test error")

        assert str(error) == "Test error"
        assert error.conversion_type is None

    def test_conversion_error_with_type(self):
        """Teste la création d'une ConversionError avec un type."""
        error = ConversionError("Test error", "ntm_to_dtm")

        assert str(error) == "Test error"
        assert error.conversion_type == "ntm_to_dtm"

    def test_conversion_error_inheritance(self):
        """Teste que ConversionError hérite d'Exception."""
        error = ConversionError("Test error")

        assert isinstance(error, Exception)


class TestInvalidConversionEngineError:
    """Tests pour l'exception InvalidConversionEngineError."""

    def test_invalid_conversion_engine_error_default(self):
        """Teste la création d'une InvalidConversionEngineError par défaut."""
        error = InvalidConversionEngineError()

        assert str(error) == "Moteur de conversion invalide"
        assert error.conversion_type is None

    def test_invalid_conversion_engine_error_custom(self):
        """Teste la création d'une InvalidConversionEngineError personnalisée."""
        error = InvalidConversionEngineError("Custom error message")

        assert str(error) == "Custom error message"
        assert error.conversion_type is None

    def test_invalid_conversion_engine_error_inheritance(self):
        """Teste que InvalidConversionEngineError hérite de ConversionError."""
        error = InvalidConversionEngineError()

        assert isinstance(error, ConversionError)
        assert isinstance(error, Exception)


class TestConversionTimeoutError:
    """Tests pour l'exception ConversionTimeoutError."""

    def test_conversion_timeout_error_default(self):
        """Teste la création d'une ConversionTimeoutError par défaut."""
        error = ConversionTimeoutError()

        assert str(error) == "Conversion interrompue par timeout"
        assert error.conversion_type is None

    def test_conversion_timeout_error_custom(self):
        """Teste la création d'une ConversionTimeoutError personnalisée."""
        error = ConversionTimeoutError("Custom timeout message")

        assert str(error) == "Custom timeout message"
        assert error.conversion_type is None

    def test_conversion_timeout_error_inheritance(self):
        """Teste que ConversionTimeoutError hérite de ConversionError."""
        error = ConversionTimeoutError()

        assert isinstance(error, ConversionError)
        assert isinstance(error, Exception)


class TestEquivalenceVerificationError:
    """Tests pour l'exception EquivalenceVerificationError."""

    def test_equivalence_verification_error_default(self):
        """Teste la création d'une EquivalenceVerificationError par défaut."""
        error = EquivalenceVerificationError()

        assert str(error) == "Échec de la vérification d'équivalence"
        assert error.conversion_type is None

    def test_equivalence_verification_error_custom(self):
        """Teste la création d'une EquivalenceVerificationError personnalisée."""
        error = EquivalenceVerificationError("Custom verification message")

        assert str(error) == "Custom verification message"
        assert error.conversion_type is None

    def test_equivalence_verification_error_inheritance(self):
        """Teste que EquivalenceVerificationError hérite de ConversionError."""
        error = EquivalenceVerificationError()

        assert isinstance(error, ConversionError)
        assert isinstance(error, Exception)


class TestOptimizationError:
    """Tests pour l'exception OptimizationError."""

    def test_optimization_error_default(self):
        """Teste la création d'une OptimizationError par défaut."""
        error = OptimizationError()

        assert str(error) == "Échec de l'optimisation"
        assert error.conversion_type is None

    def test_optimization_error_custom(self):
        """Teste la création d'une OptimizationError personnalisée."""
        error = OptimizationError("Custom optimization message")

        assert str(error) == "Custom optimization message"
        assert error.conversion_type is None

    def test_optimization_error_inheritance(self):
        """Teste que OptimizationError hérite de ConversionError."""
        error = OptimizationError()

        assert isinstance(error, ConversionError)
        assert isinstance(error, Exception)

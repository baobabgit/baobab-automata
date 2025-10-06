"""Tests unitaires pour les exceptions d'optimisation."""

import pytest
from baobab_automata.finite.optimization.optimization_exceptions import (
    OptimizationError,
    OptimizationTimeoutError,
    OptimizationMemoryError,
    OptimizationValidationError,
)


@pytest.mark.unit
class TestOptimizationExceptions:
    """Tests pour les exceptions d'optimisation."""

    def test_optimization_error_creation(self):
        """Test la création d'une OptimizationError."""
        error = OptimizationError("Optimization failed")
        assert str(error) == "Optimization failed"
        assert isinstance(error, Exception)

    def test_optimization_validation_error(self):
        """Test la création d'une OptimizationValidationError."""
        error = OptimizationValidationError("Validation failed")
        assert str(error) == "Validation failed"
        assert isinstance(error, OptimizationError)
        assert isinstance(error, Exception)

    def test_optimization_timeout_error(self):
        """Test la création d'une OptimizationTimeoutError."""
        error = OptimizationTimeoutError("Timeout occurred", 5.0)
        assert str(error) == "Timeout occurred"
        assert error.timeout_duration == 5.0
        assert isinstance(error, OptimizationError)
        assert isinstance(error, Exception)

    def test_optimization_memory_error(self):
        """Test la création d'une OptimizationMemoryError."""
        error = OptimizationMemoryError("Memory limit exceeded", 1024)
        assert str(error) == "Memory limit exceeded"
        assert error.memory_required == 1024
        assert isinstance(error, OptimizationError)
        assert isinstance(error, Exception)

    def test_exception_hierarchy(self):
        """Test la hiérarchie des exceptions d'optimisation."""
        assert issubclass(OptimizationValidationError, OptimizationError)
        assert issubclass(OptimizationTimeoutError, OptimizationError)
        assert issubclass(OptimizationMemoryError, OptimizationError)
        assert issubclass(OptimizationError, Exception)

    def test_exception_raising(self):
        """Test le levage des exceptions d'optimisation."""
        with pytest.raises(OptimizationError):
            raise OptimizationError("Test error")
        
        with pytest.raises(OptimizationValidationError):
            raise OptimizationValidationError("Test error")
        
        with pytest.raises(OptimizationTimeoutError):
            raise OptimizationTimeoutError("Test error", 5.0)
        
        with pytest.raises(OptimizationMemoryError):
            raise OptimizationMemoryError("Test error", 1024)
"""Tests étendus pour les exceptions pushdown."""

import pytest
from baobab_automata.pushdown.dpda_exceptions import (
    DPDAError, InvalidDPDAError, DeterminismError, 
    ConflictError, ConversionError, DPDAOptimizationError
)
from baobab_automata.pushdown.npda_exceptions import (
    NPDAError, InvalidNPDAError, NPDATimeoutError,
    NPDAMemoryError, NPDAConfigurationError, NPDAConversionError,
    NPDAOptimizationError, NPDAValidationError, NPDAComplexityError
)
from baobab_automata.pushdown.pda_exceptions import (
    PDAError, InvalidPDAError, InvalidStateError,
    InvalidTransitionError, PDASimulationError, PDAStackError,
    PDAValidationError, PDAOperationError
)
from baobab_automata.pushdown.conversion_exceptions import (
    ConversionError as PushdownConversionError, 
    ConversionTimeoutError, ConversionValidationError,
    ConversionNotPossibleError, ConversionConfigurationError
)
from baobab_automata.pushdown.optimization_exceptions import (
    OptimizationError, OptimizationTimeoutError,
    OptimizationEquivalenceError, OptimizationConfigurationError
)
from baobab_automata.pushdown.grammar_exceptions import (
    GrammarError, GrammarValidationError, GrammarParseError, 
    GrammarConversionError, GrammarNormalizationError, 
    GrammarOptimizationError, GrammarTimeoutError, GrammarMemoryError
)
from baobab_automata.pushdown.specialized_exceptions import (
    AlgorithmError, AlgorithmTimeoutError, AlgorithmMemoryError,
    AlgorithmValidationError, AlgorithmOptimizationError, CYKError,
    EarleyError, LeftRecursionError, EmptyProductionError, NormalizationError
)


@pytest.mark.unit
class TestPushdownExceptionsExtended:
    """Tests étendus pour les exceptions pushdown."""

    def test_dpda_error_creation(self):
        """Test la création d'une DPDAError."""
        error = DPDAError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_invalid_dpda_error_creation(self):
        """Test la création d'une InvalidDPDAError."""
        error = InvalidDPDAError("Invalid DPDA")
        assert str(error) == "Invalid DPDA"
        assert isinstance(error, DPDAError)

    def test_determinism_error_creation(self):
        """Test la création d'une DeterminismError."""
        error = DeterminismError("Determinism error")
        assert str(error) == "Determinism error"
        assert isinstance(error, DPDAError)

    def test_conflict_error_creation(self):
        """Test la création d'une ConflictError."""
        error = ConflictError("Conflict error")
        assert str(error) == "Conflict error"
        assert isinstance(error, DPDAError)

    def test_conversion_error_creation(self):
        """Test la création d'une ConversionError."""
        error = ConversionError("Conversion error")
        assert str(error) == "Conversion error"
        assert isinstance(error, DPDAError)

    def test_dpda_optimization_error_creation(self):
        """Test la création d'une DPDAOptimizationError."""
        error = DPDAOptimizationError("Optimization error")
        assert str(error) == "Optimization error"
        assert isinstance(error, DPDAError)

    def test_npda_error_creation(self):
        """Test la création d'une NPDAError."""
        error = NPDAError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_invalid_npda_error_creation(self):
        """Test la création d'une InvalidNPDAError."""
        error = InvalidNPDAError("Invalid NPDA")
        assert str(error) == "Invalid NPDA"
        assert isinstance(error, NPDAError)

    def test_npda_timeout_error_creation(self):
        """Test la création d'une NPDATimeoutError."""
        error = NPDATimeoutError("Timeout error", 30.0, "test_word")
        assert "Timeout error" in str(error)
        assert isinstance(error, NPDAError)
        assert error.timeout_duration == 30.0
        assert error.word == "test_word"

    def test_npda_memory_error_creation(self):
        """Test la création d'une NPDAMemoryError."""
        error = NPDAMemoryError("Memory error", 1024, 2048)
        assert "Memory error" in str(error)
        assert isinstance(error, NPDAError)
        assert error.memory_limit == 1024
        assert error.current_usage == 2048

    def test_npda_configuration_error_creation(self):
        """Test la création d'une NPDAConfigurationError."""
        error = NPDAConfigurationError("Configuration error")
        assert str(error) == "Configuration error"
        assert isinstance(error, NPDAError)

    def test_npda_conversion_error_creation(self):
        """Test la création d'une NPDAConversionError."""
        error = NPDAConversionError("Conversion error", "NPDA", "DPDA")
        assert "Conversion error" in str(error)
        assert isinstance(error, NPDAError)
        assert error.source_type == "NPDA"
        assert error.target_type == "DPDA"

    def test_npda_optimization_error_creation(self):
        """Test la création d'une NPDAOptimizationError."""
        error = NPDAOptimizationError("Optimization error", "minimization")
        assert "Optimization error" in str(error)
        assert isinstance(error, NPDAError)
        assert error.optimization_type == "minimization"

    def test_npda_validation_error_creation(self):
        """Test la création d'une NPDAValidationError."""
        error = NPDAValidationError("Validation error")
        assert str(error) == "Validation error"
        assert isinstance(error, NPDAError)

    def test_npda_complexity_error_creation(self):
        """Test la création d'une NPDAComplexityError."""
        error = NPDAComplexityError("Complexity error", "exponential")
        assert "Complexity error" in str(error)
        assert isinstance(error, NPDAError)
        assert error.complexity_metric == "exponential"

    def test_pda_error_creation(self):
        """Test la création d'une PDAError."""
        error = PDAError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_invalid_pda_error_creation(self):
        """Test la création d'une InvalidPDAError."""
        error = InvalidPDAError("Invalid PDA")
        assert str(error) == "Invalid PDA"
        assert isinstance(error, PDAError)

    def test_invalid_state_error_creation(self):
        """Test la création d'une InvalidStateError."""
        error = InvalidStateError("q_invalid")
        assert "État invalide: 'q_invalid'" in str(error)
        assert isinstance(error, PDAError)

    def test_invalid_transition_error_creation(self):
        """Test la création d'une InvalidTransitionError."""
        error = InvalidTransitionError(("q0", "a", "Z"))
        assert "Transition invalide: ('q0', 'a', 'Z')" in str(error)
        assert isinstance(error, PDAError)

    def test_pda_simulation_error_creation(self):
        """Test la création d'une PDASimulationError."""
        error = PDASimulationError("Simulation error", "test_word", None)
        assert "Simulation error" in str(error)
        assert isinstance(error, PDAError)

    def test_pda_stack_error_creation(self):
        """Test la création d'une PDAStackError."""
        error = PDAStackError("Stack error")
        assert str(error) == "Stack error"
        assert isinstance(error, PDAError)

    def test_pda_validation_error_creation(self):
        """Test la création d'une PDAValidationError."""
        error = PDAValidationError("Validation error")
        assert str(error) == "Validation error"
        assert isinstance(error, PDAError)

    def test_pda_operation_error_creation(self):
        """Test la création d'une PDAOperationError."""
        error = PDAOperationError("union")
        assert "Erreur lors de l'opération 'union'" in str(error)
        assert isinstance(error, PDAError)

    def test_pushdown_conversion_error_creation(self):
        """Test la création d'une PushdownConversionError."""
        error = PushdownConversionError("Conversion error")
        assert str(error) == "Conversion error"
        assert isinstance(error, Exception)

    def test_conversion_timeout_error_creation(self):
        """Test la création d'une ConversionTimeoutError."""
        error = ConversionTimeoutError(30.0, "NPDA to DPDA")
        assert "Timeout de conversion après 30.0 secondes" in str(error)
        assert isinstance(error, Exception)

    def test_conversion_validation_error_creation(self):
        """Test la création d'une ConversionValidationError."""
        error = ConversionValidationError("Invalid automaton", "NPDA")
        assert "Erreur de validation: Invalid automaton" in str(error)
        assert isinstance(error, Exception)

    def test_conversion_not_possible_error_creation(self):
        """Test la création d'une ConversionNotPossibleError."""
        error = ConversionNotPossibleError("NPDA", "DFA", "Not deterministic")
        assert "Conversion impossible de NPDA vers DFA" in str(error)
        assert isinstance(error, Exception)

    def test_conversion_configuration_error_creation(self):
        """Test la création d'une ConversionConfigurationError."""
        error = ConversionConfigurationError("Invalid parameter", "timeout")
        assert "Erreur de configuration: Invalid parameter" in str(error)
        assert isinstance(error, Exception)

    def test_optimization_error_creation(self):
        """Test la création d'une OptimizationError."""
        error = OptimizationError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_optimization_timeout_error_creation(self):
        """Test la création d'une OptimizationTimeoutError."""
        error = OptimizationTimeoutError("Optimization timeout", 60.0, "minimization")
        assert "Optimization timeout" in str(error)
        assert isinstance(error, OptimizationError)
        assert error.timeout == 60.0
        assert error.algorithm == "minimization"

    def test_optimization_equivalence_error_creation(self):
        """Test la création d'une OptimizationEquivalenceError."""
        error = OptimizationEquivalenceError("Not equivalent", "NPDA", "DPDA")
        assert "Not equivalent" in str(error)
        assert isinstance(error, OptimizationError)
        assert error.original_type == "NPDA"
        assert error.optimized_type == "DPDA"

    def test_optimization_configuration_error_creation(self):
        """Test la création d'une OptimizationConfigurationError."""
        error = OptimizationConfigurationError("Invalid config", "timeout", "value")
        assert "Invalid config" in str(error)
        assert isinstance(error, OptimizationError)
        assert error.configuration == "timeout"
        assert error.parameter == "value"

    def test_grammar_error_creation(self):
        """Test la création d'une GrammarError."""
        error = GrammarError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_grammar_normalization_error_creation(self):
        """Test la création d'une GrammarNormalizationError."""
        error = GrammarNormalizationError("Grammar normalization")
        assert "Erreur de normalisation: Grammar normalization" in str(error)
        assert isinstance(error, GrammarError)

    def test_grammar_validation_error_creation(self):
        """Test la création d'une GrammarValidationError."""
        error = GrammarValidationError("Grammar validation", "S")
        assert "Erreur de validation pour la variable 'S': Grammar validation" in str(error)
        assert isinstance(error, GrammarError)

    def test_grammar_parse_error_creation(self):
        """Test la création d'une GrammarParseError."""
        error = GrammarParseError("Grammar parse", 10)
        assert "Erreur de parsing ligne 10: Grammar parse" in str(error)
        assert isinstance(error, GrammarError)

    def test_grammar_conversion_error_creation(self):
        """Test la création d'une GrammarConversionError."""
        error = GrammarConversionError("Grammar conversion", "NPDA")
        assert "Erreur de conversion NPDA: Grammar conversion" in str(error)
        assert isinstance(error, GrammarError)

    def test_grammar_optimization_error_creation(self):
        """Test la création d'une GrammarOptimizationError."""
        error = GrammarOptimizationError("Grammar optimization", "minimization")
        assert "Erreur d'optimisation minimization: Grammar optimization" in str(error)
        assert isinstance(error, GrammarError)

    def test_grammar_timeout_error_creation(self):
        """Test la création d'une GrammarTimeoutError."""
        error = GrammarTimeoutError("Grammar timeout")
        assert "Timeout: Grammar timeout" in str(error)
        assert isinstance(error, GrammarError)

    def test_grammar_memory_error_creation(self):
        """Test la création d'une GrammarMemoryError."""
        error = GrammarMemoryError("Grammar memory")
        assert "Erreur de mémoire: Grammar memory" in str(error)
        assert isinstance(error, GrammarError)

    def test_algorithm_error_creation(self):
        """Test la création d'une AlgorithmError."""
        error = AlgorithmError("Test error")
        assert "AlgorithmError: Test error" in str(error)
        assert isinstance(error, Exception)

    def test_algorithm_timeout_error_creation(self):
        """Test la création d'une AlgorithmTimeoutError."""
        error = AlgorithmTimeoutError("Algorithm timeout", 30.0)
        assert "AlgorithmTimeoutError: Algorithm timeout" in str(error)
        assert isinstance(error, AlgorithmError)
        assert error.timeout_duration == 30.0

    def test_algorithm_memory_error_creation(self):
        """Test la création d'une AlgorithmMemoryError."""
        error = AlgorithmMemoryError("Algorithm memory", 1024)
        assert "AlgorithmMemoryError: Algorithm memory" in str(error)
        assert isinstance(error, AlgorithmError)
        assert error.memory_limit == 1024

    def test_algorithm_validation_error_creation(self):
        """Test la création d'une AlgorithmValidationError."""
        error = AlgorithmValidationError("Algorithm validation")
        assert "AlgorithmValidationError: Algorithm validation" in str(error)
        assert isinstance(error, AlgorithmError)

    def test_algorithm_optimization_error_creation(self):
        """Test la création d'une AlgorithmOptimizationError."""
        error = AlgorithmOptimizationError("Algorithm optimization")
        assert "AlgorithmOptimizationError: Algorithm optimization" in str(error)
        assert isinstance(error, AlgorithmError)

    def test_cyk_error_creation(self):
        """Test la création d'une CYKError."""
        error = CYKError("CYK error")
        assert "AlgorithmError (CYK): CYK error" in str(error)
        assert isinstance(error, AlgorithmError)

    def test_earley_error_creation(self):
        """Test la création d'une EarleyError."""
        error = EarleyError("Earley error")
        assert "AlgorithmError (Earley): Earley error" in str(error)
        assert isinstance(error, AlgorithmError)

    def test_left_recursion_error_creation(self):
        """Test la création d'une LeftRecursionError."""
        error = LeftRecursionError("Left recursion error")
        assert "LeftRecursionError: Left recursion error" in str(error)
        assert isinstance(error, AlgorithmError)

    def test_empty_production_error_creation(self):
        """Test la création d'une EmptyProductionError."""
        error = EmptyProductionError("Empty production error")
        assert "EmptyProductionError: Empty production error" in str(error)
        assert isinstance(error, AlgorithmError)

    def test_normalization_error_creation(self):
        """Test la création d'une NormalizationError."""
        error = NormalizationError("Normalization error")
        assert "NormalizationError: Normalization error" in str(error)
        assert isinstance(error, AlgorithmError)

    def test_exception_hierarchy(self):
        """Test la hiérarchie des exceptions."""
        # Test DPDA exceptions
        assert issubclass(InvalidDPDAError, DPDAError)
        assert issubclass(DeterminismError, DPDAError)
        assert issubclass(ConflictError, DPDAError)
        assert issubclass(ConversionError, DPDAError)
        assert issubclass(DPDAOptimizationError, DPDAError)

        # Test NPDA exceptions
        assert issubclass(InvalidNPDAError, NPDAError)
        assert issubclass(NPDATimeoutError, NPDAError)
        assert issubclass(NPDAMemoryError, NPDAError)
        assert issubclass(NPDAConfigurationError, NPDAError)
        assert issubclass(NPDAConversionError, NPDAError)
        assert issubclass(NPDAOptimizationError, NPDAError)
        assert issubclass(NPDAValidationError, NPDAError)
        assert issubclass(NPDAComplexityError, NPDAError)

        # Test PDA exceptions
        assert issubclass(InvalidPDAError, PDAError)
        assert issubclass(InvalidStateError, PDAError)
        assert issubclass(InvalidTransitionError, PDAError)
        assert issubclass(PDASimulationError, PDAError)
        assert issubclass(PDAStackError, PDAError)
        assert issubclass(PDAValidationError, PDAError)
        assert issubclass(PDAOperationError, PDAError)

        # Test Conversion exceptions
        assert issubclass(ConversionTimeoutError, PushdownConversionError)
        assert issubclass(ConversionValidationError, PushdownConversionError)
        assert issubclass(ConversionNotPossibleError, PushdownConversionError)
        assert issubclass(ConversionConfigurationError, PushdownConversionError)

        # Test Optimization exceptions
        assert issubclass(OptimizationTimeoutError, OptimizationError)
        assert issubclass(OptimizationEquivalenceError, OptimizationError)
        assert issubclass(OptimizationConfigurationError, OptimizationError)

        # Test Grammar exceptions
        assert issubclass(GrammarValidationError, GrammarError)
        assert issubclass(GrammarParseError, GrammarError)
        assert issubclass(GrammarConversionError, GrammarError)
        assert issubclass(GrammarNormalizationError, GrammarError)
        assert issubclass(GrammarOptimizationError, GrammarError)
        assert issubclass(GrammarTimeoutError, GrammarError)
        assert issubclass(GrammarMemoryError, GrammarError)

        # Test Algorithm exceptions
        assert issubclass(AlgorithmTimeoutError, AlgorithmError)
        assert issubclass(AlgorithmMemoryError, AlgorithmError)
        assert issubclass(AlgorithmValidationError, AlgorithmError)
        assert issubclass(AlgorithmOptimizationError, AlgorithmError)
        assert issubclass(CYKError, AlgorithmError)
        assert issubclass(EarleyError, AlgorithmError)
        assert issubclass(LeftRecursionError, AlgorithmError)
        assert issubclass(EmptyProductionError, AlgorithmError)
        assert issubclass(NormalizationError, AlgorithmError)

    def test_exception_raising(self):
        """Test le levage des exceptions."""
        with pytest.raises(DPDAError):
            raise DPDAError("Test DPDA error")
        
        with pytest.raises(InvalidDPDAError):
            raise InvalidDPDAError("Test invalid DPDA error")
        
        with pytest.raises(NPDAError):
            raise NPDAError("Test NPDA error")
        
        with pytest.raises(InvalidNPDAError):
            raise InvalidNPDAError("Test invalid NPDA error")
        
        with pytest.raises(PDAError):
            raise PDAError("Test PDA error")
        
        with pytest.raises(InvalidPDAError):
            raise InvalidPDAError("Test invalid PDA error")
        
        with pytest.raises(PushdownConversionError):
            raise PushdownConversionError("Test conversion error")
        
        with pytest.raises(OptimizationError):
            raise OptimizationError("Test optimization error")
        
        with pytest.raises(GrammarError):
            raise GrammarError("Test grammar error")
        
        with pytest.raises(AlgorithmError):
            raise AlgorithmError("Test algorithm error")
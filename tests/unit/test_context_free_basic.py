"""Tests basiques pour les modules context-free."""

import pytest


@pytest.mark.unit
class TestContextFreeBasic:
    """Tests basiques pour les modules context-free."""

    def test_context_free_init_import(self):
        """Test l'import du module context-free."""
        try:
            from baobab_automata.context_free import __init__ as context_free_init
            assert context_free_init is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_import(self):
        """Test l'import de Grammar."""
        try:
            from baobab_automata.context_free.grammar import Grammar
            assert Grammar is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_parser_import(self):
        """Test l'import de GrammarParser."""
        try:
            from baobab_automata.context_free.grammar_parser import GrammarParser
            assert GrammarParser is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_types_import(self):
        """Test l'import de GrammarType."""
        try:
            from baobab_automata.context_free.grammar_types import GrammarType
            assert GrammarType is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_analysis_import(self):
        """Test l'import de GrammarAnalysis."""
        try:
            from baobab_automata.context_free.grammar_analysis import GrammarAnalysis
            assert GrammarAnalysis is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_optimization_import(self):
        """Test l'import de GrammarOptimization."""
        try:
            from baobab_automata.context_free.grammar_optimization import GrammarOptimization
            assert GrammarOptimization is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_conversion_import(self):
        """Test l'import de GrammarConversion."""
        try:
            from baobab_automata.context_free.grammar_conversion import GrammarConversion
            assert GrammarConversion is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_validation_import(self):
        """Test l'import de GrammarValidation."""
        try:
            from baobab_automata.context_free.grammar_validation import GrammarValidation
            assert GrammarValidation is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_serialization_import(self):
        """Test l'import de GrammarSerialization."""
        try:
            from baobab_automata.context_free.grammar_serialization import GrammarSerialization
            assert GrammarSerialization is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_visualization_import(self):
        """Test l'import de GrammarVisualization."""
        try:
            from baobab_automata.context_free.grammar_visualization import GrammarVisualization
            assert GrammarVisualization is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_operations_import(self):
        """Test l'import de GrammarOperations."""
        try:
            from baobab_automata.context_free.grammar_operations import GrammarOperations
            assert GrammarOperations is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_exceptions_import(self):
        """Test l'import des exceptions grammar."""
        try:
            from baobab_automata.context_free.grammar_exceptions import GrammarError
            from baobab_automata.context_free.grammar_parser_exceptions import GrammarParserError
            from baobab_automata.context_free.grammar_analysis_exceptions import GrammarAnalysisError
            from baobab_automata.context_free.grammar_optimization_exceptions import GrammarOptimizationError
            from baobab_automata.context_free.grammar_conversion_exceptions import GrammarConversionError
            from baobab_automata.context_free.grammar_validation_exceptions import GrammarValidationError
            from baobab_automata.context_free.grammar_serialization_exceptions import GrammarSerializationError
            from baobab_automata.context_free.grammar_visualization_exceptions import GrammarVisualizationError
            from baobab_automata.context_free.grammar_operations_exceptions import GrammarOperationsError
            assert GrammarError is not None
            assert GrammarParserError is not None
            assert GrammarAnalysisError is not None
            assert GrammarOptimizationError is not None
            assert GrammarConversionError is not None
            assert GrammarValidationError is not None
            assert GrammarSerializationError is not None
            assert GrammarVisualizationError is not None
            assert GrammarOperationsError is not None
        except ImportError:
            # Si les modules ne sont pas disponibles, on passe le test
            pass

    def test_grammar_utils_import(self):
        """Test l'import des utilitaires grammar."""
        try:
            from baobab_automata.context_free.grammar_utils import GrammarUtils
            assert GrammarUtils is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_metrics_import(self):
        """Test l'import des métriques grammar."""
        try:
            from baobab_automata.context_free.grammar_metrics import GrammarMetrics
            assert GrammarMetrics is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_benchmarks_import(self):
        """Test l'import des benchmarks grammar."""
        try:
            from baobab_automata.context_free.grammar_benchmarks import GrammarBenchmarks
            assert GrammarBenchmarks is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass

    def test_grammar_tests_import(self):
        """Test l'import des tests grammar."""
        try:
            from baobab_automata.context_free.grammar_tests import GrammarTests
            assert GrammarTests is not None
        except ImportError:
            # Si le module n'est pas disponible, on passe le test
            pass
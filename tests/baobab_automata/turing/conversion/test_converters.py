"""
Tests pour les convertisseurs spécialisés.
"""

import pytest
from unittest.mock import Mock, patch
from src.baobab_automata.turing.conversion.converters import (
    NTMToDTMConverter,
    MultiTapeToSingleConverter,
    StateReductionConverter,
    SymbolMinimizationConverter,
    DTMToTMConverter,
    TMToDTMConverter,
)
from src.baobab_automata.turing.conversion.conversion_types import (
    ConversionType,
    ConversionResult,
)
from src.baobab_automata.turing.conversion.exceptions import (
    ConversionError,
    EquivalenceVerificationError,
    OptimizationError,
)


class MockMachine:
    """Machine mock pour les tests."""

    def __init__(self, states=None, alphabet=None, tape_count=1):
        self.states = states or set()
        self.alphabet = alphabet or set()
        self.tape_count = tape_count


class TestNTMToDTMConverter:
    """Tests pour le convertisseur NTM -> DTM."""

    def test_convert_success(self):
        """Teste une conversion NTM -> DTM réussie."""
        converter = NTMToDTMConverter()
        source_machine = MockMachine(states={"q0", "q1"}, alphabet={"a", "b"})
        target_type = type("DTM", (), {})

        result = converter.convert(source_machine, target_type)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.NTM_TO_DTM
        assert "conversion_time" in result.conversion_stats
        assert "algorithm" in result.conversion_stats
        assert result.conversion_stats["algorithm"] == "ntm_to_dtm_simulation"

    def test_convert_with_kwargs(self):
        """Teste une conversion avec des paramètres additionnels."""
        converter = NTMToDTMConverter()
        source_machine = MockMachine()
        target_type = type("DTM", (), {})

        result = converter.convert(
            source_machine, target_type, param1="value1"
        )

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.NTM_TO_DTM

    def test_verify_equivalence_success(self):
        """Teste la vérification d'équivalence réussie."""
        converter = NTMToDTMConverter()
        source_machine = MockMachine()
        converted_machine = MockMachine()
        test_cases = ["test1", "test2"]

        result = converter.verify_equivalence(
            source_machine, converted_machine, test_cases
        )

        assert result is True

    def test_verify_equivalence_failure(self):
        """Teste la vérification d'équivalence qui échoue."""
        converter = NTMToDTMConverter()
        source_machine = MockMachine()
        converted_machine = MockMachine()
        test_cases = ["test1", "test2"]

        # Mock pour simuler une différence de résultat
        with patch.object(converter, "_simulate_execution") as mock_exec:
            mock_exec.side_effect = [True, False]  # Différents résultats

            result = converter.verify_equivalence(
                source_machine, converted_machine, test_cases
            )

            assert result is False

    def test_optimize_conversion_success(self):
        """Teste l'optimisation d'une conversion."""
        converter = NTMToDTMConverter()
        conversion_result = ConversionResult(
            converted_machine=MockMachine(),
            conversion_type=ConversionType.NTM_TO_DTM,
        )

        result = converter.optimize_conversion(conversion_result)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.NTM_TO_DTM
        assert result.optimization_applied is True
        assert "optimization_time" in result.conversion_stats

    def test_get_conversion_complexity(self):
        """Teste l'analyse de complexité."""
        converter = NTMToDTMConverter()
        source_machine = MockMachine(
            states={"q0", "q1", "q2"}, alphabet={"a", "b", "c"}
        )

        complexity = converter.get_conversion_complexity(source_machine)

        assert isinstance(complexity, dict)
        assert "time_complexity" in complexity
        assert "space_complexity" in complexity
        assert "estimated_states" in complexity
        assert "source_states" in complexity
        assert "source_symbols" in complexity

        assert complexity["time_complexity"] == "O(2^n)"
        assert complexity["space_complexity"] == "O(2^n)"
        assert complexity["source_states"] == 3
        assert complexity["source_symbols"] == 3


class TestMultiTapeToSingleConverter:
    """Tests pour le convertisseur MultiTape -> Single."""

    def test_convert_success(self):
        """Teste une conversion MultiTape -> Single réussie."""
        converter = MultiTapeToSingleConverter()
        source_machine = MockMachine(tape_count=3)
        target_type = type("TM", (), {})

        result = converter.convert(source_machine, target_type)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.MULTITAPE_TO_SINGLE
        assert "conversion_time" in result.conversion_stats
        assert "algorithm" in result.conversion_stats
        assert (
            result.conversion_stats["algorithm"]
            == "multitape_to_single_encoding"
        )

    def test_verify_equivalence_success(self):
        """Teste la vérification d'équivalence réussie."""
        converter = MultiTapeToSingleConverter()
        source_machine = MockMachine()
        converted_machine = MockMachine()
        test_cases = ["test1", "test2"]

        result = converter.verify_equivalence(
            source_machine, converted_machine, test_cases
        )

        assert result is True

    def test_optimize_conversion_success(self):
        """Teste l'optimisation d'une conversion."""
        converter = MultiTapeToSingleConverter()
        conversion_result = ConversionResult(
            converted_machine=MockMachine(),
            conversion_type=ConversionType.MULTITAPE_TO_SINGLE,
        )

        result = converter.optimize_conversion(conversion_result)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.MULTITAPE_TO_SINGLE
        assert result.optimization_applied is True

    def test_get_conversion_complexity(self):
        """Teste l'analyse de complexité."""
        converter = MultiTapeToSingleConverter()
        source_machine = MockMachine(tape_count=3, states={"q0", "q1"})

        complexity = converter.get_conversion_complexity(source_machine)

        assert isinstance(complexity, dict)
        assert "time_complexity" in complexity
        assert "space_complexity" in complexity
        assert "tape_count" in complexity
        assert "source_states" in complexity

        assert complexity["tape_count"] == 3
        assert complexity["source_states"] == 2


class TestStateReductionConverter:
    """Tests pour le convertisseur de réduction des états."""

    def test_convert_success(self):
        """Teste une réduction d'états réussie."""
        converter = StateReductionConverter()
        source_machine = MockMachine(states={"q0", "q1", "q2", "q3"})
        target_type = type("TM", (), {})

        result = converter.convert(source_machine, target_type)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.STATE_REDUCTION
        assert "conversion_time" in result.conversion_stats
        assert "algorithm" in result.conversion_stats
        assert result.conversion_stats["algorithm"] == "state_reduction"

    def test_verify_equivalence_success(self):
        """Teste la vérification d'équivalence réussie."""
        converter = StateReductionConverter()
        source_machine = MockMachine()
        converted_machine = MockMachine()
        test_cases = ["test1", "test2"]

        result = converter.verify_equivalence(
            source_machine, converted_machine, test_cases
        )

        assert result is True

    def test_optimize_conversion_success(self):
        """Teste l'optimisation d'une conversion."""
        converter = StateReductionConverter()
        conversion_result = ConversionResult(
            converted_machine=MockMachine(),
            conversion_type=ConversionType.STATE_REDUCTION,
        )

        result = converter.optimize_conversion(conversion_result)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.STATE_REDUCTION
        assert result.optimization_applied is True

    def test_get_conversion_complexity(self):
        """Teste l'analyse de complexité."""
        converter = StateReductionConverter()
        source_machine = MockMachine(states={"q0", "q1", "q2", "q3"})

        complexity = converter.get_conversion_complexity(source_machine)

        assert isinstance(complexity, dict)
        assert "time_complexity" in complexity
        assert "space_complexity" in complexity
        assert "source_states" in complexity
        assert "estimated_reduction" in complexity

        assert complexity["time_complexity"] == "O(n^2)"
        assert complexity["space_complexity"] == "O(n^2)"
        assert complexity["source_states"] == 4


class TestSymbolMinimizationConverter:
    """Tests pour le convertisseur de minimisation des symboles."""

    def test_convert_success(self):
        """Teste une minimisation de symboles réussie."""
        converter = SymbolMinimizationConverter()
        source_machine = MockMachine(alphabet={"a", "b", "c", "d"})
        target_type = type("TM", (), {})

        result = converter.convert(source_machine, target_type)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.SYMBOL_MINIMIZATION
        assert "conversion_time" in result.conversion_stats
        assert "algorithm" in result.conversion_stats
        assert result.conversion_stats["algorithm"] == "symbol_minimization"

    def test_verify_equivalence_success(self):
        """Teste la vérification d'équivalence réussie."""
        converter = SymbolMinimizationConverter()
        source_machine = MockMachine()
        converted_machine = MockMachine()
        test_cases = ["test1", "test2"]

        result = converter.verify_equivalence(
            source_machine, converted_machine, test_cases
        )

        assert result is True

    def test_optimize_conversion_success(self):
        """Teste l'optimisation d'une conversion."""
        converter = SymbolMinimizationConverter()
        conversion_result = ConversionResult(
            converted_machine=MockMachine(),
            conversion_type=ConversionType.SYMBOL_MINIMIZATION,
        )

        result = converter.optimize_conversion(conversion_result)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.SYMBOL_MINIMIZATION
        assert result.optimization_applied is True

    def test_get_conversion_complexity(self):
        """Teste l'analyse de complexité."""
        converter = SymbolMinimizationConverter()
        source_machine = MockMachine(alphabet={"a", "b", "c", "d"})

        complexity = converter.get_conversion_complexity(source_machine)

        assert isinstance(complexity, dict)
        assert "time_complexity" in complexity
        assert "space_complexity" in complexity
        assert "source_symbols" in complexity
        assert "estimated_reduction" in complexity

        assert complexity["time_complexity"] == "O(n^2)"
        assert complexity["space_complexity"] == "O(n)"
        assert complexity["source_symbols"] == 4


class TestDTMToTMConverter:
    """Tests pour le convertisseur DTM -> TM."""

    def test_convert_success(self):
        """Teste une conversion DTM -> TM réussie."""
        converter = DTMToTMConverter()
        source_machine = MockMachine(states={"q0", "q1"})
        target_type = type("TM", (), {})

        result = converter.convert(source_machine, target_type)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.DTM_TO_TM
        assert "conversion_time" in result.conversion_stats
        assert "algorithm" in result.conversion_stats
        assert result.conversion_stats["algorithm"] == "dtm_to_tm"

    def test_verify_equivalence_success(self):
        """Teste la vérification d'équivalence réussie."""
        converter = DTMToTMConverter()
        source_machine = MockMachine()
        converted_machine = MockMachine()
        test_cases = ["test1", "test2"]

        result = converter.verify_equivalence(
            source_machine, converted_machine, test_cases
        )

        assert result is True

    def test_optimize_conversion_success(self):
        """Teste l'optimisation d'une conversion."""
        converter = DTMToTMConverter()
        conversion_result = ConversionResult(
            converted_machine=MockMachine(),
            conversion_type=ConversionType.DTM_TO_TM,
        )

        result = converter.optimize_conversion(conversion_result)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.DTM_TO_TM
        assert result.optimization_applied is True

    def test_get_conversion_complexity(self):
        """Teste l'analyse de complexité."""
        converter = DTMToTMConverter()
        source_machine = MockMachine(states={"q0", "q1"})

        complexity = converter.get_conversion_complexity(source_machine)

        assert isinstance(complexity, dict)
        assert "time_complexity" in complexity
        assert "space_complexity" in complexity
        assert "source_states" in complexity
        assert "estimated_states" in complexity

        assert complexity["time_complexity"] == "O(1)"
        assert complexity["space_complexity"] == "O(1)"
        assert complexity["source_states"] == 2


class TestTMToDTMConverter:
    """Tests pour le convertisseur TM -> DTM."""

    def test_convert_success(self):
        """Teste une conversion TM -> DTM réussie."""
        converter = TMToDTMConverter()
        source_machine = MockMachine(states={"q0", "q1"})
        target_type = type("DTM", (), {})

        result = converter.convert(source_machine, target_type)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.TM_TO_DTM
        assert "conversion_time" in result.conversion_stats
        assert "algorithm" in result.conversion_stats
        assert result.conversion_stats["algorithm"] == "tm_to_dtm"

    def test_verify_equivalence_success(self):
        """Teste la vérification d'équivalence réussie."""
        converter = TMToDTMConverter()
        source_machine = MockMachine()
        converted_machine = MockMachine()
        test_cases = ["test1", "test2"]

        result = converter.verify_equivalence(
            source_machine, converted_machine, test_cases
        )

        assert result is True

    def test_optimize_conversion_success(self):
        """Teste l'optimisation d'une conversion."""
        converter = TMToDTMConverter()
        conversion_result = ConversionResult(
            converted_machine=MockMachine(),
            conversion_type=ConversionType.TM_TO_DTM,
        )

        result = converter.optimize_conversion(conversion_result)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.TM_TO_DTM
        assert result.optimization_applied is True

    def test_get_conversion_complexity(self):
        """Teste l'analyse de complexité."""
        converter = TMToDTMConverter()
        source_machine = MockMachine(states={"q0", "q1"})

        complexity = converter.get_conversion_complexity(source_machine)

        assert isinstance(complexity, dict)
        assert "time_complexity" in complexity
        assert "space_complexity" in complexity
        assert "source_states" in complexity
        assert "estimated_states" in complexity

        assert complexity["time_complexity"] == "O(1)"
        assert complexity["space_complexity"] == "O(1)"
        assert complexity["source_states"] == 2

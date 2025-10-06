"""
Tests pour le moteur de conversion.
"""

import pytest
from unittest.mock import Mock, patch
from baobab_automata.turing.conversion.conversion_engine import (
    ConversionEngine,
)
from baobab_automata.turing.conversion.conversion_types import (
    ConversionType,
    ConversionResult,
    IConversionAlgorithm,
)
from baobab_automata.turing.conversion.exceptions import (
    ConversionError,
    InvalidConversionEngineError,
    ConversionTimeoutError,
)


class MockAlgorithm(IConversionAlgorithm):
    """Algorithme mock pour les tests."""

    def __init__(self, should_fail=False, execution_time=0.1):
        self.should_fail = should_fail
        self.execution_time = execution_time

    def convert(self, source_machine, target_type, **kwargs):
        """Convertit une machine source vers un type cible."""
        if self.should_fail:
            raise ConversionError("Conversion failed")

        # Simule un délai
        import time

        time.sleep(self.execution_time)

        return ConversionResult(
            converted_machine=object(),
            conversion_type=ConversionType.NTM_TO_DTM,
            success=True,
        )

    def verify_equivalence(
        self, source_machine, converted_machine, test_cases
    ):
        """Vérifie l'équivalence entre deux machines."""
        return True

    def optimize_conversion(self, conversion_result):
        """Optimise le résultat d'une conversion."""
        return conversion_result

    def get_conversion_complexity(self, source_machine):
        """Analyse la complexité d'une conversion."""
        return {"complexity": "O(n)"}


class TestConversionEngine:
    """Tests pour la classe ConversionEngine."""

    def test_engine_initialization(self):
        """Teste l'initialisation du moteur de conversion."""
        engine = ConversionEngine(cache_size=50, timeout=10.0)

        assert engine.cache_size == 50
        assert engine.timeout == 10.0
        assert len(engine._cache) == 0
        assert len(engine._algorithms) == 0
        assert len(engine._conversion_stats) == 0

    def test_engine_default_initialization(self):
        """Teste l'initialisation par défaut du moteur."""
        engine = ConversionEngine()

        assert engine.cache_size == 100
        assert engine.timeout == 30.0

    def test_register_algorithm_success(self):
        """Teste l'enregistrement d'un algorithme valide."""
        engine = ConversionEngine()
        algorithm = MockAlgorithm()

        engine.register_algorithm(ConversionType.NTM_TO_DTM, algorithm)

        assert ConversionType.NTM_TO_DTM in engine._algorithms
        assert engine._algorithms[ConversionType.NTM_TO_DTM] is algorithm

    def test_register_algorithm_invalid(self):
        """Teste l'enregistrement d'un algorithme invalide."""
        engine = ConversionEngine()
        invalid_algorithm = object()

        with pytest.raises(InvalidConversionEngineError):
            engine.register_algorithm(
                ConversionType.NTM_TO_DTM, invalid_algorithm
            )

    def test_convert_success(self):
        """Teste une conversion réussie."""
        engine = ConversionEngine()
        algorithm = MockAlgorithm()
        engine.register_algorithm(ConversionType.NTM_TO_DTM, algorithm)

        source_machine = object()
        target_type = type("DTM", (), {})

        result = engine.convert(
            source_machine, target_type, ConversionType.NTM_TO_DTM
        )

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.NTM_TO_DTM

    def test_convert_no_algorithm(self):
        """Teste une conversion sans algorithme enregistré."""
        engine = ConversionEngine()
        source_machine = object()
        target_type = type("DTM", (), {})

        with pytest.raises(ConversionError):
            engine.convert(
                source_machine, target_type, ConversionType.NTM_TO_DTM
            )

    def test_convert_algorithm_failure(self):
        """Teste une conversion qui échoue."""
        engine = ConversionEngine()
        algorithm = MockAlgorithm(should_fail=True)
        engine.register_algorithm(ConversionType.NTM_TO_DTM, algorithm)

        source_machine = object()
        target_type = type("DTM", (), {})

        with pytest.raises(ConversionError):
            engine.convert(
                source_machine, target_type, ConversionType.NTM_TO_DTM
            )

    def test_convert_timeout(self):
        """Teste une conversion qui dépasse le timeout."""
        engine = ConversionEngine(timeout=0.01)  # Timeout très court
        algorithm = MockAlgorithm(execution_time=0.1)  # Exécution plus longue
        engine.register_algorithm(ConversionType.NTM_TO_DTM, algorithm)

        source_machine = object()
        target_type = type("DTM", (), {})

        with pytest.raises(ConversionTimeoutError):
            engine.convert(
                source_machine, target_type, ConversionType.NTM_TO_DTM
            )

    def test_convert_caching(self):
        """Teste la mise en cache des conversions."""
        engine = ConversionEngine()
        algorithm = MockAlgorithm()
        engine.register_algorithm(ConversionType.NTM_TO_DTM, algorithm)

        source_machine = object()
        target_type = type("DTM", (), {})

        # Première conversion
        result1 = engine.convert(
            source_machine, target_type, ConversionType.NTM_TO_DTM
        )

        # Deuxième conversion (devrait utiliser le cache)
        result2 = engine.convert(
            source_machine, target_type, ConversionType.NTM_TO_DTM
        )

        assert result1 is result2  # Même objet retourné
        assert len(engine._cache) == 1

    def test_verify_equivalence_success(self):
        """Teste la vérification d'équivalence réussie."""
        engine = ConversionEngine()
        algorithm = MockAlgorithm()
        engine.register_algorithm(ConversionType.NTM_TO_DTM, algorithm)

        source_machine = object()
        converted_machine = object()
        test_cases = ["test1", "test2"]

        result = engine.verify_equivalence(
            source_machine,
            converted_machine,
            test_cases,
            ConversionType.NTM_TO_DTM,
        )

        assert result is True

    def test_verify_equivalence_no_algorithm(self):
        """Teste la vérification d'équivalence sans algorithme."""
        engine = ConversionEngine()
        source_machine = object()
        converted_machine = object()
        test_cases = ["test1", "test2"]

        with pytest.raises(ConversionError):
            engine.verify_equivalence(
                source_machine,
                converted_machine,
                test_cases,
                ConversionType.NTM_TO_DTM,
            )

    def test_optimize_conversion_success(self):
        """Teste l'optimisation d'une conversion."""
        engine = ConversionEngine()
        algorithm = MockAlgorithm()
        engine.register_algorithm(ConversionType.NTM_TO_DTM, algorithm)

        conversion_result = ConversionResult(
            converted_machine=object(),
            conversion_type=ConversionType.NTM_TO_DTM,
            success=True,
        )

        result = engine.optimize_conversion(conversion_result)

        assert isinstance(result, ConversionResult)
        assert result.conversion_type == ConversionType.NTM_TO_DTM

    def test_optimize_conversion_no_algorithm(self):
        """Teste l'optimisation sans algorithme."""
        engine = ConversionEngine()
        conversion_result = ConversionResult(
            converted_machine=object(),
            conversion_type=ConversionType.NTM_TO_DTM,
            success=True,
        )

        with pytest.raises(ConversionError):
            engine.optimize_conversion(conversion_result)

    def test_get_conversion_stats(self):
        """Teste la récupération des statistiques."""
        engine = ConversionEngine()
        algorithm = MockAlgorithm()
        engine.register_algorithm(ConversionType.NTM_TO_DTM, algorithm)

        source_machine = object()
        target_type = type("DTM", (), {})

        # Effectue une conversion pour générer des statistiques
        engine.convert(source_machine, target_type, ConversionType.NTM_TO_DTM)

        stats = engine.get_conversion_stats()

        assert isinstance(stats, dict)
        assert ConversionType.NTM_TO_DTM.value in stats

    def test_clear_cache(self):
        """Teste la suppression du cache."""
        engine = ConversionEngine()
        algorithm = MockAlgorithm()
        engine.register_algorithm(ConversionType.NTM_TO_DTM, algorithm)

        source_machine = object()
        target_type = type("DTM", (), {})

        # Effectue une conversion pour remplir le cache
        engine.convert(source_machine, target_type, ConversionType.NTM_TO_DTM)

        assert len(engine._cache) == 1

        # Vide le cache
        engine.clear_cache()

        assert len(engine._cache) == 0

    def test_cache_size_limit(self):
        """Teste la limite de taille du cache."""
        engine = ConversionEngine(cache_size=2)
        algorithm = MockAlgorithm()
        engine.register_algorithm(ConversionType.NTM_TO_DTM, algorithm)

        target_type = type("DTM", (), {})

        # Effectue plusieurs conversions pour dépasser la limite
        # Utilise des machines avec des attributs différents pour générer des clés de cache différentes
        machines = []
        for i in range(3):
            machine = type("Machine", (), {})()
            machine.id = i
            machine.name = f"machine_{i}"
            machines.append(machine)
            engine.convert(machine, target_type, ConversionType.NTM_TO_DTM)

        # Le cache ne devrait contenir que 2 éléments
        assert len(engine._cache) == 2

        # Vérifie que les deux dernières conversions sont en cache
        cache_keys = list(engine._cache.keys())
        assert len(cache_keys) == 2

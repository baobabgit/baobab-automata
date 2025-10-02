"""
Moteur de conversion des machines de Turing.

Ce module implémente le moteur principal de conversion qui gère
le cache, les algorithmes et l'orchestration des conversions.
"""

import time
from typing import Any, Dict, List, Type
from .conversion_types import (
    ConversionResult,
    ConversionType,
    IConversionAlgorithm,
)
from .exceptions import (
    ConversionError,
    InvalidConversionEngineError,
    ConversionTimeoutError,
)


class ConversionEngine:
    """Moteur principal de conversion des machines de Turing."""

    def __init__(self, cache_size: int = 100, timeout: float = 30.0):
        """Initialise le moteur de conversion.

        :param cache_size: Taille maximale du cache
        :param timeout: Timeout en secondes pour les conversions
        """
        self.cache_size = cache_size
        self.timeout = timeout
        self._cache: Dict[str, ConversionResult] = {}
        self._algorithms: Dict[ConversionType, IConversionAlgorithm] = {}
        self._conversion_stats: Dict[str, Any] = {}

    def register_algorithm(
        self, conversion_type: ConversionType, algorithm: IConversionAlgorithm
    ) -> None:
        """Enregistre un algorithme de conversion.

        :param conversion_type: Type de conversion
        :param algorithm: Algorithme à enregistrer
        :raises InvalidConversionEngineError: Si l'algorithme est invalide
        """
        if not isinstance(algorithm, IConversionAlgorithm):
            raise InvalidConversionEngineError(
                "L'algorithme doit implémenter IConversionAlgorithm"
            )
        self._algorithms[conversion_type] = algorithm

    def convert(
        self,
        source_machine: Any,
        target_type: Type,
        conversion_type: ConversionType,
        **kwargs,
    ) -> ConversionResult:
        """Convertit une machine source vers un type cible.

        :param source_machine: Machine source à convertir
        :param target_type: Type cible de la conversion
        :param conversion_type: Type de conversion à utiliser
        :param kwargs: Paramètres additionnels pour la conversion
        :return: Résultat de la conversion
        :raises ConversionError: Si la conversion échoue
        :raises ConversionTimeoutError: Si la conversion dépasse le timeout
        """
        # Vérification du cache
        cache_key = self._generate_cache_key(
            source_machine, target_type, conversion_type
        )
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Vérification de l'algorithme
        if conversion_type not in self._algorithms:
            raise ConversionError(
                f"Aucun algorithme enregistré pour le type {conversion_type}"
            )

        algorithm = self._algorithms[conversion_type]

        # Conversion avec timeout
        start_time = time.time()
        try:
            result = algorithm.convert(source_machine, target_type, **kwargs)

            # Vérification du timeout
            if time.time() - start_time > self.timeout:
                raise ConversionTimeoutError(
                    f"Conversion interrompue après {self.timeout}s"
                )

            # Mise à jour des statistiques
            duration = time.time() - start_time
            self._update_conversion_stats(conversion_type, duration)

            # Mise en cache
            self._cache_result(cache_key, result)

            return result

        except Exception as e:
            if isinstance(e, (ConversionError, ConversionTimeoutError)):
                raise
            raise ConversionError(f"Erreur lors de la conversion: {str(e)}")

    def verify_equivalence(
        self,
        source_machine: Any,
        converted_machine: Any,
        test_cases: List[str],
        conversion_type: ConversionType,
    ) -> bool:
        """Vérifie l'équivalence entre deux machines.

        :param source_machine: Machine source
        :param converted_machine: Machine convertie
        :param test_cases: Cas de test pour la vérification
        :param conversion_type: Type de conversion utilisé
        :return: True si les machines sont équivalentes
        :raises ConversionError: Si la vérification échoue
        """
        if conversion_type not in self._algorithms:
            raise ConversionError(
                f"Aucun algorithme enregistré pour le type {conversion_type}"
            )

        algorithm = self._algorithms[conversion_type]
        return algorithm.verify_equivalence(
            source_machine, converted_machine, test_cases
        )

    def optimize_conversion(
        self,
        conversion_result: ConversionResult,
        conversion_type: ConversionType,
    ) -> ConversionResult:
        """Optimise le résultat d'une conversion.

        :param conversion_result: Résultat de conversion à optimiser
        :param conversion_type: Type de conversion utilisé
        :return: Résultat optimisé
        :raises ConversionError: Si l'optimisation échoue
        """
        if conversion_type not in self._algorithms:
            raise ConversionError(
                f"Aucun algorithme enregistré pour le type {conversion_type}"
            )

        algorithm = self._algorithms[conversion_type]
        return algorithm.optimize_conversion(conversion_result)

    def get_conversion_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de conversion.

        :return: Statistiques de conversion
        """
        return self._conversion_stats.copy()

    def clear_cache(self) -> None:
        """Vide le cache de conversion."""
        self._cache.clear()

    def _generate_cache_key(
        self,
        source_machine: Any,
        target_type: Type,
        conversion_type: ConversionType,
    ) -> str:
        """Génère une clé de cache pour une conversion.

        :param source_machine: Machine source
        :param target_type: Type cible
        :param conversion_type: Type de conversion
        :return: Clé de cache
        """
        # Utilisation d'un hash simple basé sur les attributs de la machine
        machine_hash = hash(
            str(source_machine.__dict__)
            if hasattr(source_machine, "__dict__")
            else str(source_machine)
        )
        return f"{conversion_type.value}_{target_type.__name__}_{machine_hash}"

    def _cache_result(self, cache_key: str, result: ConversionResult) -> None:
        """Met en cache un résultat de conversion.

        :param cache_key: Clé de cache
        :param result: Résultat à mettre en cache
        """
        if len(self._cache) >= self.cache_size:
            # Suppression du plus ancien élément (FIFO)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]

        self._cache[cache_key] = result

    def _update_conversion_stats(
        self, conversion_type: ConversionType, duration: float
    ) -> None:
        """Met à jour les statistiques de conversion.

        :param conversion_type: Type de conversion
        :param duration: Durée de la conversion
        """
        if conversion_type.value not in self._conversion_stats:
            self._conversion_stats[conversion_type.value] = {
                "count": 0,
                "total_duration": 0.0,
                "avg_duration": 0.0,
                "min_duration": float("inf"),
                "max_duration": 0.0,
            }

        stats = self._conversion_stats[conversion_type.value]
        stats["count"] += 1
        stats["total_duration"] += duration
        stats["avg_duration"] = stats["total_duration"] / stats["count"]
        stats["min_duration"] = min(stats["min_duration"], duration)
        stats["max_duration"] = max(stats["max_duration"], duration)

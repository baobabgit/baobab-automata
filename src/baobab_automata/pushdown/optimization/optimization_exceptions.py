"""
Exceptions personnalisées pour les algorithmes d'optimisation des automates à pile.

Ce module définit la hiérarchie d'exceptions utilisée par les algorithmes
d'optimisation des automates à pile (PDA, DPDA, NPDA).
"""

from typing import Any, Dict, Optional


class OptimizationError(Exception):
    """Exception de base pour les erreurs d'optimisation des automates à pile.

    Cette exception est levée lorsqu'une erreur générale se produit
    lors de l'exécution des algorithmes d'optimisation.

    :param message: Message d'erreur détaillé
    :param details: Détails supplémentaires sur l'erreur
    """

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialise l'exception d'optimisation.

        :param message: Message d'erreur détaillé
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception.

        :return: Représentation string de l'exception
        """
        if self.details:
            return f"{self.message} (Détails: {self.details})"
        return self.message


class OptimizationTimeoutError(OptimizationError):
    """Exception levée lors d'un timeout d'optimisation.

    Cette exception est levée lorsqu'un algorithme d'optimisation
    dépasse le temps limite autorisé.

    :param message: Message d'erreur détaillé
    :param timeout: Timeout en secondes
    :param algorithm: Nom de l'algorithme qui a échoué
    """

    def __init__(self, message: str, timeout: float, algorithm: str) -> None:
        """Initialise l'exception de timeout d'optimisation.

        :param message: Message d'erreur détaillé
        :param timeout: Timeout en secondes
        :param algorithm: Nom de l'algorithme qui a échoué
        """
        super().__init__(message, {"timeout": timeout, "algorithm": algorithm})
        self.timeout = timeout
        self.algorithm = algorithm


class OptimizationMemoryError(OptimizationError):
    """Exception levée lors d'un dépassement de mémoire.

    Cette exception est levée lorsqu'un algorithme d'optimisation
    dépasse les limites de mémoire disponibles.

    :param message: Message d'erreur détaillé
    :param memory_limit: Limite de mémoire en octets
    :param algorithm: Nom de l'algorithme qui a échoué
    """

    def __init__(
        self, message: str, memory_limit: int, algorithm: str
    ) -> None:
        """Initialise l'exception de dépassement de mémoire.

        :param message: Message d'erreur détaillé
        :param memory_limit: Limite de mémoire en octets
        :param algorithm: Nom de l'algorithme qui a échoué
        """
        super().__init__(
            message, {"memory_limit": memory_limit, "algorithm": algorithm}
        )
        self.memory_limit = memory_limit
        self.algorithm = algorithm


class OptimizationValidationError(OptimizationError):
    """Exception levée lors d'une erreur de validation d'optimisation.

    Cette exception est levée lorsqu'une validation d'optimisation échoue,
    par exemple lors de la vérification d'équivalence.

    :param message: Message d'erreur détaillé
    :param validation_type: Type de validation qui a échoué
    :param details: Détails supplémentaires sur l'erreur de validation
    """

    def __init__(
        self,
        message: str,
        validation_type: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception de validation d'optimisation.

        :param message: Message d'erreur détaillé
        :param validation_type: Type de validation qui a échoué
        :param details: Détails supplémentaires sur l'erreur de validation
        """
        super().__init__(message, details)
        self.validation_type = validation_type


class OptimizationEquivalenceError(OptimizationError):
    """Exception levée lors d'une erreur d'équivalence d'optimisation.

    Cette exception est levée lorsqu'un automate optimisé n'est pas
    équivalent à l'automate original.

    :param message: Message d'erreur détaillé
    :param original_type: Type de l'automate original
    :param optimized_type: Type de l'automate optimisé
    :param test_words: Mots de test qui ont échoué
    """

    def __init__(
        self,
        message: str,
        original_type: str,
        optimized_type: str,
        test_words: Optional[list] = None,
    ) -> None:
        """Initialise l'exception d'équivalence d'optimisation.

        :param message: Message d'erreur détaillé
        :param original_type: Type de l'automate original
        :param optimized_type: Type de l'automate optimisé
        :param test_words: Mots de test qui ont échoué
        """
        super().__init__(
            message,
            {
                "original_type": original_type,
                "optimized_type": optimized_type,
                "test_words": test_words or [],
            },
        )
        self.original_type = original_type
        self.optimized_type = optimized_type
        self.test_words = test_words or []


class OptimizationConfigurationError(OptimizationError):
    """Exception levée lors d'une erreur de configuration d'optimisation.

    Cette exception est levée lorsqu'une configuration d'optimisation
    est invalide ou incompatible.

    :param message: Message d'erreur détaillé
    :param configuration: Configuration qui a échoué
    :param parameter: Paramètre problématique
    """

    def __init__(
        self, message: str, configuration: str, parameter: str
    ) -> None:
        """Initialise l'exception de configuration d'optimisation.

        :param message: Message d'erreur détaillé
        :param configuration: Configuration qui a échoué
        :param parameter: Paramètre problématique
        """
        super().__init__(
            message, {"configuration": configuration, "parameter": parameter}
        )
        self.configuration = configuration
        self.parameter = parameter


class OptimizationCacheError(OptimizationError):
    """Exception levée lors d'une erreur de cache d'optimisation.

    Cette exception est levée lorsqu'une erreur se produit lors de
    l'utilisation du cache des optimisations.

    :param message: Message d'erreur détaillé
    :param cache_operation: Opération de cache qui a échoué
    :param cache_key: Clé de cache problématique
    """

    def __init__(
        self, message: str, cache_operation: str, cache_key: str
    ) -> None:
        """Initialise l'exception de cache d'optimisation.

        :param message: Message d'erreur détaillé
        :param cache_operation: Opération de cache qui a échoué
        :param cache_key: Clé de cache problématique
        """
        super().__init__(
            message,
            {"cache_operation": cache_operation, "cache_key": cache_key},
        )
        self.cache_operation = cache_operation
        self.cache_key = cache_key

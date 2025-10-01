"""
Exceptions pour les algorithmes spécialisés.

Ce module définit les exceptions personnalisées pour les algorithmes spécialisés
des grammaires hors-contexte et des automates à pile.
"""

from typing import Any, Dict, Optional


class AlgorithmError(Exception):
    """Exception de base pour les algorithmes spécialisés.

    Cette exception est levée lorsqu'une erreur générale se produit
    dans l'exécution d'un algorithme spécialisé.
    """

    def __init__(
        self,
        message: str,
        algorithm_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception.

        :param message: Message d'erreur descriptif
        :param algorithm_type: Type d'algorithme qui a échoué
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message)
        self.message = message
        self.algorithm_type = algorithm_type
        self.details = details or {}

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception."""
        base_msg = f"AlgorithmError: {self.message}"
        if self.algorithm_type:
            base_msg = (
                f"AlgorithmError ({self.algorithm_type}): {self.message}"
            )
        return base_msg


class AlgorithmTimeoutError(AlgorithmError):
    """Exception pour timeout d'algorithme.

    Cette exception est levée lorsqu'un algorithme dépasse le temps
    maximum autorisé pour son exécution.
    """

    def __init__(
        self,
        message: str,
        timeout_duration: float,
        algorithm_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception de timeout.

        :param message: Message d'erreur descriptif
        :param timeout_duration: Durée du timeout en secondes
        :param algorithm_type: Type d'algorithme qui a échoué
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, algorithm_type, details)
        self.timeout_duration = timeout_duration

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception."""
        return f"AlgorithmTimeoutError: {self.message} (timeout: {self.timeout_duration}s)"


class AlgorithmMemoryError(AlgorithmError):
    """Exception pour dépassement de mémoire.

    Cette exception est levée lorsqu'un algorithme dépasse la limite
    de mémoire autorisée pour son exécution.
    """

    def __init__(
        self,
        message: str,
        memory_limit: int,
        algorithm_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception de mémoire.

        :param message: Message d'erreur descriptif
        :param memory_limit: Limite de mémoire en octets
        :param algorithm_type: Type d'algorithme qui a échoué
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, algorithm_type, details)
        self.memory_limit = memory_limit

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception."""
        return f"AlgorithmMemoryError: {self.message} (limit: {self.memory_limit} bytes)"


class AlgorithmValidationError(AlgorithmError):
    """Exception pour erreur de validation.

    Cette exception est levée lorsqu'une validation d'algorithme échoue,
    par exemple lors de la validation d'une grammaire ou d'un automate.
    """

    def __init__(
        self,
        message: str,
        validation_type: Optional[str] = None,
        algorithm_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception de validation.

        :param message: Message d'erreur descriptif
        :param validation_type: Type de validation qui a échoué
        :param algorithm_type: Type d'algorithme qui a échoué
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, algorithm_type, details)
        self.validation_type = validation_type

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception."""
        base_msg = f"AlgorithmValidationError: {self.message}"
        if self.validation_type:
            base_msg = f"AlgorithmValidationError ({self.validation_type}): {self.message}"
        return base_msg


class AlgorithmOptimizationError(AlgorithmError):
    """Exception pour erreur d'optimisation.

    Cette exception est levée lorsqu'une optimisation d'algorithme échoue,
    par exemple lors de la mise en cache ou de l'optimisation de performance.
    """

    def __init__(
        self,
        message: str,
        optimization_type: Optional[str] = None,
        algorithm_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception d'optimisation.

        :param message: Message d'erreur descriptif
        :param optimization_type: Type d'optimisation qui a échoué
        :param algorithm_type: Type d'algorithme qui a échoué
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, algorithm_type, details)
        self.optimization_type = optimization_type

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception."""
        base_msg = f"AlgorithmOptimizationError: {self.message}"
        if self.optimization_type:
            base_msg = f"AlgorithmOptimizationError ({self.optimization_type}): {self.message}"
        return base_msg


class CYKError(AlgorithmError):
    """Exception spécifique pour l'algorithme CYK."""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialise l'exception CYK.

        :param message: Message d'erreur descriptif
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, "CYK", details)


class EarleyError(AlgorithmError):
    """Exception spécifique pour l'algorithme Earley."""

    def __init__(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialise l'exception Earley.

        :param message: Message d'erreur descriptif
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, "Earley", details)


class LeftRecursionError(AlgorithmError):
    """Exception pour les erreurs de récursivité gauche."""

    def __init__(
        self,
        message: str,
        variable: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception de récursivité gauche.

        :param message: Message d'erreur descriptif
        :param variable: Variable avec récursivité gauche
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, "LeftRecursion", details)
        self.variable = variable

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception."""
        base_msg = f"LeftRecursionError: {self.message}"
        if self.variable:
            base_msg = f"LeftRecursionError (variable '{self.variable}'): {self.message}"
        return base_msg


class EmptyProductionError(AlgorithmError):
    """Exception pour les erreurs de productions vides."""

    def __init__(
        self,
        message: str,
        variable: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception de production vide.

        :param message: Message d'erreur descriptif
        :param variable: Variable avec production vide
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, "EmptyProduction", details)
        self.variable = variable

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception."""
        base_msg = f"EmptyProductionError: {self.message}"
        if self.variable:
            base_msg = f"EmptyProductionError (variable '{self.variable}'): {self.message}"
        return base_msg


class NormalizationError(AlgorithmError):
    """Exception pour les erreurs de normalisation."""

    def __init__(
        self,
        message: str,
        normalization_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception de normalisation.

        :param message: Message d'erreur descriptif
        :param normalization_type: Type de normalisation qui a échoué
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, "Normalization", details)
        self.normalization_type = normalization_type

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception."""
        base_msg = f"NormalizationError: {self.message}"
        if self.normalization_type:
            base_msg = f"NormalizationError ({self.normalization_type}): {self.message}"
        return base_msg

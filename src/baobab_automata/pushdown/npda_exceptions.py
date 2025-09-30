"""
Exceptions personnalisées pour les automates à pile non-déterministes (NPDA).

Ce module définit la hiérarchie d'exceptions spécifiques aux NPDA,
permettant une gestion d'erreurs fine et informative.
"""

from typing import Any, Optional


class NPDAError(Exception):
    """Exception de base pour les NPDA.

    Cette exception est la classe de base pour toutes les exceptions
    spécifiques aux automates à pile non-déterministes.
    """

    def __init__(self, message: str, details: Optional[Any] = None) -> None:
        """Initialise l'exception avec un message et des détails optionnels.

        :param message: Message d'erreur descriptif
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception.

        :return: Message d'erreur avec détails si disponibles
        """
        if self.details:
            return f"{self.message} (Détails: {self.details})"
        return self.message


class InvalidNPDAError(NPDAError):
    """Exception pour NPDA invalide.

    Cette exception est levée lorsqu'un NPDA ne respecte pas
    les contraintes de validité définies.
    """

    def __init__(self, message: str, validation_errors: Optional[list] = None) -> None:
        """Initialise l'exception avec les erreurs de validation.

        :param message: Message d'erreur descriptif
        :param validation_errors: Liste des erreurs de validation
        """
        super().__init__(message, validation_errors)
        self.validation_errors = validation_errors or []


class NPDATimeoutError(NPDAError):
    """Exception pour timeout de calcul.

    Cette exception est levée lorsqu'un calcul de reconnaissance
    dépasse le timeout configuré.
    """

    def __init__(self, message: str, timeout_duration: float, word: str) -> None:
        """Initialise l'exception avec les détails du timeout.

        :param message: Message d'erreur descriptif
        :param timeout_duration: Durée du timeout en secondes
        :param word: Mot qui a causé le timeout
        """
        super().__init__(message, {"timeout_duration": timeout_duration, "word": word})
        self.timeout_duration = timeout_duration
        self.word = word


class NPDAMemoryError(NPDAError):
    """Exception pour dépassement de mémoire.

    Cette exception est levée lorsqu'un calcul de reconnaissance
    dépasse la limite de mémoire configurée.
    """

    def __init__(self, message: str, memory_limit: int, current_usage: int) -> None:
        """Initialise l'exception avec les détails de mémoire.

        :param message: Message d'erreur descriptif
        :param memory_limit: Limite de mémoire en octets
        :param current_usage: Utilisation actuelle de la mémoire en octets
        """
        super().__init__(
            message, {"memory_limit": memory_limit, "current_usage": current_usage}
        )
        self.memory_limit = memory_limit
        self.current_usage = current_usage


class NPDAConfigurationError(NPDAError):
    """Exception pour erreur de configuration.

    Cette exception est levée lorsqu'une configuration d'exécution
    parallèle est invalide.
    """

    def __init__(self, message: str, config_errors: Optional[list] = None) -> None:
        """Initialise l'exception avec les erreurs de configuration.

        :param message: Message d'erreur descriptif
        :param config_errors: Liste des erreurs de configuration
        """
        super().__init__(message, config_errors)
        self.config_errors = config_errors or []


class NPDAConversionError(NPDAError):
    """Exception pour erreur de conversion.

    Cette exception est levée lorsqu'une conversion entre types
    d'automates échoue.
    """

    def __init__(self, message: str, source_type: str, target_type: str) -> None:
        """Initialise l'exception avec les détails de conversion.

        :param message: Message d'erreur descriptif
        :param source_type: Type d'automate source
        :param target_type: Type d'automate cible
        """
        super().__init__(
            message, {"source_type": source_type, "target_type": target_type}
        )
        self.source_type = source_type
        self.target_type = target_type


class NPDAOptimizationError(NPDAError):
    """Exception pour erreur d'optimisation.

    Cette exception est levée lorsqu'une optimisation parallèle
    échoue.
    """

    def __init__(self, message: str, optimization_type: str) -> None:
        """Initialise l'exception avec le type d'optimisation.

        :param message: Message d'erreur descriptif
        :param optimization_type: Type d'optimisation qui a échoué
        """
        super().__init__(message, {"optimization_type": optimization_type})
        self.optimization_type = optimization_type


class NPDAValidationError(NPDAError):
    """Exception pour erreur de validation.

    Cette exception est levée lorsqu'une validation de cohérence
    d'un NPDA échoue.
    """

    def __init__(self, message: str, validation_errors: Optional[list] = None) -> None:
        """Initialise l'exception avec les erreurs de validation.

        :param message: Message d'erreur descriptif
        :param validation_errors: Liste des erreurs de validation
        """
        super().__init__(message, validation_errors)
        self.validation_errors = validation_errors or []


class NPDAComplexityError(NPDAError):
    """Exception pour erreur d'analyse de complexité.

    Cette exception est levée lorsqu'une analyse de complexité
    échoue.
    """

    def __init__(self, message: str, complexity_metric: str) -> None:
        """Initialise l'exception avec la métrique de complexité.

        :param message: Message d'erreur descriptif
        :param complexity_metric: Métrique de complexité qui a échoué
        """
        super().__init__(message, {"complexity_metric": complexity_metric})
        self.complexity_metric = complexity_metric

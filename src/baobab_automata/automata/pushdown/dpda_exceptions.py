"""
Exceptions personnalisées pour les automates à pile déterministes (DPDA).

Ce module définit la hiérarchie d'exceptions pour la gestion des erreurs
spécifiques aux DPDA, incluant les erreurs de déterminisme, de conflits
et de conversion.
"""

from typing import Any, Dict, Optional


class DPDAError(Exception):
    """Exception de base pour les erreurs liées aux DPDA.

    Cette exception sert de classe de base pour toutes les erreurs
    spécifiques aux automates à pile déterministes.

    :param message: Message d'erreur descriptif
    :param details: Détails supplémentaires sur l'erreur
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialise l'exception DPDA.

        :param message: Message d'erreur descriptif
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception.

        :return: Message d'erreur avec détails si disponibles
        """
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class InvalidDPDAError(DPDAError):
    """Exception levée quand un DPDA est invalide.

    Cette exception est levée lors de la validation d'un DPDA qui ne
    respecte pas les contraintes de validité ou de déterminisme.

    :param message: Message d'erreur descriptif
    :param validation_errors: Liste des erreurs de validation
    :param details: Détails supplémentaires sur l'erreur
    """

    def __init__(
        self,
        message: str,
        validation_errors: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception InvalidDPDAError.

        :param message: Message d'erreur descriptif
        :param validation_errors: Liste des erreurs de validation
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, details)
        self.validation_errors = validation_errors or []

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception.

        :return: Message d'erreur avec erreurs de validation
        """
        if self.validation_errors:
            errors_str = "; ".join(self.validation_errors)
            return f"{self.message} - Erreurs: {errors_str}"
        return self.message


class DeterminismError(DPDAError):
    """Exception levée quand les contraintes de déterminisme sont violées.

    Cette exception est levée quand un automate ne respecte pas les
    contraintes de déterminisme requises pour un DPDA.

    :param message: Message d'erreur descriptif
    :param conflicts: Liste des conflits de déterminisme détectés
    :param details: Détails supplémentaires sur l'erreur
    """

    def __init__(
        self,
        message: str,
        conflicts: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception DeterminismError.

        :param message: Message d'erreur descriptif
        :param conflicts: Liste des conflits de déterminisme détectés
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, details)
        self.conflicts = conflicts or []

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception.

        :return: Message d'erreur avec conflits détectés
        """
        if self.conflicts:
            conflicts_str = "; ".join(self.conflicts)
            return f"{self.message} - Conflits: {conflicts_str}"
        return self.message


class ConflictError(DPDAError):
    """Exception levée quand des conflits de déterminisme sont détectés.

    Cette exception est levée lors de la détection de conflits spécifiques
    dans les transitions d'un DPDA.

    :param message: Message d'erreur descriptif
    :param conflict_type: Type de conflit détecté
    :param conflict_details: Détails du conflit
    :param details: Détails supplémentaires sur l'erreur
    """

    def __init__(
        self,
        message: str,
        conflict_type: Optional[str] = None,
        conflict_details: Optional[Dict[str, Any]] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception ConflictError.

        :param message: Message d'erreur descriptif
        :param conflict_type: Type de conflit détecté
        :param conflict_details: Détails du conflit
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, details)
        self.conflict_type = conflict_type
        self.conflict_details = conflict_details or {}

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception.

        :return: Message d'erreur avec type de conflit
        """
        if self.conflict_type:
            return f"{self.message} - Type: {self.conflict_type}"
        return self.message


class ConversionError(DPDAError):
    """Exception levée lors d'erreurs de conversion entre types d'automates.

    Cette exception est levée quand une conversion entre PDA et DPDA
    échoue ou n'est pas possible.

    :param message: Message d'erreur descriptif
    :param source_type: Type d'automate source
    :param target_type: Type d'automate cible
    :param conversion_step: Étape de conversion où l'erreur s'est produite
    :param details: Détails supplémentaires sur l'erreur
    """

    def __init__(
        self,
        message: str,
        source_type: Optional[str] = None,
        target_type: Optional[str] = None,
        conversion_step: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception ConversionError.

        :param message: Message d'erreur descriptif
        :param source_type: Type d'automate source
        :param target_type: Type d'automate cible
        :param conversion_step: Étape de conversion où l'erreur s'est produite
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, details)
        self.source_type = source_type
        self.target_type = target_type
        self.conversion_step = conversion_step

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception.

        :return: Message d'erreur avec détails de conversion
        """
        parts = [self.message]
        if self.source_type and self.target_type:
            parts.append(f"({self.source_type} -> {self.target_type})")
        if self.conversion_step:
            parts.append(f"à l'étape: {self.conversion_step}")
        return " ".join(parts)


class DPDAOptimizationError(DPDAError):
    """Exception levée lors d'erreurs d'optimisation des DPDA.

    Cette exception est levée quand une optimisation d'un DPDA échoue
    ou produit un résultat invalide.

    :param message: Message d'erreur descriptif
    :param optimization_type: Type d'optimisation qui a échoué
    :param details: Détails supplémentaires sur l'erreur
    """

    def __init__(
        self,
        message: str,
        optimization_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialise l'exception DPDAOptimizationError.

        :param message: Message d'erreur descriptif
        :param optimization_type: Type d'optimisation qui a échoué
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message, details)
        self.optimization_type = optimization_type

    def __str__(self) -> str:
        """Retourne la représentation string de l'exception.

        :return: Message d'erreur avec type d'optimisation
        """
        if self.optimization_type:
            return f"{self.message} - Type d'optimisation: {self.optimization_type}"
        return self.message

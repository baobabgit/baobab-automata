"""
Exceptions personnalisées pour les algorithmes de conversion des automates à pile.

Ce module définit la hiérarchie d'exceptions pour la gestion des erreurs
dans les conversions entre différents types d'automates à pile.
"""


class ConversionError(Exception):
    """Exception de base pour les erreurs de conversion."""

    def __init__(self, message: str, details: str = None) -> None:
        """Initialise l'exception de conversion.

        :param message: Message d'erreur principal
        :param details: Détails supplémentaires optionnels
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Représentation textuelle de l'exception."""
        if self.details:
            return f"{self.message} - Détails: {self.details}"
        return self.message


class ConversionTimeoutError(ConversionError):
    """Exception levée lors d'un timeout de conversion."""

    def __init__(self, timeout: float, operation: str = None) -> None:
        """Initialise l'exception de timeout.

        :param timeout: Timeout en secondes
        :param operation: Opération qui a échoué
        """
        message = f"Timeout de conversion après {timeout} secondes"
        if operation:
            message += f" lors de l'opération: {operation}"
        super().__init__(message)


class ConversionMemoryError(ConversionError):
    """Exception levée lors d'un dépassement de mémoire."""

    def __init__(self, operation: str = None) -> None:
        """Initialise l'exception de mémoire.

        :param operation: Opération qui a échoué
        """
        message = "Dépassement de mémoire lors de la conversion"
        if operation:
            message += f" lors de l'opération: {operation}"
        super().__init__(message)


class ConversionValidationError(ConversionError):
    """Exception levée lors d'une erreur de validation."""

    def __init__(
        self, validation_error: str, automaton_type: str = None
    ) -> None:
        """Initialise l'exception de validation.

        :param validation_error: Erreur de validation
        :param automaton_type: Type d'automate concerné
        """
        message = f"Erreur de validation: {validation_error}"
        if automaton_type:
            message += f" pour l'automate de type: {automaton_type}"
        super().__init__(message)


class ConversionOptimizationError(ConversionError):
    """Exception levée lors d'une erreur d'optimisation."""

    def __init__(
        self, optimization_error: str, optimization_type: str = None
    ) -> None:
        """Initialise l'exception d'optimisation.

        :param optimization_error: Erreur d'optimisation
        :param optimization_type: Type d'optimisation concerné
        """
        message = f"Erreur d'optimisation: {optimization_error}"
        if optimization_type:
            message += f" pour l'optimisation: {optimization_type}"
        super().__init__(message)


class ConversionEquivalenceError(ConversionError):
    """Exception levée lors d'une erreur de vérification d'équivalence."""

    def __init__(
        self,
        equivalence_error: str,
        automaton1_type: str = None,
        automaton2_type: str = None,
    ) -> None:
        """Initialise l'exception d'équivalence.

        :param equivalence_error: Erreur d'équivalence
        :param automaton1_type: Type du premier automate
        :param automaton2_type: Type du deuxième automate
        """
        message = f"Erreur d'équivalence: {equivalence_error}"
        if automaton1_type and automaton2_type:
            message += f" entre {automaton1_type} et {automaton2_type}"
        super().__init__(message)


class ConversionNotPossibleError(ConversionError):
    """Exception levée quand une conversion n'est pas possible."""

    def __init__(
        self, source_type: str, target_type: str, reason: str = None
    ) -> None:
        """Initialise l'exception de conversion impossible.

        :param source_type: Type source de l'automate
        :param target_type: Type cible de l'automate
        :param reason: Raison de l'impossibilité
        """
        message = f"Conversion impossible de {source_type} vers {target_type}"
        if reason:
            message += f" - Raison: {reason}"
        super().__init__(message)


class ConversionConfigurationError(ConversionError):
    """Exception levée lors d'une erreur de configuration."""

    def __init__(self, config_error: str, parameter: str = None) -> None:
        """Initialise l'exception de configuration.

        :param config_error: Erreur de configuration
        :param parameter: Paramètre concerné
        """
        message = f"Erreur de configuration: {config_error}"
        if parameter:
            message += f" pour le paramètre: {parameter}"
        super().__init__(message)

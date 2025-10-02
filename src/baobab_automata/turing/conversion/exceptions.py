"""
Exceptions personnalisées pour les algorithmes de conversion.

Ce module définit les exceptions spécifiques aux erreurs de conversion
des machines de Turing.
"""


class ConversionError(Exception):
    """Exception de base pour les erreurs de conversion."""

    def __init__(self, message: str, conversion_type: str = None):
        """Initialise l'exception de conversion.

        :param message: Message d'erreur
        :param conversion_type: Type de conversion qui a échoué
        """
        super().__init__(message)
        self.conversion_type = conversion_type


class InvalidConversionEngineError(ConversionError):
    """Exception levée quand le moteur de conversion est invalide."""

    def __init__(self, message: str = "Moteur de conversion invalide"):
        """Initialise l'exception de moteur invalide.

        :param message: Message d'erreur
        """
        super().__init__(message)


class ConversionTimeoutError(ConversionError):
    """Exception levée quand une conversion dépasse le temps limite."""

    def __init__(self, message: str = "Conversion interrompue par timeout"):
        """Initialise l'exception de timeout.

        :param message: Message d'erreur
        """
        super().__init__(message)


class EquivalenceVerificationError(ConversionError):
    """Exception levée quand la vérification d'équivalence échoue."""

    def __init__(
        self, message: str = "Échec de la vérification d'équivalence"
    ):
        """Initialise l'exception de vérification d'équivalence.

        :param message: Message d'erreur
        """
        super().__init__(message)


class OptimizationError(ConversionError):
    """Exception levée quand une optimisation échoue."""

    def __init__(self, message: str = "Échec de l'optimisation"):
        """Initialise l'exception d'optimisation.

        :param message: Message d'erreur
        """
        super().__init__(message)

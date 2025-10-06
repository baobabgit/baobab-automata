"""Exceptions pour les conversions de machines de Turing."""

class ConversionError(Exception):
    """Erreur générale de conversion."""
    def __init__(self, message: str, conversion_type: str = None):
        super().__init__(message)
        self.conversion_type = conversion_type

class ConversionTimeoutError(ConversionError):
    """Erreur de timeout lors de la conversion."""
    def __init__(self, message: str = "Conversion interrompue par timeout", conversion_type: str = None):
        super().__init__(message, conversion_type)

class ConversionValidationError(ConversionError):
    """Erreur de validation lors de la conversion."""
    pass

class InvalidConversionEngineError(ConversionError):
    """Erreur de moteur de conversion invalide."""
    def __init__(self, message: str = "Moteur de conversion invalide", conversion_type: str = None):
        super().__init__(message, conversion_type)

class EquivalenceVerificationError(ConversionError):
    """Erreur de vérification d'équivalence."""
    def __init__(self, message: str = "Échec de la vérification d'équivalence", conversion_type: str = None):
        super().__init__(message, conversion_type)

class OptimizationError(ConversionError):
    """Erreur d'optimisation."""
    def __init__(self, message: str = "Échec de l'optimisation", conversion_type: str = None):
        super().__init__(message, conversion_type)

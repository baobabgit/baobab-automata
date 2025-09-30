"""
Exceptions personnalisées pour les ε-NFA.

Ce module définit les exceptions spécifiques aux automates finis non-déterministes
avec transitions epsilon (ε-NFA).
"""


class EpsilonNFAError(Exception):
    """Exception de base pour les erreurs ε-NFA."""
    pass


class InvalidEpsilonNFAError(EpsilonNFAError):
    """Exception levée quand un ε-NFA est invalide."""
    pass


class InvalidEpsilonTransitionError(EpsilonNFAError):
    """Exception levée quand une transition epsilon est invalide."""
    pass


class ConversionError(EpsilonNFAError):
    """Exception levée lors d'une erreur de conversion."""
    pass
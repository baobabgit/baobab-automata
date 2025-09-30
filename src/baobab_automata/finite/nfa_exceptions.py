"""
Exceptions personnalisées pour les NFA.

Ce module définit les exceptions spécifiques aux automates finis non-déterministes.
"""


class NFAError(Exception):
    """Exception de base pour les erreurs NFA."""
    pass


class InvalidNFAError(NFAError):
    """Exception levée quand un NFA est invalide."""
    pass


class InvalidTransitionError(NFAError):
    """Exception levée quand une transition est invalide."""
    pass


class ConversionError(NFAError):
    """Exception levée lors d'une erreur de conversion."""
    pass
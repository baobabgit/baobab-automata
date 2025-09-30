"""
Exceptions personnalisées pour les DFA.

Ce module définit les exceptions spécifiques aux automates finis déterministes.
"""


class DFAError(Exception):
    """Exception de base pour les erreurs DFA."""
    pass


class InvalidDFAError(DFAError):
    """Exception levée quand un DFA est invalide."""
    pass


class InvalidTransitionError(DFAError):
    """Exception levée quand une transition est invalide."""
    pass


class InvalidStateError(DFAError):
    """Exception levée quand un état est invalide."""
    pass
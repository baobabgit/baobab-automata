"""
Exceptions pour les opérations sur les langages.

Ce module définit toutes les exceptions spécifiques aux opérations
sur les langages réguliers dans la bibliothèque Baobab Automata.
"""


class LanguageOperationError(Exception):
    """
    Exception de base pour les erreurs d'opérations sur les langages.

    Cette exception est la classe parente de toutes les exceptions
    liées aux opérations sur les langages réguliers.
    """


class InvalidOperationError(LanguageOperationError):
    """
    Exception levée lorsqu'une opération invalide est tentée.

    Cette exception est levée lorsque l'opération demandée n'est pas
    supportée ou n'est pas valide dans le contexte donné.
    """


class IncompatibleAutomataError(LanguageOperationError):
    """
    Exception levée lorsque les automates sont incompatibles.

    Cette exception est levée lorsque deux automates ne peuvent pas
    être utilisés ensemble dans une opération (par exemple, alphabets
    différents, types incompatibles, etc.).
    """


class OperationTimeoutError(LanguageOperationError):
    """
    Exception levée lors d'un timeout d'opération.

    Cette exception est levée lorsque une opération prend trop de temps
    à s'exécuter et dépasse le délai maximum autorisé.
    """


class OperationMemoryError(LanguageOperationError):
    """
    Exception levée lors d'une erreur de mémoire.

    Cette exception est levée lorsque une opération nécessite plus
    de mémoire que disponible ou que la limite configurée est dépassée.
    """


class InvalidMappingError(LanguageOperationError):
    """
    Exception levée lors d'un mapping invalide.

    Cette exception est levée lorsque le mapping fourni pour un
    homomorphisme n'est pas valide ou cohérent.
    """


class OperationValidationError(LanguageOperationError):
    """
    Exception levée lors d'une erreur de validation d'opération.

    Cette exception est levée lorsque les paramètres d'une opération
    ne passent pas la validation ou ne respectent pas les contraintes.
    """

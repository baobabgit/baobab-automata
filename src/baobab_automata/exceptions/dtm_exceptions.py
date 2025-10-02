"""
Exceptions personnalisées pour les machines de Turing déterministes.

Ce module définit toutes les exceptions spécifiques aux machines de Turing
déterministes et à leur simulation optimisée.
"""

from .tm_exceptions import TMError


class DTMError(TMError):
    """Exception de base pour les machines de Turing déterministes.

    Cette exception est la classe parente de toutes les exceptions
    spécifiques aux machines de Turing déterministes.
    """


class InvalidDTMError(DTMError):
    """Exception levée lorsqu'une machine de Turing déterministe est invalide.

    Cette exception est levée lors de la construction d'une machine
    de Turing déterministe qui ne respecte pas les contraintes de validité
    ou de déterminisme.
    """


class DTMDeterminismError(DTMError):
    """Exception levée lors d'une violation du déterminisme.

    Cette exception est levée lorsqu'une machine de Turing déterministe
    présente des transitions non-déterministes.
    """


class DTMSimulationError(DTMError):
    """Exception levée lors d'une erreur de simulation déterministe.

    Cette exception est levée lorsqu'une erreur survient pendant
    la simulation optimisée d'une machine de Turing déterministe.
    """


class DTMOptimizationError(DTMError):
    """Exception levée lors d'une erreur d'optimisation.

    Cette exception est levée lorsqu'une erreur survient pendant
    l'optimisation des transitions d'une machine de Turing déterministe.
    """


class DTMCacheError(DTMError):
    """Exception levée lors d'une erreur de cache.

    Cette exception est levée lorsqu'une erreur survient dans le système
    de cache des optimisations d'une machine de Turing déterministe.
    """

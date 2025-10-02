"""
Exceptions spécifiques aux machines de Turing non-déterministes.

Ce module définit les exceptions personnalisées pour les machines de Turing
non-déterministes (NTM), étendant la hiérarchie d'exceptions des machines de
Turing.
"""

from .tm_exceptions import TMError


class NTMError(TMError):
    """Exception de base pour les machines de Turing non-déterministes.

    Cette exception est la classe de base pour toutes les erreurs
    spécifiques aux machines de Turing non-déterministes.
    """


class InvalidNTMError(NTMError):
    """Exception pour machine de Turing non-déterministe invalide.

    Cette exception est levée lorsque la configuration d'une NTM
    ne respecte pas les contraintes de validité.
    """


class NTMNonDeterminismError(NTMError):
    """Exception pour violation du non-déterminisme.

    Cette exception est levée lorsque les transitions d'une NTM
    ne respectent pas les contraintes de non-déterminisme.
    """


class NTMSimulationError(NTMError):
    """Exception pour erreur de simulation non-déterministe.

    Cette exception est levée lors d'erreurs pendant la simulation
    d'une machine de Turing non-déterministe.
    """


class NTMOptimizationError(NTMError):
    """Exception pour erreur d'optimisation.

    Cette exception est levée lors d'erreurs pendant l'optimisation
    d'une machine de Turing non-déterministe.
    """


class NTMBranchLimitError(NTMError):
    """Exception pour dépassement de la limite de branches.

    Cette exception est levée lorsque le nombre de branches simultanées
    dépasse la limite autorisée lors de la simulation.
    """


class NTMConfigurationError(NTMError):
    """Exception pour erreur de configuration NTM.

    Cette exception est levée lors d'erreurs dans la configuration
    d'une machine de Turing non-déterministe.
    """


class NTMTransitionError(NTMError):
    """Exception pour erreur de transition NTM.

    Cette exception est levée lors d'erreurs dans la définition
    ou l'exécution des transitions non-déterministes.
    """

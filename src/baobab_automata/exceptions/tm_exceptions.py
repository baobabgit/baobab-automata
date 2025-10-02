"""
Exceptions personnalisées pour les machines de Turing.

Ce module définit toutes les exceptions spécifiques aux machines de Turing
et à leur simulation.
"""


class TMError(Exception):
    """Exception de base pour les machines de Turing.

    Cette exception est la classe parente de toutes les exceptions
    spécifiques aux machines de Turing.
    """


class InvalidTMError(TMError):
    """Exception levée lorsqu'une machine de Turing est invalide.

    Cette exception est levée lors de la construction d'une machine
    de Turing qui ne respecte pas les contraintes de validité.
    """


class InvalidStateError(TMError):
    """Exception levée lorsqu'un état invalide est utilisé.

    Cette exception est levée lorsqu'un état qui n'existe pas
    dans la machine est référencé.
    """


class InvalidTransitionError(TMError):
    """Exception levée lorsqu'une transition invalide est définie.

    Cette exception est levée lorsqu'une transition ne respecte pas
    les contraintes de la machine de Turing.
    """


class TMSimulationError(TMError):
    """Exception levée lors d'une erreur de simulation.

    Cette exception est levée lorsqu'une erreur survient pendant
    la simulation d'une machine de Turing.
    """


class TMTimeoutError(TMError):
    """Exception levée lors d'un timeout de simulation.

    Cette exception est levée lorsqu'une simulation dépasse
    le nombre maximum d'étapes autorisées.
    """

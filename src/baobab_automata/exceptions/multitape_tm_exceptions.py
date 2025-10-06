"""
Exceptions spécifiques aux machines de Turing multi-bandes.

Ce module définit les exceptions personnalisées pour les machines de Turing
multi-bandes, permettant une gestion d'erreurs fine et spécifique.
"""

from typing import List, Optional
from .tm_exceptions import TMError


class MultiTapeTMError(TMError):
    """Exception de base pour les machines de Turing multi-bandes.

    Cette exception sert de classe de base pour toutes les erreurs
    spécifiques aux machines de Turing multi-bandes.
    """

    def __init__(self, message: str, error_code: Optional[str] = None):
        """Initialise l'exception.

        :param message: Message d'erreur descriptif
        :param error_code: Code d'erreur optionnel pour le debugging
        """
        super().__init__(message)
        self.error_code = error_code


class InvalidMultiTapeTMError(MultiTapeTMError):
    """Exception pour machine de Turing multi-bande invalide.

    Cette exception est levée lorsque la configuration d'une machine
    de Turing multi-bande ne respecte pas les contraintes de validité.
    """

    def __init__(self, message: str, validation_errors: Optional[List[str]] = None):
        """Initialise l'exception.

        :param message: Message d'erreur descriptif
        :param validation_errors: Liste des erreurs de validation détaillées
        """
        super().__init__(message, "INVALID_MULTITAPE_TM")
        self.validation_errors = validation_errors or []


class MultiTapeTMConsistencyError(MultiTapeTMError):
    """Exception pour violation de la cohérence multi-bande.

    Cette exception est levée lorsque les transitions ou la configuration
    d'une machine multi-bande ne respectent pas la cohérence entre les bandes.
    """

    def __init__(self, message: str, inconsistency_details: Optional[List[str]] = None):
        """Initialise l'exception.

        :param message: Message d'erreur descriptif
        :param inconsistency_details: Détails des incohérences détectées
        """
        super().__init__(message, "MULTITAPE_CONSISTENCY_ERROR")
        self.inconsistency_details = inconsistency_details or []


class MultiTapeTMSimulationError(MultiTapeTMError):
    """Exception pour erreur de simulation multi-bande.

    Cette exception est levée lors d'erreurs pendant la simulation
    d'une machine de Turing multi-bande.
    """

    def __init__(self, message: str, step_count: Optional[int] = None):
        """Initialise l'exception.

        :param message: Message d'erreur descriptif
        :param step_count: Nombre d'étapes effectuées avant l'erreur
        """
        super().__init__(message, "MULTITAPE_SIMULATION_ERROR")
        self.step_count = step_count


class MultiTapeTMConversionError(MultiTapeTMError):
    """Exception pour erreur de conversion.

    Cette exception est levée lors d'erreurs pendant la conversion
    d'une machine multi-bande vers une machine à bande unique.
    """

    def __init__(self, message: str, conversion_step: Optional[str] = None):
        """Initialise l'exception.

        :param message: Message d'erreur descriptif
        :param conversion_step: Étape de conversion où l'erreur s'est produite
        """
        super().__init__(message, "MULTITAPE_CONVERSION_ERROR")
        self.conversion_step = conversion_step


class MultiTapeTMOptimizationError(MultiTapeTMError):
    """Exception pour erreur d'optimisation.

    Cette exception est levée lors d'erreurs pendant l'optimisation
    d'une machine de Turing multi-bande.
    """

    def __init__(self, message: str, optimization_type: Optional[str] = None):
        """Initialise l'exception.

        :param message: Message d'erreur descriptif
        :param optimization_type: Type d'optimisation qui a échoué
        """
        super().__init__(message, "MULTITAPE_OPTIMIZATION_ERROR")
        self.optimization_type = optimization_type


class MultiTapeTMSynchronizationError(MultiTapeTMError):
    """Exception pour erreur de synchronisation.

    Cette exception est levée lors d'erreurs pendant la synchronisation
    des têtes de lecture/écriture d'une machine multi-bande.
    """

    def __init__(self, message: str, tape_ids: Optional[List[int]] = None):
        """Initialise l'exception.

        :param message: Message d'erreur descriptif
        :param tape_ids: Identifiants des bandes impliquées dans l'erreur
        """
        super().__init__(message, "MULTITAPE_SYNCHRONIZATION_ERROR")
        self.tape_ids = tape_ids or []


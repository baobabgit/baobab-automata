"""
Exceptions pour les algorithmes d'optimisation.

Ce module définit les exceptions spécifiques aux algorithmes d'optimisation
des automates finis.
"""


class OptimizationError(Exception):
    """
    Exception de base pour les erreurs d'optimisation.
    
    Cette exception est levée lorsqu'une erreur générale se produit
    lors de l'optimisation d'un automate.
    """
    
    def __init__(self, message: str) -> None:
        """
        Initialise l'exception d'optimisation.
        
        :param message: Message d'erreur
        :type message: str
        """
        super().__init__(message)
        self.message = message


class OptimizationTimeoutError(OptimizationError):
    """
    Exception levée lors d'un timeout d'optimisation.
    
    Cette exception est levée lorsqu'un algorithme d'optimisation
    dépasse le temps limite autorisé.
    """
    
    def __init__(self, message: str, timeout_duration: float) -> None:
        """
        Initialise l'exception de timeout d'optimisation.
        
        :param message: Message d'erreur
        :type message: str
        :param timeout_duration: Durée du timeout en secondes
        :type timeout_duration: float
        """
        super().__init__(message)
        self.timeout_duration = timeout_duration


class OptimizationMemoryError(OptimizationError):
    """
    Exception levée lors d'une erreur de mémoire d'optimisation.
    
    Cette exception est levée lorsqu'un algorithme d'optimisation
    nécessite plus de mémoire que disponible.
    """
    
    def __init__(self, message: str, memory_required: int) -> None:
        """
        Initialise l'exception de mémoire d'optimisation.
        
        :param message: Message d'erreur
        :type message: str
        :param memory_required: Mémoire requise en octets
        :type memory_required: int
        """
        super().__init__(message)
        self.memory_required = memory_required


class OptimizationValidationError(OptimizationError):
    """
    Exception levée lors d'une erreur de validation d'optimisation.
    
    Cette exception est levée lorsqu'une optimisation produit un
    automate non équivalent à l'original.
    """
    
    def __init__(self, message: str, validation_details: str = "") -> None:
        """
        Initialise l'exception de validation d'optimisation.
        
        :param message: Message d'erreur
        :type message: str
        :param validation_details: Détails de la validation
        :type validation_details: str
        """
        super().__init__(message)
        self.validation_details = validation_details
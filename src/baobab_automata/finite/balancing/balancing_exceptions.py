"""
Exceptions pour les stratégies de balancing.

Ce module définit les exceptions spécifiques aux opérations
de balancing des automates finis.
"""

from ..optimization_exceptions import OptimizationError


class BalancingError(OptimizationError):
    """
    Exception de base pour les erreurs de balancing.
    
    Cette exception est levée lorsqu'une erreur survient
    lors d'une opération de balancing d'automate.
    """
    
    def __init__(self, message: str, automaton_type: str = None) -> None:
        """
        Initialise l'exception de balancing.
        
        :param message: Message d'erreur
        :type message: str
        :param automaton_type: Type d'automate concerné
        :type automaton_type: str, optional
        """
        super().__init__(message)
        self.automaton_type = automaton_type


class InvalidBalancingStrategyError(BalancingError):
    """
    Exception levée lorsqu'une stratégie de balancing est invalide.
    
    Cette exception est levée lorsque :
    - Une stratégie de balancing n'est pas correctement implémentée
    - Une stratégie ne peut pas être appliquée à un automate donné
    - Les paramètres d'une stratégie sont invalides
    """
    
    def __init__(self, strategy_name: str, reason: str = None) -> None:
        """
        Initialise l'exception de stratégie invalide.
        
        :param strategy_name: Nom de la stratégie invalide
        :type strategy_name: str
        :param reason: Raison de l'invalidité
        :type reason: str, optional
        """
        message = f"Stratégie de balancing invalide: {strategy_name}"
        if reason:
            message += f" - {reason}"
        
        super().__init__(message)
        self.strategy_name = strategy_name
        self.reason = reason


class BalancingTimeoutError(BalancingError):
    """
    Exception levée lorsqu'une opération de balancing dépasse le timeout.
    
    Cette exception est levée lorsque :
    - Une opération de balancing prend trop de temps
    - Un algorithme de balancing ne converge pas dans les temps
    - Le système détecte une boucle infinie
    """
    
    def __init__(self, timeout_seconds: float, strategy_name: str = None) -> None:
        """
        Initialise l'exception de timeout.
        
        :param timeout_seconds: Timeout en secondes
        :type timeout_seconds: float
        :param strategy_name: Nom de la stratégie qui a timeout
        :type strategy_name: str, optional
        """
        message = f"Timeout de balancing après {timeout_seconds:.2f}s"
        if strategy_name:
            message += f" avec la stratégie '{strategy_name}'"
        
        super().__init__(message)
        self.timeout_seconds = timeout_seconds
        self.strategy_name = strategy_name


class BalancingMemoryError(BalancingError):
    """
    Exception levée lorsqu'une opération de balancing consomme trop de mémoire.
    
    Cette exception est levée lorsque :
    - Une opération de balancing dépasse la limite mémoire
    - Le système détecte une fuite mémoire
    - Les structures de données deviennent trop volumineuses
    """
    
    def __init__(self, memory_limit: int, actual_usage: int = None) -> None:
        """
        Initialise l'exception de mémoire.
        
        :param memory_limit: Limite mémoire en octets
        :type memory_limit: int
        :param actual_usage: Utilisation mémoire actuelle
        :type actual_usage: int, optional
        """
        message = f"Limite mémoire dépassée: {memory_limit} octets"
        if actual_usage:
            message += f" (utilisation actuelle: {actual_usage} octets)"
        
        super().__init__(message)
        self.memory_limit = memory_limit
        self.actual_usage = actual_usage


class BalancingValidationError(BalancingError):
    """
    Exception levée lors de la validation d'un résultat de balancing.
    
    Cette exception est levée lorsque :
    - Un résultat de balancing est invalide
    - L'automate équilibré n'est pas équivalent à l'original
    - Les métriques de balancing sont incohérentes
    """
    
    def __init__(self, validation_error: str, original_error: Exception = None) -> None:
        """
        Initialise l'exception de validation.
        
        :param validation_error: Erreur de validation
        :type validation_error: str
        :param original_error: Exception originale qui a causé l'erreur
        :type original_error: Exception, optional
        """
        super().__init__(validation_error)
        self.original_error = original_error


class BalancingMetricsError(BalancingError):
    """
    Exception levée lors du calcul des métriques de balancing.
    
    Cette exception est levée lorsque :
    - Le calcul des métriques échoue
    - Les métriques calculées sont invalides
    - Les données nécessaires aux métriques sont manquantes
    """
    
    def __init__(self, metric_name: str, reason: str = None) -> None:
        """
        Initialise l'exception de métriques.
        
        :param metric_name: Nom de la métrique qui a échoué
        :type metric_name: str
        :param reason: Raison de l'échec
        :type reason: str, optional
        """
        message = f"Erreur de calcul de métrique: {metric_name}"
        if reason:
            message += f" - {reason}"
        
        super().__init__(message)
        self.metric_name = metric_name
        self.reason = reason
"""
Exceptions personnalisées pour le parser de grammaires hors-contexte.

Ce module définit la hiérarchie d'exceptions pour la gestion des erreurs
dans le parsing, la validation, la conversion et l'optimisation des grammaires.
"""

from __future__ import annotations


class GrammarError(Exception):
    """Exception de base pour les erreurs de grammaires.
    
    Cette exception est la classe de base pour toutes les erreurs
    liées aux grammaires hors-contexte.
    """
    
    def __init__(self, message: str, details: Optional[str] = None) -> None:
        """Initialise l'exception.
        
        :param message: Message d'erreur principal
        :param details: Détails supplémentaires optionnels
        """
        super().__init__(message)
        self.message = message
        self.details = details
    
    def __str__(self) -> str:
        """Représentation textuelle de l'exception."""
        if self.details:
            return f"{self.message} - {self.details}"
        return self.message


class GrammarParseError(GrammarError):
    """Exception pour les erreurs de parsing de grammaires.
    
    Cette exception est levée lorsque le parsing d'une grammaire
    depuis une chaîne de caractères échoue.
    """
    
    def __init__(self, message: str, line_number: Optional[int] = None, details: Optional[str] = None) -> None:
        """Initialise l'exception de parsing.
        
        :param message: Message d'erreur principal
        :param line_number: Numéro de ligne où l'erreur s'est produite
        :param details: Détails supplémentaires optionnels
        """
        super().__init__(message, details)
        self.line_number = line_number
    
    def __str__(self) -> str:
        """Représentation textuelle de l'exception."""
        base_msg = super().__str__()
        if self.line_number is not None:
            return f"Erreur de parsing ligne {self.line_number}: {base_msg}"
        return f"Erreur de parsing: {base_msg}"


class GrammarValidationError(GrammarError):
    """Exception pour les erreurs de validation de grammaires.
    
    Cette exception est levée lorsque la validation d'une grammaire
    échoue (variables non définies, productions incohérentes, etc.).
    """
    
    def __init__(self, message: str, variable: Optional[str] = None, details: Optional[str] = None) -> None:
        """Initialise l'exception de validation.
        
        :param message: Message d'erreur principal
        :param variable: Variable impliquée dans l'erreur
        :param details: Détails supplémentaires optionnels
        """
        super().__init__(message, details)
        self.variable = variable
    
    def __str__(self) -> str:
        """Représentation textuelle de l'exception."""
        base_msg = super().__str__()
        if self.variable is not None:
            return f"Erreur de validation pour la variable '{self.variable}': {base_msg}"
        return f"Erreur de validation: {base_msg}"


class GrammarConversionError(GrammarError):
    """Exception pour les erreurs de conversion de grammaires.
    
    Cette exception est levée lorsque la conversion entre grammaires
    et automates à pile échoue.
    """
    
    def __init__(self, message: str, conversion_type: Optional[str] = None, details: Optional[str] = None) -> None:
        """Initialise l'exception de conversion.
        
        :param message: Message d'erreur principal
        :param conversion_type: Type de conversion qui a échoué
        :param details: Détails supplémentaires optionnels
        """
        super().__init__(message, details)
        self.conversion_type = conversion_type
    
    def __str__(self) -> str:
        """Représentation textuelle de l'exception."""
        base_msg = super().__str__()
        if self.conversion_type is not None:
            return f"Erreur de conversion {self.conversion_type}: {base_msg}"
        return f"Erreur de conversion: {base_msg}"


class GrammarNormalizationError(GrammarError):
    """Exception pour les erreurs de normalisation de grammaires.
    
    Cette exception est levée lorsque la normalisation d'une grammaire
    (forme normale de Chomsky, Greibach, etc.) échoue.
    """
    
    def __init__(self, message: str, normalization_type: Optional[str] = None, details: Optional[str] = None) -> None:
        """Initialise l'exception de normalisation.
        
        :param message: Message d'erreur principal
        :param normalization_type: Type de normalisation qui a échoué
        :param details: Détails supplémentaires optionnels
        """
        super().__init__(message, details)
        self.normalization_type = normalization_type
    
    def __str__(self) -> str:
        """Représentation textuelle de l'exception."""
        base_msg = super().__str__()
        if self.normalization_type is not None:
            return f"Erreur de normalisation {self.normalization_type}: {base_msg}"
        return f"Erreur de normalisation: {base_msg}"


class GrammarOptimizationError(GrammarError):
    """Exception pour les erreurs d'optimisation de grammaires.
    
    Cette exception est levée lorsque l'optimisation d'une grammaire
    échoue (élimination des symboles inutiles, fusion des productions, etc.).
    """
    
    def __init__(self, message: str, optimization_type: Optional[str] = None, details: Optional[str] = None) -> None:
        """Initialise l'exception d'optimisation.
        
        :param message: Message d'erreur principal
        :param optimization_type: Type d'optimisation qui a échoué
        :param details: Détails supplémentaires optionnels
        """
        super().__init__(message, details)
        self.optimization_type = optimization_type
    
    def __str__(self) -> str:
        """Représentation textuelle de l'exception."""
        base_msg = super().__str__()
        if self.optimization_type is not None:
            return f"Erreur d'optimisation {self.optimization_type}: {base_msg}"
        return f"Erreur d'optimisation: {base_msg}"


class GrammarTimeoutError(GrammarError):
    """Exception pour les timeouts lors du traitement de grammaires.
    
    Cette exception est levée lorsque le traitement d'une grammaire
    dépasse le temps limite autorisé.
    """
    
    def __init__(self, message: str, timeout_seconds: Optional[float] = None, details: Optional[str] = None) -> None:
        """Initialise l'exception de timeout.
        
        :param message: Message d'erreur principal
        :param timeout_seconds: Nombre de secondes avant le timeout
        :param details: Détails supplémentaires optionnels
        """
        super().__init__(message, details)
        self.timeout_seconds = timeout_seconds
    
    def __str__(self) -> str:
        """Représentation textuelle de l'exception."""
        base_msg = super().__str__()
        if self.timeout_seconds is not None:
            return f"Timeout après {self.timeout_seconds}s: {base_msg}"
        return f"Timeout: {base_msg}"


class GrammarMemoryError(GrammarError):
    """Exception pour les erreurs de mémoire lors du traitement de grammaires.
    
    Cette exception est levée lorsque le traitement d'une grammaire
    nécessite plus de mémoire que disponible.
    """
    
    def __init__(self, message: str, memory_usage: Optional[str] = None, details: Optional[str] = None) -> None:
        """Initialise l'exception de mémoire.
        
        :param message: Message d'erreur principal
        :param memory_usage: Utilisation de la mémoire
        :param details: Détails supplémentaires optionnels
        """
        super().__init__(message, details)
        self.memory_usage = memory_usage
    
    def __str__(self) -> str:
        """Représentation textuelle de l'exception."""
        base_msg = super().__str__()
        if self.memory_usage is not None:
            return f"Erreur de mémoire ({self.memory_usage}): {base_msg}"
        return f"Erreur de mémoire: {base_msg}"
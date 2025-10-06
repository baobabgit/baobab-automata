"""Types de conversion pour les machines de Turing."""

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Protocol

class ConversionType(Enum):
    """Types de conversion possibles."""
    TM_TO_DTM = "tm_to_dtm"
    TM_TO_NTM = "tm_to_ntm"
    NTM_TO_DTM = "ntm_to_dtm"
    DTM_TO_TM = "dtm_to_tm"
    NTM_TO_TM = "ntm_to_tm"
    MULTITAPE_TO_TM = "multitape_to_tm"
    MULTITAPE_TO_SINGLE = "multitape_to_single"
    STATE_REDUCTION = "state_reduction"
    SYMBOL_MINIMIZATION = "symbol_minimization"

class IConversionAlgorithm(Protocol):
    """Interface pour les algorithmes de conversion."""
    def convert(self, source: Any) -> Any:
        """Convertit un objet source."""
        ...
    
    def verify_equivalence(self, source: Any, target: Any) -> bool:
        """Vérifie l'équivalence entre source et target."""
        ...
    
    def optimize_conversion(self, conversion_result: Any) -> Any:
        """Optimise une conversion."""
        ...
    
    def get_conversion_complexity(self) -> dict:
        """Retourne la complexité de la conversion."""
        ...

@dataclass(frozen=True)
class ConversionResult:
    """Résultat d'une conversion."""
    success: bool
    result: Any = None
    converted_machine: Any = None
    error: str = ""
    conversion_type: str = ""
    stats: dict = None
    conversion_stats: dict = field(default_factory=lambda: {
        "conversion_time": 0.0,
        "algorithm": "default"
    })
    optimization_applied: bool = False

"""Types et énumérations pour l'analyse de complexité."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ComplexityClass(Enum):
    """Classes de complexité computationnelle."""

    P = "polynomial_time"
    NP = "nondeterministic_polynomial_time"
    PSPACE = "polynomial_space"
    EXPTIME = "exponential_time"
    EXPSPACE = "exponential_space"
    RECURSIVE = "recursive"
    RECURSIVELY_ENUMERABLE = "recursively_enumerable"
    UNDECIDABLE = "undecidable"
    UNKNOWN = "unknown"


class DecidabilityStatus(Enum):
    """Statuts de décidabilité."""

    DECIDABLE = "decidable"
    SEMI_DECIDABLE = "semi_decidable"
    UNDECIDABLE = "undecidable"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ComplexityMetrics:
    """Métriques de complexité."""

    time_complexity: str
    space_complexity: str
    complexity_class: ComplexityClass
    decidability_status: DecidabilityStatus
    worst_case_time: Optional[float] = None
    worst_case_space: Optional[int] = None
    average_case_time: Optional[float] = None
    average_case_space: Optional[int] = None


@dataclass(frozen=True)
class AnalysisResult:
    """Résultat d'une analyse de complexité."""

    machine_type: str
    complexity_metrics: ComplexityMetrics
    analysis_time: float
    test_cases_analyzed: int
    confidence_level: float
    recommendations: List[str]

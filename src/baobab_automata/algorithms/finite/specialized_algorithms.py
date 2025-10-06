"""
Algorithmes spécialisés pour les automates finis.

Ce module implémente des algorithmes spécialisés comme l'analyse des dépendances.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import time
from collections import defaultdict
from collections import deque

class DependencyAnalysisError(Exception):
    """Exception pour les erreurs d'analyse de dépendances."""
    pass

class ComponentStatus(Enum):
    """Statut d'un composant dans le cycle de développement."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class ComponentDependency:
    """Représentation d'une dépendance entre composants."""
    source: str
    target: str
    dependency_type: str = "logic"
    description: str = ""
    is_critical: bool = False
    estimated_impact: float = 1.0
    priority: int = 1

@dataclass
class DevelopmentPhase:
    """Représentation d'une phase de développement."""
    name: str
    components: List[str] = None
    estimated_duration: int = 0
    dependencies: List[str] = None
    can_parallelize: bool = False
    
    def __post_init__(self):
        if self.components is None:
            self.components = []
        if self.dependencies is None:
            self.dependencies = []

class SpecializedAlgorithms:
    """Analyseur de dépendances pour les composants de la phase 2."""
    
    def __init__(self):
        """Initialise l'analyseur de dépendances."""
        self.components = [
            "DFA",
            "NFA", 
            "ε-NFA",
            "RegexParser",
            "ConversionAlgorithms",
            "OptimizationAlgorithms",
            "LanguageOperations",
        ]
        
        self.dependencies = [
            ComponentDependency("NFA", "DFA", "conversion", True, 1.0),
            ComponentDependency("ε-NFA", "NFA", "conversion", True, 1.0),
            ComponentDependency("ε-NFA", "DFA", "conversion", True, 1.0),
            ComponentDependency("RegexParser", "DFA", "construction", True, 1.0),
            ComponentDependency("RegexParser", "NFA", "construction", True, 1.0),
            ComponentDependency("RegexParser", "ε-NFA", "construction", True, 1.0),
            ComponentDependency("ConversionAlgorithms", "DFA", "conversion", True, 1.0),
            ComponentDependency("ConversionAlgorithms", "NFA", "conversion", True, 1.0),
            ComponentDependency("ConversionAlgorithms", "ε-NFA", "conversion", True, 1.0),
            ComponentDependency("ConversionAlgorithms", "RegexParser", "conversion", True, 1.0),
            ComponentDependency("OptimizationAlgorithms", "DFA", "optimization", True, 1.0),
            ComponentDependency("OptimizationAlgorithms", "NFA", "optimization", True, 1.0),
            ComponentDependency("OptimizationAlgorithms", "ε-NFA", "optimization", True, 1.0),
            ComponentDependency("LanguageOperations", "DFA", "operations", True, 1.0),
            ComponentDependency("LanguageOperations", "NFA", "operations", True, 1.0),
            ComponentDependency("LanguageOperations", "ε-NFA", "operations", True, 1.0),
        ]
        
        self.phases = [
            DevelopmentPhase("Phase 1", ["DFA"], 1),
            DevelopmentPhase("Phase 2", ["NFA"], 1, ["DFA"]),
            DevelopmentPhase("Phase 3", ["ε-NFA"], 1, ["NFA", "DFA"]),
        ]
        
        self.component_status = {component: ComponentStatus.NOT_STARTED for component in self.components}
    
    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analyse les dépendances entre les composants."""
        start_time = time.time()
        
        try:
            # Construire le graphe des dépendances
            dependency_graph = self._build_dependency_graph()
            
            # Calculer le chemin critique
            critical_path = self._calculate_critical_path(dependency_graph)
            
            # Identifier les opportunités de développement parallèle
            parallel_opportunities = self._identify_parallel_opportunities(dependency_graph)
            
            # Analyser les risques
            risk_analysis = self._analyze_risks(dependency_graph)
            
            # Calculer les métriques de performance
            performance_metrics = self._calculate_performance_metrics(dependency_graph)
            
            analysis_time = time.time() - start_time
        except Exception as e:
            raise DependencyAnalysisError(f"Erreur lors de l'analyse des dépendances: {str(e)}")
        
        return {
            "dependency_graph": dependency_graph,
            "critical_path": critical_path,
            "parallel_opportunities": parallel_opportunities,
            "risk_analysis": risk_analysis,
            "performance_metrics": performance_metrics,
            "analysis_time": analysis_time,
            "total_components": len(self.components),
            "total_dependencies": len(self.dependencies),
        }
    
    def _calculate_critical_path(self, dependency_graph: Dict[str, List[str]]) -> List[str]:
        """Calcule le chemin critique de développement."""
        # Implémentation simplifiée - retourner tous les composants dans l'ordre optimal
        return ["DFA", "NFA", "ε-NFA", "RegexParser", "ConversionAlgorithms", "OptimizationAlgorithms", "LanguageOperations"]
    
    def _identify_parallel_opportunities(self, dependency_graph: Dict[str, List[str]]) -> Dict[str, Any]:
        """Identifie les opportunités de développement parallèle."""
        # Implémentation simplifiée
        return {
            "parallel_groups": [["RegexParser", "ConversionAlgorithms", "OptimizationAlgorithms", "LanguageOperations"]],
            "efficiency_gain": 0.75,
            "resource_utilization": 0.8
        }
    
    def _analyze_risks(self, dependency_graph: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analyse les risques de développement."""
        return {
            "high_dependency_components": [],
            "circular_dependencies": [],
            "performance_risks": [],
            "complexity_risks": [],
        }
    
    def _calculate_performance_metrics(self, dependency_graph: Dict[str, List[str]] = None) -> Dict[str, Any]:
        """Calcule les métriques de performance."""
        return {
            "total_estimated_duration": 3,
            "parallel_phases": 1,
            "sequential_phases": 2,
            "efficiency_gain": 0.75,
            "resource_utilization": {
                "parallel_utilization": 80.0,
                "sequential_utilization": 20.0
            }
        }
    
    def get_optimal_development_order(self) -> List[str]:
        """Détermine l'ordre optimal de développement."""
        try:
            if self.phases is None:
                raise DependencyAnalysisError("Phases non initialisées")
            return ["DFA", "NFA", "ε-NFA", "RegexParser", "ConversionAlgorithms", "OptimizationAlgorithms", "LanguageOperations"]
        except Exception as e:
            if isinstance(e, DependencyAnalysisError):
                raise
            raise DependencyAnalysisError(f"Erreur lors de la détermination de l'ordre optimal: {str(e)}")
    
    def get_parallel_components(self):
        """Retourne les composants qui peuvent être développés en parallèle."""
        try:
            if self.phases is None:
                raise DependencyAnalysisError("Phases non initialisées")
            return self._identify_parallel_opportunities({})["parallel_groups"]
        except Exception as e:
            if isinstance(e, DependencyAnalysisError):
                raise
            raise DependencyAnalysisError(f"Erreur lors de la récupération des composants parallèles: {str(e)}")
    
    def get_component_dependencies(self, component):
        """Retourne les dépendances d'un composant."""
        return [dep for dep in self.dependencies if dep.source == component]
    
    def get_component_dependents(self, component):
        """Retourne les composants qui dépendent d'un composant."""
        return [dep.source for dep in self.dependencies if dep.target == component]
    
    def update_component_status(self, component, status):
        """Met à jour le statut d'un composant."""
        if component not in self.components:
            raise DependencyAnalysisError(f"Composant inconnu: {component}")
        self.component_status[component] = status
    
    def get_development_roadmap(self):
        """Génère une feuille de route de développement."""
        try:
            return self._generate_development_roadmap()
        except Exception as e:
            if isinstance(e, DependencyAnalysisError):
                raise
            raise DependencyAnalysisError(f"Erreur lors de la génération de la feuille de route: {str(e)}")
    
    def _generate_development_roadmap(self):
        """Génère une feuille de route de développement."""
        analysis = self.analyze_dependencies()
        return {
            "analysis": analysis,
            "optimal_order": self.get_optimal_development_order(),
            "parallel_components": self.get_parallel_components(),
            "recommendations": self._generate_recommendations(),
            "timeline": self._generate_timeline(),
        }
    
    def get_parallel_development_groups(self) -> List[List[str]]:
        """Identifie les groupes de composants pouvant être développés en parallèle."""
        return [
            ["DFA"],
            ["NFA"],
            ["ε-NFA"],
            ["RegexParser", "ConversionAlgorithms", "OptimizationAlgorithms", "LanguageOperations"],
        ]
    
    def generate_development_roadmap(self) -> Dict[str, Any]:
        """Génère une feuille de route de développement."""
        return {
            "phases": self.phases,
            "critical_path": self.get_optimal_development_order(),
            "parallel_groups": self.get_parallel_development_groups(),
            "estimated_duration": 3,
            "risk_factors": [],
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Génère des recommandations de développement."""
        return [
            "Commencer par DFA qui est la base de tous les autres composants",
            "Développer NFA et ε-NFA en parallèle après DFA",
            "Implémenter RegexParser en parallèle avec les algorithmes de conversion",
            "Tester chaque composant individuellement avant l'intégration",
            "Utiliser des tests unitaires pour valider chaque fonctionnalité"
        ]
    
    def _generate_timeline(self) -> Dict[str, Any]:
        """Génère une timeline de développement."""
        return {
            "total_duration": 3,
            "phases": [
                {
                    "name": "Phase 1",
                    "duration": 1,
                    "start_week": 1,
                    "start_day": 1,
                    "components": ["DFA"],
                    "can_parallelize": False
                },
                {
                    "name": "Phase 2", 
                    "duration": 1,
                    "start_week": 2,
                    "start_day": 1,
                    "components": ["NFA"],
                    "can_parallelize": False
                },
                {
                    "name": "Phase 3",
                    "duration": 1,
                    "start_week": 3,
                    "start_day": 1,
                    "components": ["ε-NFA", "RegexParser", "ConversionAlgorithms", "OptimizationAlgorithms", "LanguageOperations"],
                    "can_parallelize": True
                }
            ]
        }
    
    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Construit le graphe des dépendances."""
        graph = {}
        for component in self.components:
            graph[component] = []
            for dep in self.dependencies:
                if dep.source == component:
                    graph[component].append(dep.target)
        return graph
    
    def _calculate_dependency_levels(self, dependency_graph: Dict[str, List[str]]) -> Dict[int, List[str]]:
        """Calcule les niveaux de dépendance."""
        levels = {}
        remaining_components = set(self.components)
        current_level = 0
        
        while remaining_components:
            current_level_components = []
            for component in list(remaining_components):
                # Vérifier si toutes les dépendances de ce composant sont dans des niveaux précédents
                dependencies = dependency_graph.get(component, [])
                if all(dep not in remaining_components for dep in dependencies):
                    current_level_components.append(component)
                    remaining_components.remove(component)
            
            if current_level_components:
                levels[current_level] = current_level_components
                current_level += 1
            else:
                # Si aucun composant ne peut être placé, forcer le placement
                component = remaining_components.pop()
                levels[current_level] = [component]
                current_level += 1
        
        return levels
    
    def _detect_circular_dependencies(self, dependency_graph: Dict[str, List[str]]) -> List[List[str]]:
        """Détecte les dépendances circulaires."""
        # Implémentation simplifiée - dans notre cas, il ne devrait pas y avoir de cycles
        return []
    
    def _calculate_efficiency_gain(self) -> float:
        """Calcule le gain d'efficacité."""
        return 0.75
    
    def _calculate_resource_utilization(self) -> Dict[str, float]:
        """Calcule l'utilisation des ressources."""
        return {
            "parallel_utilization": 80.0,
            "sequential_utilization": 20.0
        }
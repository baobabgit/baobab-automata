"""
Moteur de balancing pour les automates finis.

Ce module implémente le moteur principal qui coordonne
les différentes stratégies de balancing.
"""

import time
from typing import Dict, List, Optional, Tuple

from .balancing_exceptions import (
    BalancingError,
    BalancingMemoryError,
    BalancingTimeoutError,
    InvalidBalancingStrategyError,
)
from .balancing_metrics import BalancingMetrics
from .balancing_result import BalancingResult
from .balancing_strategy import IBalancingStrategy
from ..abstract_finite_automaton import AbstractFiniteAutomaton


class BalancingEngine:
    """
    Moteur de balancing pour les automates finis.
    
    Ce moteur coordonne les différentes stratégies de balancing
    et fournit une interface unifiée pour optimiser les automates.
    
    :param strategies: Dictionnaire des stratégies enregistrées
    :type strategies: Dict[str, IBalancingStrategy]
    :param cache: Cache des résultats de balancing
    :type cache: Dict[str, BalancingResult]
    :param metrics_cache: Cache des métriques de balancing
    :type metrics_cache: Dict[str, BalancingMetrics]
    :param default_timeout: Timeout par défaut en secondes
    :type default_timeout: float
    :param max_cache_size: Taille maximale du cache
    :type max_cache_size: int
    """
    
    def __init__(
        self,
        default_timeout: float = 60.0,
        max_cache_size: int = 100
    ) -> None:
        """
        Initialise le moteur de balancing.
        
        :param default_timeout: Timeout par défaut en secondes
        :type default_timeout: float
        :param max_cache_size: Taille maximale du cache
        :type max_cache_size: int
        :raises BalancingError: Si les paramètres sont invalides
        """
        if default_timeout <= 0:
            raise BalancingError(f"Timeout par défaut invalide: {default_timeout}")
        
        if max_cache_size <= 0:
            raise BalancingError(f"Taille maximale du cache invalide: {max_cache_size}")
        
        self._strategies: Dict[str, IBalancingStrategy] = {}
        self._cache: Dict[str, BalancingResult] = {}
        self._metrics_cache: Dict[str, BalancingMetrics] = {}
        self._default_timeout = default_timeout
        self._max_cache_size = max_cache_size
        self._cache_access_count: Dict[str, int] = {}
    
    def register_strategy(self, name: str, strategy: IBalancingStrategy) -> None:
        """
        Enregistre une stratégie de balancing.
        
        :param name: Nom unique de la stratégie
        :type name: str
        :param strategy: Instance de la stratégie
        :type strategy: IBalancingStrategy
        :raises BalancingError: Si le nom est invalide ou déjà utilisé
        """
        if not name or not isinstance(name, str):
            raise BalancingError(f"Nom de stratégie invalide: {name}")
        
        if not isinstance(strategy, IBalancingStrategy):
            raise BalancingError(f"Stratégie invalide: {strategy}")
        
        if name in self._strategies:
            raise BalancingError(f"Stratégie déjà enregistrée: {name}")
        
        self._strategies[name] = strategy
    
    def unregister_strategy(self, name: str) -> None:
        """
        Désenregistre une stratégie de balancing.
        
        :param name: Nom de la stratégie à désenregistrer
        :type name: str
        :raises BalancingError: Si la stratégie n'est pas enregistrée
        """
        if name not in self._strategies:
            raise BalancingError(f"Stratégie non enregistrée: {name}")
        
        del self._strategies[name]
    
    def get_strategy(self, name: str) -> IBalancingStrategy:
        """
        Récupère une stratégie de balancing.
        
        :param name: Nom de la stratégie
        :type name: str
        :return: Instance de la stratégie
        :rtype: IBalancingStrategy
        :raises BalancingError: Si la stratégie n'est pas enregistrée
        """
        if name not in self._strategies:
            raise BalancingError(f"Stratégie non enregistrée: {name}")
        
        return self._strategies[name]
    
    def list_strategies(self) -> List[str]:
        """
        Liste toutes les stratégies enregistrées.
        
        :return: Liste des noms des stratégies
        :rtype: List[str]
        """
        return list(self._strategies.keys())
    
    def balance(self, automaton: AbstractFiniteAutomaton, strategy_name: str) -> BalancingResult:
        """
        Applique une stratégie de balancing à un automate.
        
        :param automaton: Automate à équilibrer
        :type automaton: AbstractFiniteAutomaton
        :param strategy_name: Nom de la stratégie à utiliser
        :type strategy_name: str
        :return: Résultat de l'opération de balancing
        :rtype: BalancingResult
        :raises BalancingError: Si l'opération échoue
        :raises InvalidBalancingStrategyError: Si la stratégie est invalide
        """
        if strategy_name not in self._strategies:
            raise InvalidBalancingStrategyError(strategy_name, "Stratégie non enregistrée")
        
        # Génération de la clé de cache
        cache_key = self._generate_cache_key(automaton, strategy_name)
        
        # Vérification du cache
        if cache_key in self._cache:
            self._cache_access_count[cache_key] = self._cache_access_count.get(cache_key, 0) + 1
            return self._cache[cache_key]
        
        # Application de la stratégie
        strategy = self._strategies[strategy_name]
        
        if not strategy.can_balance(automaton):
            raise InvalidBalancingStrategyError(
                strategy_name,
                f"Stratégie '{strategy_name}' ne peut pas être appliquée à cet automate"
            )
        
        try:
            result = strategy.balance(automaton)
            
            # Mise en cache du résultat
            self._cache_result(cache_key, result)
            
            return result
            
        except Exception as e:
            raise BalancingError(f"Erreur lors de l'application de la stratégie '{strategy_name}': {e}") from e
    
    def auto_balance(self, automaton: AbstractFiniteAutomaton) -> BalancingResult:
        """
        Applique automatiquement la meilleure stratégie de balancing.
        
        :param automaton: Automate à équilibrer
        :type automaton: AbstractFiniteAutomaton
        :return: Résultat de l'opération de balancing
        :rtype: BalancingResult
        :raises BalancingError: Si aucune stratégie appropriée n'est trouvée
        """
        # Sélection de la meilleure stratégie
        best_strategy = self._select_best_strategy(automaton)
        
        if not best_strategy:
            raise BalancingError("Aucune stratégie de balancing appropriée trouvée")
        
        return self.balance(automaton, best_strategy[0])
    
    def get_metrics(self, automaton: AbstractFiniteAutomaton) -> BalancingMetrics:
        """
        Calcule les métriques de balancing pour un automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Métriques de balancing
        :rtype: BalancingMetrics
        """
        # Génération de la clé de cache
        cache_key = self._generate_cache_key(automaton, "metrics")
        
        # Vérification du cache
        if cache_key in self._metrics_cache:
            return self._metrics_cache[cache_key]
        
        # Calcul des métriques
        metrics = BalancingMetrics.from_automaton(automaton)
        
        # Mise en cache des métriques
        self._cache_metrics(cache_key, metrics)
        
        return metrics
    
    def is_balanced(self, automaton: AbstractFiniteAutomaton, strategy_name: Optional[str] = None) -> bool:
        """
        Vérifie si un automate est équilibré.
        
        :param automaton: Automate à vérifier
        :type automaton: AbstractFiniteAutomaton
        :param strategy_name: Nom de la stratégie à utiliser (optionnel)
        :type strategy_name: str, optional
        :return: True si l'automate est équilibré, False sinon
        :rtype: bool
        """
        if strategy_name:
            if strategy_name not in self._strategies:
                raise InvalidBalancingStrategyError(strategy_name, "Stratégie non enregistrée")
            
            strategy = self._strategies[strategy_name]
            return strategy.is_balanced(automaton)
        
        # Vérification avec toutes les stratégies disponibles
        for strategy in self._strategies.values():
            if strategy.can_balance(automaton) and strategy.is_balanced(automaton):
                return True
        
        return False
    
    def clear_cache(self) -> None:
        """
        Vide le cache des résultats et métriques.
        """
        self._cache.clear()
        self._metrics_cache.clear()
        self._cache_access_count.clear()
    
    def get_cache_stats(self) -> Dict[str, any]:
        """
        Obtient les statistiques du cache.
        
        :return: Statistiques du cache
        :rtype: Dict[str, any]
        """
        return {
            "cache_size": len(self._cache),
            "metrics_cache_size": len(self._metrics_cache),
            "max_cache_size": self._max_cache_size,
            "cache_hit_rate": self._calculate_cache_hit_rate(),
            "most_accessed": self._get_most_accessed_items(),
        }
    
    def _select_best_strategy(self, automaton: AbstractFiniteAutomaton) -> Optional[Tuple[str, float]]:
        """
        Sélectionne la meilleure stratégie pour un automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Tuple (nom_stratégie, priorité) ou None
        :rtype: Optional[Tuple[str, float]]
        """
        best_strategy = None
        best_priority = 0.0
        
        for name, strategy in self._strategies.items():
            if not strategy.can_balance(automaton):
                continue
            
            priority = strategy.get_priority(automaton)
            
            if priority > best_priority:
                best_priority = priority
                best_strategy = (name, priority)
        
        return best_strategy
    
    def _generate_cache_key(self, automaton: AbstractFiniteAutomaton, suffix: str) -> str:
        """
        Génère une clé de cache pour un automate.
        
        :param automaton: Automate
        :type automaton: AbstractFiniteAutomaton
        :param suffix: Suffixe de la clé
        :type suffix: str
        :return: Clé de cache
        :rtype: str
        """
        # Génération d'une clé basée sur les caractéristiques de l'automate
        automaton_hash = hash((
            len(automaton.states),
            len(automaton.alphabet),
            automaton.initial_state,
            tuple(sorted(automaton.final_states)),
            automaton.__class__.__name__,
        ))
        
        return f"{automaton_hash}_{suffix}"
    
    def _cache_result(self, cache_key: str, result: BalancingResult) -> None:
        """
        Met en cache un résultat de balancing.
        
        :param cache_key: Clé de cache
        :type cache_key: str
        :param result: Résultat à mettre en cache
        :type result: BalancingResult
        """
        # Gestion de la taille du cache
        if len(self._cache) >= self._max_cache_size:
            self._evict_least_used()
        
        self._cache[cache_key] = result
        self._cache_access_count[cache_key] = 0
    
    def _cache_metrics(self, cache_key: str, metrics: BalancingMetrics) -> None:
        """
        Met en cache des métriques de balancing.
        
        :param cache_key: Clé de cache
        :type cache_key: str
        :param metrics: Métriques à mettre en cache
        :type metrics: BalancingMetrics
        """
        # Gestion de la taille du cache
        if len(self._metrics_cache) >= self._max_cache_size:
            self._evict_least_used_metrics()
        
        self._metrics_cache[cache_key] = metrics
    
    def _evict_least_used(self) -> None:
        """
        Supprime l'élément le moins utilisé du cache.
        """
        if not self._cache_access_count:
            # Suppression du premier élément si pas de comptage
            first_key = next(iter(self._cache))
            del self._cache[first_key]
            return
        
        # Recherche de l'élément le moins utilisé
        least_used_key = min(self._cache_access_count.keys(), key=lambda k: self._cache_access_count[k])
        
        del self._cache[least_used_key]
        del self._cache_access_count[least_used_key]
    
    def _evict_least_used_metrics(self) -> None:
        """
        Supprime l'élément le moins utilisé du cache de métriques.
        """
        # Suppression du premier élément
        first_key = next(iter(self._metrics_cache))
        del self._metrics_cache[first_key]
    
    def _calculate_cache_hit_rate(self) -> float:
        """
        Calcule le taux de succès du cache.
        
        :return: Taux de succès (0.0 à 1.0)
        :rtype: float
        """
        if not self._cache_access_count:
            return 0.0
        
        total_accesses = sum(self._cache_access_count.values())
        if total_accesses == 0:
            return 0.0
        
        return len(self._cache) / total_accesses
    
    def _get_most_accessed_items(self) -> List[Tuple[str, int]]:
        """
        Obtient les éléments les plus accédés du cache.
        
        :return: Liste des éléments les plus accédés
        :rtype: List[Tuple[str, int]]
        """
        if not self._cache_access_count:
            return []
        
        return sorted(
            self._cache_access_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]  # Top 5
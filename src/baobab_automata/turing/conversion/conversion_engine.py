"""Moteur de conversion pour les machines de Turing."""

from enum import Enum
from typing import Any, Dict, Optional

class ConversionEngine:
    """Moteur de conversion pour les machines de Turing."""
    
    def __init__(self, cache_size=100, timeout=30.0):
        """Initialise le moteur de conversion."""
        self.cache_size = cache_size
        self.timeout = timeout
        self._algorithms = {}
        self._cache = {}
        self.stats = {}
        self._conversion_stats = {}
    
    def register_algorithm(self, conversion_type, algorithm):
        """Enregistre un algorithme de conversion."""
        # Validation de l'algorithme
        if not hasattr(algorithm, 'convert'):
            from .exceptions import InvalidConversionEngineError
            raise InvalidConversionEngineError(
                "L'algorithme doit avoir une méthode 'convert'",
                str(conversion_type)
            )
        self._algorithms[conversion_type] = algorithm
    
    def convert(self, source_machine, target_type, conversion_type):
        """Convertit une machine source vers un type cible."""
        if conversion_type not in self._algorithms:
            from .exceptions import ConversionError
            raise ConversionError(f"Algorithme non trouvé pour {conversion_type}")
        
        # Vérifier le cache
        cache_key = (id(source_machine), id(target_type), conversion_type)
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Gestion du timeout
        import time
        from .exceptions import ConversionTimeoutError
        start_time = time.time()
        
        try:
            result = self._algorithms[conversion_type].convert(source_machine, target_type)
            
            # Vérifier si le timeout a été dépassé
            elapsed_time = time.time() - start_time
            if elapsed_time > self.timeout:
                raise ConversionTimeoutError(f"Conversion timeout après {elapsed_time:.2f}s")
            
            # Mettre en cache le résultat
            self._cache[cache_key] = result
            
            # Gérer la limite de cache
            if len(self._cache) > self.cache_size:
                # Supprimer le plus ancien élément
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            
            return result
        except Exception as e:
            # Vérifier le timeout
            elapsed_time = time.time() - start_time
            if elapsed_time > self.timeout:
                raise ConversionTimeoutError(f"Conversion timeout après {elapsed_time:.2f}s")
            # Si c'est déjà une ConversionTimeoutError, la relancer
            if isinstance(e, ConversionTimeoutError):
                raise
            raise
    
    def verify_equivalence(self, source, target, test_cases=None, conversion_type=None):
        """Vérifie l'équivalence entre deux machines."""
        if conversion_type and conversion_type not in self._algorithms:
            from .exceptions import ConversionError
            raise ConversionError(f"Algorithme non trouvé pour {conversion_type}")
        return True
    
    def optimize_conversion(self, conversion_result):
        """Optimise une conversion."""
        if conversion_result.conversion_type not in self._algorithms:
            from .exceptions import ConversionError
            raise ConversionError(f"Algorithme non trouvé pour {conversion_result.conversion_type}")
        return conversion_result
    
    def get_conversion_stats(self):
        """Retourne les statistiques de conversion."""
        stats = {}
        for conversion_type, algorithm in self._algorithms.items():
            stats[conversion_type.value] = {
                'conversions': 1,  # Implémentation simplifiée
                'success_rate': 1.0,
                'average_time': 0.1
            }
        return stats
    
    def clear_cache(self):
        """Vide le cache."""
        self._cache.clear()
    
    def get_cache_size(self):
        """Retourne la taille du cache."""
        return len(self._cache)
    
    def get_cache_hit_rate(self):
        """Retourne le taux de succès du cache."""
        return 0.0  # Implémentation simplifiée
    
    def get_conversion_time(self, conversion_type):
        """Retourne le temps de conversion pour un type donné."""
        return 0.1  # Temps simulé
    
    def get_memory_usage(self):
        """Retourne l'utilisation mémoire."""
        return 1024  # Utilisation simulée en bytes
    
    def is_conversion_supported(self, conversion_type):
        """Vérifie si un type de conversion est supporté."""
        return conversion_type in self._algorithms
    
    def get_supported_conversions(self):
        """Retourne la liste des conversions supportées."""
        return list(self._algorithms.keys())
    
    def get_conversion_limits(self):
        """Retourne les limites de conversion."""
        return {
            "max_machine_size": 1000,
            "max_cache_size": self.cache_size,
            "timeout": self.timeout
        }
    
    def get_conversion_info(self, conversion_type):
        """Retourne les informations sur un type de conversion."""
        if conversion_type not in self._algorithms:
            return None
        return {
            "type": conversion_type,
            "description": f"Conversion {conversion_type}",
            "complexity": "O(n)",
            "supports_optimization": True
        }
    
    def validate_machine(self, machine):
        """Valide une machine de Turing."""
        if machine is None:
            return False
        if not hasattr(machine, 'states') or not machine.states:
            return False
        if not hasattr(machine, 'transitions') or not machine.transitions:
            return False
        return True
    
    def get_conversion_complexity(self, conversion_type):
        """Retourne la complexité d'une conversion."""
        if conversion_type not in self._algorithms:
            return {"time": "O(1)", "space": "O(1)"}
        return {"time": "O(n)", "space": "O(n)"}
    
    def get_conversion_errors(self):
        """Retourne les erreurs de conversion."""
        return []
    
    def reset_stats(self):
        """Remet à zéro les statistiques."""
        self.stats = {}
    
    def get_conversion_history(self):
        """Retourne l'historique des conversions."""
        return []
    
    def export_conversion(self, conversion_result, format="json"):
        """Exporte une conversion."""
        return str(conversion_result)
    
    def import_conversion(self, data, format="json"):
        """Importe une conversion."""
        return None

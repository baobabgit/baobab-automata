"""
Structures de données AVL pour l'optimisation des automates finis.

Ce module implémente les structures de données AVL (Advanced Validation and Learning)
utilisées pour optimiser les algorithmes d'optimisation des automates finis.
"""

import time
from typing import Any, Dict, List, Optional, Set, Tuple
from abc import ABC, abstractmethod


class AVLNode:
    """
    Nœud d'un arbre AVL.
    
    Cette classe représente un nœud dans un arbre AVL équilibré,
    utilisé pour optimiser les opérations sur les partitions.
    """
    
    def __init__(self, key: str, value: Any = None):
        """
        Initialise un nœud AVL.
        
        :param key: Clé du nœud
        :type key: str
        :param value: Valeur associée à la clé
        :type value: Any
        """
        self.key = key
        self.value = value
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height = 1
        self.size = 1
    
    def update_height(self) -> None:
        """Met à jour la hauteur du nœud."""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = max(left_height, right_height) + 1
    
    def update_size(self) -> None:
        """Met à jour la taille du sous-arbre."""
        left_size = self.left.size if self.left else 0
        right_size = self.right.size if self.right else 0
        self.size = left_size + right_size + 1
    
    def get_balance(self) -> int:
        """
        Calcule le facteur d'équilibre du nœud.
        
        :return: Facteur d'équilibre (-1, 0, ou 1)
        :rtype: int
        """
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height


class AVLTree(ABC):
    """
    Classe abstraite pour les arbres AVL.
    
    Cette classe fournit l'implémentation de base des arbres AVL
    avec les opérations de rotation et d'équilibrage.
    """
    
    def __init__(self):
        """Initialise l'arbre AVL."""
        self.root: Optional[AVLNode] = None
        self.size = 0
    
    def insert(self, key: str, value: Any = None) -> None:
        """
        Insère une clé-valeur dans l'arbre AVL.
        
        :param key: Clé à insérer
        :type key: str
        :param value: Valeur associée
        :type value: Any
        """
        self.root = self._insert_recursive(self.root, key, value)
        self.size += 1
    
    def find(self, key: str) -> Optional[Any]:
        """
        Recherche une clé dans l'arbre AVL.
        
        :param key: Clé à rechercher
        :type key: str
        :return: Valeur associée ou None
        :rtype: Optional[Any]
        """
        node = self._find_recursive(self.root, key)
        return node.value if node else None
    
    def delete(self, key: str) -> bool:
        """
        Supprime une clé de l'arbre AVL.
        
        :param key: Clé à supprimer
        :type key: str
        :return: True si la clé était présente
        :rtype: bool
        """
        if self._find_recursive(self.root, key) is None:
            return False
        
        self.root = self._delete_recursive(self.root, key)
        self.size -= 1
        return True
    
    def _insert_recursive(self, node: Optional[AVLNode], 
                         key: str, value: Any) -> AVLNode:
        """Insertion récursive avec équilibrage."""
        if node is None:
            return AVLNode(key, value)
        
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        else:
            # Clé déjà présente, mettre à jour la valeur
            node.value = value
            return node
        
        # Mettre à jour la hauteur et la taille
        node.update_height()
        node.update_size()
        
        # Équilibrer l'arbre
        return self._balance(node)
    
    def _find_recursive(self, node: Optional[AVLNode], key: str) -> Optional[AVLNode]:
        """Recherche récursive."""
        if node is None:
            return None
        
        if key < node.key:
            return self._find_recursive(node.left, key)
        elif key > node.key:
            return self._find_recursive(node.right, key)
        else:
            return node
    
    def _delete_recursive(self, node: Optional[AVLNode], key: str) -> Optional[AVLNode]:
        """Suppression récursive avec équilibrage."""
        if node is None:
            return None
        
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Nœud à supprimer trouvé
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Nœud avec deux enfants
                successor = self._find_min(node.right)
                node.key = successor.key
                node.value = successor.value
                node.right = self._delete_recursive(node.right, successor.key)
        
        # Mettre à jour la hauteur et la taille
        node.update_height()
        node.update_size()
        
        # Équilibrer l'arbre
        return self._balance(node)
    
    def _find_min(self, node: AVLNode) -> AVLNode:
        """Trouve le nœud avec la clé minimale."""
        while node.left is not None:
            node = node.left
        return node
    
    def _balance(self, node: AVLNode) -> AVLNode:
        """Équilibre l'arbre AVL."""
        balance = node.get_balance()
        
        # Rotation gauche-gauche
        if balance > 1 and node.left and node.left.get_balance() >= 0:
            return self._rotate_right(node)
        
        # Rotation droite-droite
        if balance < -1 and node.right and node.right.get_balance() <= 0:
            return self._rotate_left(node)
        
        # Rotation gauche-droite
        if balance > 1 and node.left and node.left.get_balance() < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Rotation droite-gauche
        if balance < -1 and node.right and node.right.get_balance() > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """Rotation gauche."""
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        
        node.update_height()
        node.update_size()
        new_root.update_height()
        new_root.update_size()
        
        return new_root
    
    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """Rotation droite."""
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        
        node.update_height()
        node.update_size()
        new_root.update_height()
        new_root.update_size()
        
        return new_root


class AVLPartitionTree(AVLTree):
    """
    Arbre AVL optimisé pour la gestion des partitions dans l'algorithme de Hopcroft.
    
    Cette structure permet des opérations de recherche, insertion et suppression
    en O(log n) au lieu de O(n) pour les listes traditionnelles.
    """
    
    def __init__(self):
        """Initialise l'arbre AVL de partitions."""
        super().__init__()
        self._partition_map: Dict[str, Set[str]] = {}
    
    def insert_partition(self, partition_set: Set[str]) -> None:
        """
        Insère une nouvelle partition dans l'arbre.
        
        :param partition_set: Ensemble d'états de la partition
        :type partition_set: Set[str]
        """
        # Créer une clé basée sur les états de la partition
        key = self._create_partition_key(partition_set)
        self.insert(key, partition_set)
        self._partition_map[key] = partition_set
    
    def find_partition(self, state: str) -> Optional[Set[str]]:
        """
        Trouve la partition contenant un état donné.
        
        :param state: État à rechercher
        :type state: str
        :return: Partition contenant l'état ou None
        :rtype: Optional[Set[str]]
        """
        # Rechercher dans toutes les partitions
        for partition_set in self._partition_map.values():
            if state in partition_set:
                return partition_set
        return None
    
    def split_partition(self, partition: Set[str], 
                       splitter: Set[str]) -> Tuple[Set[str], Set[str]]:
        """
        Divise une partition en deux selon un splitter.
        
        :param partition: Partition à diviser
        :type partition: Set[str]
        :param splitter: Ensemble d'états pour la division
        :type splitter: Set[str]
        :return: Tuple des deux nouvelles partitions
        :rtype: Tuple[Set[str], Set[str]]
        """
        intersection = partition & splitter
        difference = partition - splitter
        
        return intersection, difference
    
    def remove_partition(self, partition_set: Set[str]) -> None:
        """
        Supprime une partition de l'arbre.
        
        :param partition_set: Partition à supprimer
        :type partition_set: Set[str]
        """
        key = self._create_partition_key(partition_set)
        if self.delete(key):
            self._partition_map.pop(key, None)
    
    def get_all_partitions(self) -> List[Set[str]]:
        """
        Récupère toutes les partitions.
        
        :return: Liste de toutes les partitions
        :rtype: List[Set[str]]
        """
        return list(self._partition_map.values())
    
    def clear(self) -> None:
        """Vide l'arbre de partitions."""
        self.root = None
        self.size = 0
        self._partition_map.clear()
    
    def _create_partition_key(self, partition_set: Set[str]) -> str:
        """Crée une clé unique pour une partition."""
        sorted_states = sorted(partition_set)
        return "|".join(sorted_states)


class AVLCache:
    """
    Cache intelligent basé sur des arbres AVL pour les optimisations.
    
    Ce cache utilise des techniques d'apprentissage pour prédire
    les accès futurs et optimiser la rétention des données.
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Initialise le cache AVL.
        
        :param max_size: Taille maximale du cache
        :type max_size: int
        """
        self.max_size = max_size
        self.access_tree = AVLTree()
        self.frequency_tree = AVLTree()
        self.cache_data: Dict[str, Any] = {}
        self.access_count = 0
        self.access_history: Dict[str, List[float]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """
        Récupère un automate du cache.
        
        :param key: Clé de l'automate
        :type key: str
        :return: Automate en cache ou None
        :rtype: Optional[Any]
        """
        if key not in self.cache_data:
            return None
        
        # Enregistrer l'accès
        current_time = time.time()
        self.access_count += 1
        
        if key not in self.access_history:
            self.access_history[key] = []
        self.access_history[key].append(current_time)
        
        # Mettre à jour les arbres de fréquence
        self._update_access_tree(key, current_time)
        self._update_frequency_tree(key)
        
        return self.cache_data[key]
    
    def put(self, key: str, value: Any) -> None:
        """
        Met un automate en cache.
        
        :param key: Clé de l'automate
        :type key: str
        :param value: Automate à mettre en cache
        :type value: Any
        """
        # Vérifier la taille du cache
        if len(self.cache_data) >= self.max_size:
            self._evict_least_used()
        
        # Ajouter au cache
        self.cache_data[key] = value
        
        # Initialiser l'historique d'accès
        if key not in self.access_history:
            self.access_history[key] = []
        
        # Mettre à jour les arbres
        current_time = time.time()
        self._update_access_tree(key, current_time)
        self._update_frequency_tree(key)
    
    def invalidate_pattern(self, pattern: str) -> None:
        """
        Invalide les entrées correspondant à un pattern.
        
        :param pattern: Pattern d'invalidation
        :type pattern: str
        """
        keys_to_remove = []
        for key in self.cache_data:
            if pattern in key:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            self._remove_key(key)
    
    def predict_next_access(self, key: str) -> float:
        """
        Prédit la probabilité d'accès futur d'une clé.
        
        :param key: Clé à analyser
        :type key: str
        :return: Probabilité d'accès (0.0 à 1.0)
        :rtype: float
        """
        if key not in self.access_history:
            return 0.0
        
        access_times = self.access_history[key]
        if len(access_times) < 2:
            return 0.5
        
        # Calculer la fréquence moyenne
        current_time = time.time()
        recent_accesses = [t for t in access_times if current_time - t < 3600]  # 1 heure
        
        if not recent_accesses:
            return 0.1
        
        # Calculer la probabilité basée sur la fréquence récente
        frequency = len(recent_accesses) / 3600  # accès par seconde
        return min(1.0, frequency * 0.1)  # Normaliser
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques du cache.
        
        :return: Statistiques du cache
        :rtype: Dict[str, Any]
        """
        return {
            "size": len(self.cache_data),
            "max_size": self.max_size,
            "access_count": self.access_count,
            "keys": list(self.cache_data.keys()),
            "hit_rate": self._calculate_hit_rate(),
        }
    
    def clear(self) -> None:
        """Vide le cache."""
        self.cache_data.clear()
        self.access_history.clear()
        self.access_tree.root = None
        self.frequency_tree.root = None
        self.access_count = 0
    
    def _update_access_tree(self, key: str, access_time: float) -> None:
        """Met à jour l'arbre d'accès."""
        self.access_tree.insert(key, access_time)
    
    def _update_frequency_tree(self, key: str) -> None:
        """Met à jour l'arbre de fréquence."""
        frequency = len(self.access_history.get(key, []))
        self.frequency_tree.insert(key, frequency)
    
    def _evict_least_used(self) -> None:
        """Évince l'entrée la moins utilisée."""
        if not self.cache_data:
            return
        
        # Trouver la clé avec la fréquence la plus faible
        min_frequency = float('inf')
        key_to_evict = None
        
        for key in self.cache_data:
            frequency = len(self.access_history.get(key, []))
            if frequency < min_frequency:
                min_frequency = frequency
                key_to_evict = key
        
        if key_to_evict:
            self._remove_key(key_to_evict)
    
    def _remove_key(self, key: str) -> None:
        """Supprime une clé du cache."""
        self.cache_data.pop(key, None)
        self.access_history.pop(key, None)
        self.access_tree.delete(key)
        self.frequency_tree.delete(key)
    
    def _calculate_hit_rate(self) -> float:
        """Calcule le taux de succès du cache."""
        if self.access_count == 0:
            return 0.0
        
        hits = sum(len(history) for history in self.access_history.values())
        return hits / self.access_count if self.access_count > 0 else 0.0


class AutomatonFeatureExtractor:
    """
    Extracteur de caractéristiques pour les automates.
    
    Cette classe extrait des caractéristiques des automates pour
    l'apprentissage automatique et la sélection d'algorithmes.
    """
    
    def extract(self, automaton) -> Dict[str, float]:
        """
        Extrait les caractéristiques d'un automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Dictionnaire des caractéristiques
        :rtype: Dict[str, float]
        """
        features = {}
        
        # Caractéristiques de base
        features['num_states'] = len(automaton.states)
        features['num_transitions'] = len(automaton._transitions)
        features['alphabet_size'] = len(automaton.alphabet)
        features['final_states_ratio'] = len(automaton.final_states) / len(automaton.states)
        
        # Densité des transitions
        features['transition_density'] = features['num_transitions'] / (
            features['num_states'] * features['alphabet_size']
        )
        
        # Caractéristiques de connectivité
        features['connectivity'] = self._calculate_connectivity(automaton)
        features['average_out_degree'] = self._calculate_average_out_degree(automaton)
        
        # Caractéristiques de régularité
        features['regularity_score'] = self._calculate_regularity_score(automaton)
        
        return features
    
    def _calculate_connectivity(self, automaton) -> float:
        """Calcule la connectivité de l'automate."""
        reachable_states = automaton.get_reachable_states()
        return len(reachable_states) / len(automaton.states)
    
    def _calculate_average_out_degree(self, automaton) -> float:
        """Calcule le degré de sortie moyen."""
        total_out_degree = 0
        for state in automaton.states:
            out_degree = 0
            for symbol in automaton.alphabet:
                if isinstance(automaton, DFA):
                    target = automaton.get_transition(state, symbol)
                    if target:
                        out_degree += 1
                else:  # NFA ou EpsilonNFA
                    targets = automaton.get_transition(state, symbol)
                    out_degree += len(targets) if targets else 0
            
            total_out_degree += out_degree
        
        return total_out_degree / len(automaton.states)
    
    def _calculate_regularity_score(self, automaton) -> float:
        """Calcule un score de régularité."""
        # Pour l'instant, retourner un score basé sur la densité des transitions
        num_states = len(automaton.states)
        num_transitions = len(automaton._transitions)
        alphabet_size = len(automaton.alphabet)
        
        max_possible_transitions = num_states * alphabet_size
        if max_possible_transitions == 0:
            return 0.0
        
        density = num_transitions / max_possible_transitions
        return 1.0 - abs(density - 0.5) * 2  # Score entre 0 et 1


class PerformanceModel:
    """
    Modèle de prédiction de performance.
    
    Cette classe utilise des techniques simples de prédiction
    pour estimer les performances des algorithmes d'optimisation.
    """
    
    def __init__(self):
        """Initialise le modèle de performance."""
        self.training_data: List[Tuple[Dict[str, float], Dict[str, float]]] = []
        self.feature_weights: Dict[str, float] = {}
    
    def predict(self, features: Dict[str, float]) -> Dict[str, float]:
        """
        Prédit les performances basées sur les caractéristiques.
        
        :param features: Caractéristiques de l'automate
        :type features: Dict[str, float]
        :return: Prédictions de performance
        :rtype: Dict[str, float]
        """
        # Modèle simple basé sur des heuristiques
        num_states = features.get('num_states', 1)
        num_transitions = features.get('num_transitions', 1)
        alphabet_size = features.get('alphabet_size', 1)
        
        # Prédictions basées sur la complexité théorique
        time_prediction = num_states * num_transitions * 0.001  # ms
        memory_prediction = num_states * alphabet_size * 0.01  # MB
        improvement_prediction = min(0.5, num_states * 0.001)  # %
        
        return {
            'time': time_prediction,
            'memory': memory_prediction,
            'improvement': improvement_prediction,
        }
    
    def update(self, features: Dict[str, float], 
               actual_performance: Dict[str, float]) -> None:
        """
        Met à jour le modèle avec les performances réelles.
        
        :param features: Caractéristiques de l'automate
        :type features: Dict[str, float]
        :param actual_performance: Performances réelles
        :type actual_performance: Dict[str, float]
        """
        self.training_data.append((features, actual_performance))
        
        # Limiter la taille des données d'entraînement
        if len(self.training_data) > 1000:
            self.training_data = self.training_data[-1000:]
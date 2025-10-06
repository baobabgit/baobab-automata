"""
Statistiques des opérations sur les langages.

Ce module implémente la classe OperationStats pour le suivi
des performances des opérations sur les langages réguliers.
"""

import time
from typing import Any, Dict, List, Optional


class OperationStats:
    """
    Classe pour le suivi des statistiques des opérations sur les langages.

    Cette classe permet de collecter et d'analyser les métriques de performance
    des opérations sur les langages réguliers, incluant le temps d'exécution,
    le nombre d'états et de transitions résultants.
    """

    def __init__(self) -> None:
        """
        Initialise les statistiques des opérations.

        Crée un nouveau conteneur de statistiques vide.
        """
        self._operations: List[Dict[str, Any]] = []
        self._start_time: Optional[float] = None

    def add_operation(
        self,
        operation: str,
        time_taken: float,
        states: int,
        transitions: int,
        memory_used: int = 0,
    ) -> None:
        """
        Ajoute une opération aux statistiques.

        :param operation: Nom de l'opération effectuée
        :type operation: str
        :param time_taken: Temps d'exécution en secondes
        :type time_taken: float
        :param states: Nombre d'états dans le résultat
        :type states: int
        :param transitions: Nombre de transitions dans le résultat
        :type transitions: int
        :param memory_used: Mémoire utilisée en octets (optionnel)
        :type memory_used: int
        """
        self._operations.append(
            {
                "operation": operation,
                "time": time_taken,
                "states": states,
                "transitions": transitions,
                "memory": memory_used,
                "timestamp": time.time(),
            }
        )

    def start_timing(self) -> None:
        """
        Démarre le chronométrage d'une opération.

        Cette méthode doit être appelée avant le début d'une opération
        pour permettre le calcul automatique du temps d'exécution.
        """
        self._start_time = time.time()

    def stop_timing(
        self,
        operation: str,
        states: int,
        transitions: int,
        memory_used: int = 0,
    ) -> None:
        """
        Arrête le chronométrage et ajoute l'opération aux statistiques.

        :param operation: Nom de l'opération effectuée
        :type operation: str
        :param states: Nombre d'états dans le résultat
        :type states: int
        :param transitions: Nombre de transitions dans le résultat
        :type transitions: int
        :param memory_used: Mémoire utilisée en octets (optionnel)
        :type memory_used: int
        :raises ValueError: Si start_timing n'a pas été appelé
        """
        if self._start_time is None:
            raise ValueError("start_timing() must be called before stop_timing()")

        time_taken = time.time() - self._start_time
        self.add_operation(operation, time_taken, states, transitions, memory_used)
        self._start_time = None

    def get_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques globales.

        :return: Dictionnaire contenant les statistiques globales
        :rtype: Dict[str, Any]
        """
        if not self._operations:
            return {
                "total_operations": 0,
                "average_time": 0.0,
                "total_time": 0.0,
                "average_states": 0.0,
                "average_transitions": 0.0,
                "operations_by_type": {},
            }

        total_time = sum(op["time"] for op in self._operations)
        total_states = sum(op["states"] for op in self._operations)
        total_transitions = sum(op["transitions"] for op in self._operations)

        # Statistiques par type d'opération
        operations_by_type: Dict[str, Dict[str, Any]] = {}
        for op in self._operations:
            op_type = op["operation"]
            if op_type not in operations_by_type:
                operations_by_type[op_type] = {
                    "count": 0,
                    "total_time": 0.0,
                    "average_time": 0.0,
                    "total_states": 0,
                    "average_states": 0.0,
                    "total_transitions": 0,
                    "average_transitions": 0.0,
                }

            operations_by_type[op_type]["count"] += 1
            operations_by_type[op_type]["total_time"] += op["time"]
            operations_by_type[op_type]["total_states"] += op["states"]
            operations_by_type[op_type]["total_transitions"] += op["transitions"]

        # Calcul des moyennes par type
        for op_type in operations_by_type:
            count = operations_by_type[op_type]["count"]
            operations_by_type[op_type]["average_time"] = (
                operations_by_type[op_type]["total_time"] / count
            )
            operations_by_type[op_type]["average_states"] = (
                operations_by_type[op_type]["total_states"] / count
            )
            operations_by_type[op_type]["average_transitions"] = (
                operations_by_type[op_type]["total_transitions"] / count
            )

        return {
            "total_operations": len(self._operations),
            "average_time": total_time / len(self._operations),
            "total_time": total_time,
            "average_states": total_states / len(self._operations),
            "average_transitions": total_transitions / len(self._operations),
            "operations_by_type": operations_by_type,
        }

    def get_operation_history(self) -> List[Dict[str, Any]]:
        """
        Récupère l'historique complet des opérations.

        :return: Liste de tous les enregistrements d'opérations
        :rtype: List[Dict[str, Any]]
        """
        return self._operations.copy()

    def get_operations_by_type(self, operation_type: str) -> List[Dict[str, Any]]:
        """
        Récupère toutes les opérations d'un type donné.

        :param operation_type: Type d'opération à filtrer
        :type operation_type: str
        :return: Liste des opérations du type spécifié
        :rtype: List[Dict[str, Any]]
        """
        return [op for op in self._operations if op["operation"] == operation_type]

    def reset(self) -> None:
        """
        Remet à zéro toutes les statistiques.

        Efface l'historique des opérations et remet à zéro
        tous les compteurs et métriques.
        """
        self._operations.clear()
        self._start_time = None

    def export_to_dict(self) -> Dict[str, Any]:
        """
        Exporte les statistiques vers un dictionnaire.

        :return: Dictionnaire contenant toutes les statistiques
        :rtype: Dict[str, Any]
        """
        return {
            "stats": self.get_stats(),
            "history": self.get_operation_history(),
        }

    def import_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Importe les statistiques depuis un dictionnaire.

        :param data: Dictionnaire contenant les statistiques à importer
        :type data: Dict[str, Any]
        :raises ValueError: Si le format des données est invalide
        """
        if "history" not in data:
            raise ValueError("Invalid data format: missing 'history' key")

        self.reset()
        for op in data["history"]:
            required_keys = ["operation", "time", "states", "transitions"]
            if not all(key in op for key in required_keys):
                raise ValueError(f"Invalid operation data: missing required keys")

            self.add_operation(
                op["operation"],
                op["time"],
                op["states"],
                op["transitions"],
                op.get("memory", 0),
            )

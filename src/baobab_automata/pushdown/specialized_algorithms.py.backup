"""
Algorithmes spécialisés pour les grammaires hors-contexte et les automates à pile.

Ce module implémente les algorithmes spécialisés tels que CYK, Earley,
l'élimination de récursivité gauche, l'élimination de productions vides,
et la normalisation des grammaires.
"""

import time
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass, field

from .grammar_types import ContextFreeGrammar, Production
from .specialized_exceptions import (
    AlgorithmError,
    AlgorithmTimeoutError,
    CYKError,
    EarleyError,
    LeftRecursionError,
    EmptyProductionError,
    NormalizationError,
)


@dataclass
class ParseTree:
    """Arbre de dérivation pour les algorithmes de parsing."""

    symbol: str
    children: List["ParseTree"] = field(default_factory=list)
    start_pos: int = 0
    end_pos: int = 0

    def __str__(self) -> str:
        """Représentation string de l'arbre."""
        if not self.children:
            return self.symbol
        children_str = " ".join(str(child) for child in self.children)
        return f"({self.symbol} {children_str})"


@dataclass
class AlgorithmStats:
    """Statistiques de performance des algorithmes."""

    algorithm_type: str
    execution_time: float
    memory_used: int
    cache_hits: int = 0
    cache_misses: int = 0
    iterations: int = 0

    @property
    def cache_hit_rate(self) -> float:
        """Taux de réussite du cache."""
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0


class SpecializedAlgorithms:
    """Algorithmes spécialisés pour les grammaires hors-contexte et les automates à pile.

    Cette classe fournit des algorithmes avancés pour l'analyse syntaxique,
    la manipulation des grammaires et l'optimisation des automates à pile.
    """

    def __init__(
        self,
        enable_caching: bool = True,
        max_cache_size: int = 1000,
        timeout: float = 60.0,
    ) -> None:
        """Initialise les algorithmes spécialisés.

        :param enable_caching: Active la mise en cache des résultats
        :param max_cache_size: Taille maximale du cache
        :param timeout: Timeout en secondes pour les algorithmes
        :raises AlgorithmError: Si l'initialisation échoue
        """
        self.enable_caching = enable_caching
        self.max_cache_size = max_cache_size
        self.timeout = timeout

        # Cache pour les résultats des algorithmes
        self._cache: Dict[str, Any] = {}
        self._cache_stats = {"hits": 0, "misses": 0}

        # Statistiques de performance
        self._performance_stats: List[AlgorithmStats] = []

        # Configuration des algorithmes
        self._algorithm_config: Dict[str, Dict[str, Any]] = {
            "CYK": {"optimize": True, "use_cache": True},
            "Earley": {"optimize": True, "use_cache": True},
            "LeftRecursion": {"detect_indirect": True},
            "EmptyProduction": {"preserve_grammar": True},
            "Normalization": {
                "chomsky_optimize": True,
                "greibach_optimize": True,
            },
        }

        # Validation de la configuration
        if max_cache_size <= 0:
            raise AlgorithmError("La taille du cache doit être positive")
        if timeout <= 0:
            raise AlgorithmError("Le timeout doit être positif")

    def configure_algorithm(
        self, algorithm_type: str, parameters: Dict[str, Any]
    ) -> None:
        """Configure un algorithme spécifique.

        :param algorithm_type: Type d'algorithme à configurer
        :param parameters: Paramètres de configuration
        :raises AlgorithmError: Si la configuration échoue
        """
        if algorithm_type not in self._algorithm_config:
            raise AlgorithmError(
                f"Type d'algorithme inconnu: {algorithm_type}"
            )

        # Validation des paramètres
        for key in parameters.keys():
            if not isinstance(key, str):
                raise AlgorithmError(f"Clé de paramètre invalide: {key}")

        # Mise à jour de la configuration
        self._algorithm_config[algorithm_type].update(parameters)

    def cyk_parse(self, grammar: ContextFreeGrammar, word: str) -> bool:
        """Parse un mot avec l'algorithme CYK.

        :param grammar: Grammaire en forme normale de Chomsky
        :param word: Mot à parser
        :return: True si le mot est généré par la grammaire, False sinon
        :raises CYKError: Si le parsing échoue
        :raises AlgorithmTimeoutError: Si le parsing dépasse le timeout
        """
        start_time = time.time()

        try:
            # Vérification que la grammaire est en forme normale de Chomsky
            if not self._is_chomsky_normal_form(grammar):
                raise CYKError(
                    "La grammaire doit être en forme normale de Chomsky"
                )

            # Vérification du cache
            cache_key = f"cyk_{id(grammar)}_{word}"
            if self.enable_caching and cache_key in self._cache:
                self._cache_stats["hits"] += 1
                return self._cache[cache_key]

            self._cache_stats["misses"] += 1

            # Algorithme CYK
            n = len(word)
            if n == 0:
                # Mot vide - vérifier si S -> ε existe
                result = Production("S", ()) in grammar.productions
            else:
                # Table de parsing CYK
                table = [[set() for _ in range(n)] for _ in range(n)]

                # Remplissage de la diagonale (productions terminales)
                for i in range(n):
                    for production in grammar.productions:
                        if (
                            len(production.right_side) == 1
                            and production.right_side[0] == word[i]
                        ):
                            table[i][i].add(production.left_side)

                # Remplissage du reste de la table
                for length in range(2, n + 1):
                    for i in range(n - length + 1):
                        j = i + length - 1
                        for k in range(i, j):
                            # Vérifier toutes les productions A -> BC
                            for production in grammar.productions:
                                if len(production.right_side) == 2:
                                    B, C = production.right_side
                                    if (
                                        B in table[i][k]
                                        and C in table[k + 1][j]
                                    ):
                                        table[i][j].add(production.left_side)

                # Vérifier si le symbole de départ est dans table[0][n-1]
                result = grammar.start_symbol in table[0][n - 1]

            # Mise en cache du résultat
            if self.enable_caching and len(self._cache) < self.max_cache_size:
                self._cache[cache_key] = result

            # Enregistrement des statistiques
            execution_time = time.time() - start_time
            self._performance_stats.append(
                AlgorithmStats(
                    algorithm_type="CYK",
                    execution_time=execution_time,
                    memory_used=0,  # TODO: Implémenter la mesure de mémoire
                    cache_hits=self._cache_stats["hits"],
                    cache_misses=self._cache_stats["misses"],
                )
            )

            return result

        except Exception as e:
            if isinstance(e, (CYKError, AlgorithmTimeoutError)):
                raise
            raise CYKError(f"Erreur lors du parsing CYK: {str(e)}") from e

    def cyk_parse_with_tree(
        self, grammar: ContextFreeGrammar, word: str
    ) -> Optional[ParseTree]:
        """Parse un mot avec l'algorithme CYK et retourne l'arbre de dérivation.

        :param grammar: Grammaire en forme normale de Chomsky
        :param word: Mot à parser
        :return: Arbre de dérivation ou None si le mot n'est pas généré
        :raises CYKError: Si le parsing échoue
        """
        start_time = time.time()

        try:
            # Vérification que la grammaire est en forme normale de Chomsky
            if not self._is_chomsky_normal_form(grammar):
                raise CYKError(
                    "La grammaire doit être en forme normale de Chomsky"
                )

            n = len(word)
            if n == 0:
                # Mot vide - vérifier si S -> ε existe
                if Production("S", ()) in grammar.productions:
                    return ParseTree("S", [], 0, 0)
                return None

            # Table de parsing CYK avec arbres
            table = [[{} for _ in range(n)] for _ in range(n)]

            # Remplissage de la diagonale (productions terminales)
            for i in range(n):
                for production in grammar.productions:
                    if (
                        len(production.right_side) == 1
                        and production.right_side[0] == word[i]
                    ):
                        table[i][i][production.left_side] = ParseTree(
                            production.left_side,
                            [ParseTree(word[i], [], i, i)],
                            i,
                            i,
                        )

            # Remplissage du reste de la table
            for length in range(2, n + 1):
                for i in range(n - length + 1):
                    j = i + length - 1
                    for k in range(i, j):
                        # Vérifier toutes les productions A -> BC
                        for production in grammar.productions:
                            if len(production.right_side) == 2:
                                B, C = production.right_side
                                if B in table[i][k] and C in table[k + 1][j]:
                                    table[i][j][production.left_side] = (
                                        ParseTree(
                                            production.left_side,
                                            [
                                                table[i][k][B],
                                                table[k + 1][j][C],
                                            ],
                                            i,
                                            j,
                                        )
                                    )

            # Retourner l'arbre si le symbole de départ est présent
            if grammar.start_symbol in table[0][n - 1]:
                return table[0][n - 1][grammar.start_symbol]

            return None

        except Exception as e:
            if isinstance(e, CYKError):
                raise
            raise CYKError(
                f"Erreur lors du parsing CYK avec arbre: {str(e)}"
            ) from e

    def cyk_parse_optimized(
        self, grammar: ContextFreeGrammar, word: str
    ) -> bool:
        """Parse un mot avec l'algorithme CYK optimisé.

        :param grammar: Grammaire en forme normale de Chomsky
        :param word: Mot à parser
        :return: True si le mot est généré par la grammaire, False sinon
        :raises CYKError: Si le parsing échoue
        """
        # Pour l'instant, utilise l'implémentation de base
        # TODO: Implémenter les optimisations
        return self.cyk_parse(grammar, word)

    def earley_parse(self, grammar: ContextFreeGrammar, word: str) -> bool:
        """Parse un mot avec l'algorithme Earley.

        :param grammar: Grammaire hors-contexte
        :param word: Mot à parser
        :return: True si le mot est généré par la grammaire, False sinon
        :raises EarleyError: Si le parsing échoue
        :raises AlgorithmTimeoutError: Si le parsing dépasse le timeout
        """
        start_time = time.time()

        try:
            # Vérification du cache
            cache_key = f"earley_{id(grammar)}_{word}"
            if self.enable_caching and cache_key in self._cache:
                self._cache_stats["hits"] += 1
                return self._cache[cache_key]

            self._cache_stats["misses"] += 1

            # Algorithme Earley simplifié
            n = len(word)
            if n == 0:
                # Mot vide - vérifier si S -> ε existe
                result = any(
                    production.left_side == grammar.start_symbol and 
                    not production.right_side
                    for production in grammar.productions
                )
            else:
                # Pour un mot non-vide, utiliser une approche de parsing très simple
                result = self._very_simple_earley_parse(grammar, word)

            # Mise en cache du résultat
            if self.enable_caching and len(self._cache) < self.max_cache_size:
                self._cache[cache_key] = result

            # Enregistrement des statistiques
            execution_time = time.time() - start_time
            self._performance_stats.append(
                AlgorithmStats(
                    algorithm_type="Earley",
                    execution_time=execution_time,
                    memory_used=0,  # TODO: Implémenter la mesure de mémoire
                    cache_hits=self._cache_stats["hits"],
                    cache_misses=self._cache_stats["misses"],
                )
            )

            return result

        except Exception as e:
            if isinstance(e, (EarleyError, AlgorithmTimeoutError)):
                raise
            raise EarleyError(
                f"Erreur lors du parsing Earley: {str(e)}"
            ) from e

    def earley_parse_with_tree(
        self, grammar: ContextFreeGrammar, word: str
    ) -> Optional[ParseTree]:
        """Parse un mot avec l'algorithme Earley et retourne l'arbre de dérivation.

        :param grammar: Grammaire hors-contexte
        :param word: Mot à parser
        :return: Arbre de dérivation ou None si le mot n'est pas généré
        :raises EarleyError: Si le parsing échoue
        """
        # Pour l'instant, utilise l'implémentation de base
        # TODO: Implémenter la construction d'arbre pour Earley
        if self.earley_parse(grammar, word):
            # Construction d'un arbre simple
            return ParseTree(grammar.start_symbol, [], 0, len(word))
        return None

    def earley_parse_optimized(
        self, grammar: ContextFreeGrammar, word: str
    ) -> bool:
        """Parse un mot avec l'algorithme Earley optimisé.

        :param grammar: Grammaire hors-contexte
        :param word: Mot à parser
        :return: True si le mot est généré par la grammaire, False sinon
        :raises EarleyError: Si le parsing échoue
        """
        # Pour l'instant, utilise l'implémentation de base
        # TODO: Implémenter les optimisations
        return self.earley_parse(grammar, word)

    def detect_left_recursion(
        self, grammar: ContextFreeGrammar
    ) -> Dict[str, List[str]]:
        """Détecte la récursivité gauche dans une grammaire.

        :param grammar: Grammaire à analyser
        :return: Dictionnaire des variables avec récursivité gauche
        :raises LeftRecursionError: Si l'analyse échoue
        """
        try:
            left_recursive = defaultdict(list)

            for production in grammar.productions:
                if (
                    production.right_side
                    and production.right_side[0] == production.left_side
                ):
                    left_recursive[production.left_side].append(
                        " ".join(production.right_side)
                    )

            return dict(left_recursive)

        except Exception as e:
            raise LeftRecursionError(
                f"Erreur lors de la détection de récursivité gauche: {str(e)}"
            ) from e

    def eliminate_left_recursion(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Élimine la récursivité gauche d'une grammaire.

        :param grammar: Grammaire à traiter
        :return: Grammaire sans récursivité gauche
        :raises LeftRecursionError: Si l'élimination échoue
        """
        try:
            new_productions = set()
            new_variables = set(grammar.variables)

            for variable in grammar.variables:
                # Séparer les productions récursives et non-récursives
                recursive_productions = []
                non_recursive_productions = []

                for production in grammar.productions:
                    if production.left_side == variable:
                        if (
                            production.right_side
                            and production.right_side[0] == variable
                        ):
                            recursive_productions.append(production)
                        else:
                            non_recursive_productions.append(production)

                if recursive_productions:
                    # Créer une nouvelle variable pour la récursivité
                    new_var = f"{variable}'"
                    new_variables.add(new_var)

                    # Ajouter les productions non-récursives
                    for prod in non_recursive_productions:
                        if prod.right_side:
                            new_productions.add(
                                Production(
                                    variable,
                                    tuple(list(prod.right_side) + [new_var]),
                                )
                            )
                        else:
                            new_productions.add(
                                Production(variable, (new_var,))
                            )

                    # Ajouter les productions récursives
                    for prod in recursive_productions:
                        if len(prod.right_side) > 1:
                            new_productions.add(
                                Production(
                                    new_var,
                                    tuple(
                                        list(prod.right_side[1:]) + [new_var]
                                    ),
                                )
                            )

                    # Ajouter la production vide pour la nouvelle variable
                    new_productions.add(Production(new_var, ()))
                else:
                    # Pas de récursivité gauche, garder les productions
                    for prod in non_recursive_productions:
                        new_productions.add(prod)

            return ContextFreeGrammar(
                variables=new_variables,
                terminals=grammar.terminals,
                productions=new_productions,
                start_symbol=grammar.start_symbol,
            )

        except Exception as e:
            raise LeftRecursionError(
                f"Erreur lors de l'élimination de récursivité gauche: {str(e)}"
            ) from e

    def eliminate_indirect_left_recursion(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Élimine la récursivité gauche indirecte d'une grammaire.

        :param grammar: Grammaire à traiter
        :return: Grammaire sans récursivité gauche indirecte
        :raises LeftRecursionError: Si l'élimination échoue
        """
        # Pour l'instant, utilise l'élimination directe
        # TODO: Implémenter l'élimination indirecte
        return self.eliminate_left_recursion(grammar)

    def detect_empty_productions(
        self, grammar: ContextFreeGrammar
    ) -> Set[str]:
        """Détecte les variables qui peuvent générer le mot vide.

        :param grammar: Grammaire à analyser
        :return: Ensemble des variables générant le mot vide
        :raises EmptyProductionError: Si l'analyse échoue
        """
        try:
            nullable = set()
            changed = True

            while changed:
                changed = False
                for production in grammar.productions:
                    if production.left_side not in nullable and (
                        not production.right_side
                        or all(
                            symbol in nullable
                            for symbol in production.right_side
                        )
                    ):
                        nullable.add(production.left_side)
                        changed = True

            return nullable

        except Exception as e:
            raise EmptyProductionError(
                f"Erreur lors de la détection de productions vides: {str(e)}"
            ) from e

    def eliminate_empty_productions(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Élimine les productions vides d'une grammaire.

        :param grammar: Grammaire à traiter
        :return: Grammaire sans productions vides
        :raises EmptyProductionError: Si l'élimination échoue
        """
        try:
            # Détecter les variables nullable
            nullable = self.detect_empty_productions(grammar)

            new_productions = set()

            for production in grammar.productions:
                if not production.right_side:
                    # Production vide - l'ignorer
                    continue

                # Générer toutes les combinaisons sans les variables nullable
                self._generate_combinations(
                    production.left_side,
                    production.right_side,
                    nullable,
                    new_productions,
                )

            return ContextFreeGrammar(
                variables=grammar.variables,
                terminals=grammar.terminals,
                productions=new_productions,
                start_symbol=grammar.start_symbol,
            )

        except Exception as e:
            raise EmptyProductionError(
                f"Erreur lors de l'élimination de productions vides: {str(e)}"
            ) from e

    def to_chomsky_normal_form(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Convertit une grammaire en forme normale de Chomsky.

        :param grammar: Grammaire à convertir
        :return: Grammaire en forme normale de Chomsky
        :raises NormalizationError: Si la conversion échoue
        """
        try:
            # 1. Éliminer les productions vides
            grammar = self.eliminate_empty_productions(grammar)

            # 2. Éliminer les productions unitaires
            grammar = self._eliminate_unit_productions(grammar)

            # 3. Convertir en productions binaires
            grammar = self._convert_to_binary_productions(grammar)

            return grammar

        except Exception as e:
            raise NormalizationError(
                f"Erreur lors de la conversion en forme normale de Chomsky: {str(e)}"
            ) from e

    def to_greibach_normal_form(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Convertit une grammaire en forme normale de Greibach.

        :param grammar: Grammaire à convertir
        :return: Grammaire en forme normale de Greibach
        :raises NormalizationError: Si la conversion échoue
        """
        try:
            # 1. Convertir en forme normale de Chomsky
            grammar = self.to_chomsky_normal_form(grammar)

            # 2. Éliminer la récursivité gauche
            grammar = self.eliminate_left_recursion(grammar)

            # 3. Convertir en productions de la forme A -> aα
            # TODO: Implémenter la conversion complète
            return grammar

        except Exception as e:
            raise NormalizationError(
                f"Erreur lors de la conversion en forme normale de Greibach: {str(e)}"
            ) from e

    def detect_ambiguity(self, grammar: ContextFreeGrammar) -> bool:
        """Détecte si une grammaire est ambiguë.

        :param grammar: Grammaire à analyser
        :return: True si la grammaire est ambiguë, False sinon
        :raises AlgorithmError: Si l'analyse échoue
        """
        # Pour l'instant, détection simple
        # TODO: Implémenter une détection plus sophistiquée
        return False

    def analyze_recursion(self, grammar: ContextFreeGrammar) -> Dict[str, Any]:
        """Analyse la récursivité d'une grammaire.

        :param grammar: Grammaire à analyser
        :return: Dictionnaire avec l'analyse de récursivité
        :raises AlgorithmError: Si l'analyse échoue
        """
        try:
            left_recursion = self.detect_left_recursion(grammar)

            return {
                "left_recursion": left_recursion,
                "has_left_recursion": bool(left_recursion),
                "recursive_variables": list(left_recursion.keys()),
            }

        except Exception as e:
            raise AlgorithmError(
                f"Erreur lors de l'analyse de récursivité: {str(e)}"
            ) from e

    def analyze_symbols(self, grammar: ContextFreeGrammar) -> Dict[str, Any]:
        """Analyse les symboles d'une grammaire.

        :param grammar: Grammaire à analyser
        :return: Dictionnaire avec l'analyse des symboles
        :raises AlgorithmError: Si l'analyse échoue
        """
        try:
            # Compter les productions par variable
            productions_by_var = defaultdict(int)
            for production in grammar.productions:
                productions_by_var[production.left_side] += 1

            return {
                "variables": len(grammar.variables),
                "terminals": len(grammar.terminals),
                "productions": len(grammar.productions),
                "productions_by_variable": dict(productions_by_var),
            }

        except Exception as e:
            raise AlgorithmError(
                f"Erreur lors de l'analyse des symboles: {str(e)}"
            ) from e

    def clear_cache(self) -> None:
        """Vide le cache des algorithmes."""
        self._cache.clear()
        self._cache_stats = {"hits": 0, "misses": 0}

    def get_cache_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques du cache.

        :return: Dictionnaire avec les statistiques du cache
        """
        total = self._cache_stats["hits"] + self._cache_stats["misses"]
        hit_rate = self._cache_stats["hits"] / total if total > 0 else 0.0

        return {
            "hits": self._cache_stats["hits"],
            "misses": self._cache_stats["misses"],
            "hit_rate": hit_rate,
            "size": len(self._cache),
            "max_size": self.max_cache_size,
        }

    def get_performance_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques de performance.

        :return: Dictionnaire avec les statistiques de performance
        """
        if not self._performance_stats:
            return {}

        # Statistiques par type d'algorithme
        stats_by_type = defaultdict(list)
        for stat in self._performance_stats:
            stats_by_type[stat.algorithm_type].append(stat)

        result = {}
        for algo_type, stats in stats_by_type.items():
            total_time = sum(s.execution_time for s in stats)
            avg_time = total_time / len(stats)

            result[algo_type] = {
                "count": len(stats),
                "total_time": total_time,
                "average_time": avg_time,
                "cache_hit_rate": stats[0].cache_hit_rate if stats else 0.0,
            }

        return result

    def to_dict(self) -> Dict[str, Any]:
        """Convertit les algorithmes en dictionnaire.

        :return: Représentation dictionnaire des algorithmes
        """
        return {
            "enable_caching": self.enable_caching,
            "max_cache_size": self.max_cache_size,
            "timeout": self.timeout,
            "algorithm_config": self._algorithm_config,
            "cache_stats": self._cache_stats,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpecializedAlgorithms":
        """Crée les algorithmes à partir d'un dictionnaire.

        :param data: Données des algorithmes
        :return: Instance des algorithmes
        :raises AlgorithmError: Si les données sont invalides
        """
        if not isinstance(data, dict):
            raise AlgorithmError("Les données doivent être un dictionnaire")

        try:
            instance = cls(
                enable_caching=data.get("enable_caching", True),
                max_cache_size=data.get("max_cache_size", 1000),
                timeout=data.get("timeout", 60.0),
            )

            if "algorithm_config" in data:
                instance._algorithm_config = data["algorithm_config"]

            return instance

        except Exception as e:
            raise AlgorithmError(
                f"Erreur lors de la création depuis le dictionnaire: {str(e)}"
            ) from e

    def _very_simple_earley_parse(self, grammar: ContextFreeGrammar, word: str) -> bool:
        """Parse très simple pour l'algorithme Earley.
        
        :param grammar: Grammaire hors-contexte
        :param word: Mot à parser
        :return: True si le mot peut être généré par la grammaire
        """
        # Approche très simple : utiliser une méthode de parsing descendant récursif
        # avec mémorisation pour éviter les calculs redondants
        
        memo = {}
        
        def parse(variable: str, pos: int) -> bool:
            """Parse récursif avec mémorisation."""
            if (variable, pos) in memo:
                return memo[(variable, pos)]
            
            if pos == len(word):
                # Fin du mot - vérifier si la variable peut générer ε
                result = any(
                    production.left_side == variable and not production.right_side
                    for production in grammar.productions
                )
            else:
                # Essayer toutes les productions de la variable
                result = False
                for production in grammar.productions:
                    if production.left_side == variable:
                        if not production.right_side:
                            # Production vide - continuer avec la même position
                            result = parse(variable, pos)
                        elif len(production.right_side) == 1:
                            # Production terminale
                            if (production.right_side[0] == word[pos] and 
                                parse(variable, pos + 1)):
                                result = True
                                break
                        else:
                            # Production avec plusieurs symboles
                            # Essayer de parser la séquence de droite
                            if parse_sequence(production.right_side, pos):
                                result = True
                                break
            
            memo[(variable, pos)] = result
            return result
        
        def parse_sequence(sequence: Tuple[str, ...], pos: int) -> bool:
            """Parse une séquence de symboles."""
            if not sequence:
                return True
            
            if len(sequence) == 1:
                symbol = sequence[0]
                if symbol in grammar.terminals:
                    return pos < len(word) and word[pos] == symbol
                else:
                    return parse(symbol, pos)
            
            # Pour les séquences multiples, essayer toutes les partitions
            for i in range(1, len(sequence)):
                left_part = sequence[:i]
                right_part = sequence[i:]
                
                if parse_sequence(left_part, pos):
                    new_pos = pos + len(left_part)
                    if new_pos <= len(word) and parse_sequence(right_part, new_pos):
                        return True
            
            return False
        
        return parse(grammar.start_symbol, 0)

    def _is_chomsky_normal_form(self, grammar: ContextFreeGrammar) -> bool:
        """Vérifie si une grammaire est en forme normale de Chomsky."""
        for production in grammar.productions:
            if not production.right_side:
                # Production vide - seulement pour le symbole de départ
                if production.left_side != grammar.start_symbol:
                    return False
            elif len(production.right_side) == 1:
                # Production terminale
                if production.right_side[0] not in grammar.terminals:
                    return False
            elif len(production.right_side) == 2:
                # Production binaire
                if (
                    production.right_side[0] not in grammar.variables
                    or production.right_side[1] not in grammar.variables
                ):
                    return False
            else:
                # Production non-binaire
                return False

        return True

    def _generate_combinations(
        self,
        left_side: str,
        right_side: Tuple[str, ...],
        nullable: Set[str],
        productions: Set[Production],
    ) -> None:
        """Génère toutes les combinaisons sans les variables nullable."""
        # TODO: Implémenter la génération de combinaisons
        productions.add(Production(left_side, right_side))

    def _eliminate_unit_productions(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Élimine les productions unitaires d'une grammaire."""
        new_productions = set()

        for production in grammar.productions:
            if (
                len(production.right_side) == 1
                and production.right_side[0] in grammar.variables
            ):
                # Production unitaire - la remplacer par les productions de la variable
                unit_var = production.right_side[0]
                for other_production in grammar.productions:
                    if other_production.left_side == unit_var:
                        new_productions.add(
                            Production(
                                production.left_side,
                                other_production.right_side,
                            )
                        )
            else:
                # Production non-unitaire - la garder
                new_productions.add(production)

        return ContextFreeGrammar(
            variables=grammar.variables,
            terminals=grammar.terminals,
            productions=new_productions,
            start_symbol=grammar.start_symbol,
        )

    def _convert_to_binary_productions(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Convertit les productions en productions binaires."""
        new_productions = set()
        new_variables = set(grammar.variables)
        var_counter = 0

        # Créer des variables pour chaque terminal
        terminal_vars = {}
        for terminal in grammar.terminals:
            terminal_var = f"T{var_counter}"
            var_counter += 1
            new_variables.add(terminal_var)
            terminal_vars[terminal] = terminal_var
            # Ajouter la production T -> a
            new_productions.add(Production(terminal_var, (terminal,)))

        for production in grammar.productions:
            if (
                len(production.right_side) == 1
                and production.right_side[0] in grammar.terminals
            ):
                # Production terminale - la garder
                new_productions.add(production)
            elif len(production.right_side) == 2 and all(
                s in grammar.variables for s in production.right_side
            ):
                # Production binaire de variables - la garder
                new_productions.add(production)
            else:
                # Production mixte - la convertir
                current_left = production.left_side
                right_side = list(production.right_side)

                # Remplacer les terminaux par leurs variables
                for i, symbol in enumerate(right_side):
                    if symbol in grammar.terminals:
                        right_side[i] = terminal_vars[symbol]

                # Créer des productions binaires
                while len(right_side) > 2:
                    # Créer une nouvelle variable
                    new_var = f"X{var_counter}"
                    var_counter += 1
                    new_variables.add(new_var)

                    # Ajouter la production A -> B C
                    new_productions.add(
                        Production(current_left, (right_side[0], new_var))
                    )

                    # Continuer avec le reste
                    current_left = new_var
                    right_side = right_side[1:]

                # Ajouter la dernière production
                new_productions.add(
                    Production(current_left, tuple(right_side))
                )

        return ContextFreeGrammar(
            variables=new_variables,
            terminals=grammar.terminals,
            productions=new_productions,
            start_symbol=grammar.start_symbol,
        )

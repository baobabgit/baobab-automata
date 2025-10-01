"""
Parser de grammaires hors-contexte avec conversions vers/depuis les automates à pile.

Ce module implémente un parser complet de grammaires hors-contexte (CFG) permettant
la conversion bidirectionnelle entre grammaires et automates à pile (PDA, DPDA, NPDA).
Il inclut également des fonctionnalités de normalisation, d'optimisation et d'analyse
des grammaires.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional, Set, Tuple

from .grammar_exceptions import (
    GrammarConversionError,
    GrammarError,
    GrammarNormalizationError,
    GrammarOptimizationError,
    GrammarParseError,
    GrammarValidationError,
)
from .grammar_types import ContextFreeGrammar, GrammarType, Production


class GrammarParser:
    """Parser de grammaires hors-contexte avec conversions vers/depuis les automates à pile.

    Cette classe fournit un ensemble complet d'outils pour :
    - Parser et valider des grammaires hors-contexte
    - Convertir des grammaires en automates à pile (PDA, DPDA, NPDA)
    - Convertir des automates à pile en grammaires
    - Normaliser les grammaires (forme normale de Chomsky, Greibach)
    - Optimiser et analyser les grammaires
    - Sérialiser et désérialiser les grammaires

    Exemple d'utilisation :
        parser = GrammarParser()
        grammar = parser.parse_grammar("S -> aSb | ε")
        pda = parser.grammar_to_pda(grammar)
        assert pda.accepts('aabb')  # True
    """

    def __init__(
        self,
        grammar: Optional[ContextFreeGrammar] = None,
        strict_validation: bool = True,
    ) -> None:
        """Initialise le parser de grammaires.

        :param grammar: Grammaire optionnelle à parser
        :param strict_validation: Validation stricte des grammaires
        :raises GrammarError: Si la grammaire n'est pas valide
        """
        self._grammar: Optional[ContextFreeGrammar] = None
        self._strict_validation = strict_validation
        self._cache: Dict[str, Any] = {}

        if grammar is not None:
            self.load_grammar(grammar)

    def load_grammar(self, grammar: ContextFreeGrammar) -> None:
        """Charge une grammaire dans le parser.

        :param grammar: Grammaire à charger
        :raises GrammarError: Si la grammaire n'est pas valide
        """
        if self._strict_validation:
            self.validate_grammar(grammar)

        self._grammar = grammar
        self._cache.clear()

    def load_from_string(self, grammar_string: str) -> None:
        """Charge une grammaire depuis une chaîne de caractères.

        :param grammar_string: Représentation textuelle de la grammaire
        :raises GrammarError: Si la grammaire n'est pas valide
        """
        grammar = self.parse_grammar(grammar_string)
        self.load_grammar(grammar)

    def load_from_file(self, file_path: str) -> None:
        """Charge une grammaire depuis un fichier.

        :param file_path: Chemin vers le fichier
        :raises GrammarError: Si la grammaire n'est pas valide
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.load_from_string(content)
        except FileNotFoundError:
            raise GrammarError(f"Fichier non trouvé : {file_path}")
        except Exception as e:
            raise GrammarError(f"Erreur lors de la lecture du fichier : {e}")

    def parse_grammar(self, grammar_string: str) -> ContextFreeGrammar:
        """Parse une grammaire depuis une chaîne de caractères.

        :param grammar_string: Représentation textuelle de la grammaire
        :return: Grammaire parsée
        :raises GrammarParseError: Si le parsing échoue
        """
        try:
            # Nettoyage de la chaîne
            lines = [
                line.strip()
                for line in grammar_string.strip().split("\n")
                if line.strip()
            ]

            if not lines:
                raise GrammarParseError("Grammaire vide")

            variables: Set[str] = set()
            terminals: Set[str] = set()
            productions: Set[Production] = set()
            start_symbol: Optional[str] = None

            for line in lines:
                if "->" not in line:
                    raise GrammarParseError(f"Ligne invalide : {line}")

                parts = line.split("->", 1)
                if len(parts) != 2:
                    raise GrammarParseError(f"Ligne invalide : {line}")

                left_side = parts[0].strip()
                right_side = parts[1].strip()

                if not left_side:
                    raise GrammarParseError(f"Variable de gauche vide : {line}")

                # Ajout de la variable
                variables.add(left_side)

                # Définition du symbole de départ
                if start_symbol is None:
                    start_symbol = left_side

                # Parsing du côté droit
                if right_side == "ε" or right_side == "":
                    # Production vide
                    productions.add(Production(left_side, ()))
                else:
                    # Parsing des alternatives
                    alternatives = [alt.strip() for alt in right_side.split("|")]

                    for alt in alternatives:
                        if not alt:
                            continue

                        # Parsing des symboles
                        symbols = self._parse_symbols(alt)
                        productions.add(Production(left_side, symbols))

                        # Ajout des terminaux (uniquement les symboles atomiques)
                        for symbol in symbols:
                            if (
                                symbol not in variables
                                and len(symbol) == 1
                                and symbol.islower()
                            ):
                                terminals.add(symbol)

            if start_symbol is None:
                raise GrammarParseError("Aucun symbole de départ trouvé")

            grammar = ContextFreeGrammar(
                variables=variables,
                terminals=terminals,
                productions=productions,
                start_symbol=start_symbol,
            )

            if self._strict_validation:
                self.validate_grammar(grammar)

            return grammar

        except GrammarParseError:
            raise
        except Exception as e:
            raise GrammarParseError(f"Erreur lors du parsing : {e}")

    def _parse_symbols(self, symbol_string: str) -> Tuple[str, ...]:
        """Parse une chaîne de symboles.

        :param symbol_string: Chaîne de symboles à parser
        :return: Tuple des symboles
        """
        # Si la chaîne contient des espaces, séparer par espaces
        if " " in symbol_string:
            symbols = [s.strip() for s in symbol_string.split() if s.strip()]
        else:
            # Sinon, séparer caractère par caractère
            symbols = list(symbol_string)

        # Validation des symboles
        for symbol in symbols:
            if not symbol:
                raise GrammarParseError(f"Symbole invalide : {symbol}")

        return tuple(symbols)

    def validate_grammar(self, grammar: ContextFreeGrammar) -> bool:
        """Valide une grammaire.

        :param grammar: Grammaire à valider
        :return: True si la grammaire est valide, False sinon
        :raises GrammarError: Si la grammaire n'est pas valide
        """
        try:
            # Vérification des variables
            if not grammar.variables:
                raise GrammarValidationError("Aucune variable définie")

            # Vérification du symbole de départ
            if grammar.start_symbol not in grammar.variables:
                raise GrammarValidationError(
                    f"Symbole de départ '{grammar.start_symbol}' n'est pas une variable"
                )

            # Vérification des productions
            if not grammar.productions:
                raise GrammarValidationError("Aucune production définie")

            for production in grammar.productions:
                # Vérification de la variable de gauche
                if production.left_side not in grammar.variables:
                    raise GrammarValidationError(
                        f"Variable '{production.left_side}' non définie"
                    )

                # Vérification des symboles de droite
                for symbol in production.right_side:
                    if (
                        symbol not in grammar.variables
                        and symbol not in grammar.terminals
                    ):
                        raise GrammarValidationError(f"Symbole '{symbol}' non défini")

            # Vérification de l'accessibilité des variables (avertissement seulement)
            accessible_vars = self._get_accessible_variables(grammar)
            if grammar.variables - accessible_vars:
                unused_vars = grammar.variables - accessible_vars
                # Avertissement seulement, pas d'erreur
                pass

            # Vérification de la génération des variables (avertissement seulement)
            generating_vars = self._get_generating_variables(grammar)
            if grammar.variables - generating_vars:
                non_generating_vars = grammar.variables - generating_vars
                # Avertissement seulement, pas d'erreur
                pass

            return True

        except GrammarValidationError:
            raise
        except Exception as e:
            raise GrammarValidationError(f"Erreur de validation : {e}")

    def _get_accessible_variables(self, grammar: ContextFreeGrammar) -> Set[str]:
        """Obtient les variables accessibles depuis le symbole de départ.

        :param grammar: Grammaire à analyser
        :return: Ensemble des variables accessibles
        """
        accessible = {grammar.start_symbol}
        changed = True

        while changed:
            changed = False
            for production in grammar.productions:
                if production.left_side in accessible:
                    for symbol in production.right_side:
                        if symbol in grammar.variables and symbol not in accessible:
                            accessible.add(symbol)
                            changed = True

        return accessible

    def _get_generating_variables(self, grammar: ContextFreeGrammar) -> Set[str]:
        """Obtient les variables génératrices.

        :param grammar: Grammaire à analyser
        :return: Ensemble des variables génératrices
        """
        generating = set()
        changed = True

        # Variables qui génèrent des chaînes de terminaux
        while changed:
            changed = False
            for production in grammar.productions:
                if production.left_side not in generating:
                    # Vérification si tous les symboles de droite sont générateurs ou terminaux
                    if all(
                        symbol in generating or symbol in grammar.terminals
                        for symbol in production.right_side
                    ):
                        generating.add(production.left_side)
                        changed = True

        return generating

    def analyze_grammar(self, grammar: ContextFreeGrammar) -> Dict[str, Any]:
        """Analyse les propriétés d'une grammaire.

        :param grammar: Grammaire à analyser
        :return: Dictionnaire avec les propriétés de la grammaire
        """
        analysis = {
            "type": self._get_grammar_type(grammar),
            "left_recursive": self._has_left_recursion(grammar),
            "right_recursive": self._has_right_recursion(grammar),
            "ambiguous": self._detect_ambiguity(grammar),
            "empty_productions": self._has_empty_productions(grammar),
            "accessible_variables": self._get_accessible_variables(grammar),
            "generating_variables": self._get_generating_variables(grammar),
            "useless_variables": self._get_useless_variables(grammar),
            "production_count": len(grammar.productions),
            "variable_count": len(grammar.variables),
            "terminal_count": len(grammar.terminals),
        }

        return analysis

    def _get_grammar_type(self, grammar: ContextFreeGrammar) -> GrammarType:
        """Détermine le type de grammaire.

        :param grammar: Grammaire à analyser
        :return: Type de grammaire
        """
        if self._is_chomsky_normal_form(grammar):
            return GrammarType.CHOMSKY_NORMAL_FORM
        elif self._is_greibach_normal_form(grammar):
            return GrammarType.GREIBACH_NORMAL_FORM
        elif self._has_left_recursion(grammar):
            return GrammarType.LEFT_RECURSIVE
        elif self._has_right_recursion(grammar):
            return GrammarType.RIGHT_RECURSIVE
        elif self._detect_ambiguity(grammar):
            return GrammarType.AMBIGUOUS
        else:
            return GrammarType.GENERAL

    def _is_chomsky_normal_form(self, grammar: ContextFreeGrammar) -> bool:
        """Vérifie si la grammaire est en forme normale de Chomsky.

        :param grammar: Grammaire à analyser
        :return: True si en forme normale de Chomsky
        """
        for production in grammar.productions:
            if not production.right_side:  # Production vide
                if production.left_side != grammar.start_symbol:
                    return False
            elif len(production.right_side) == 1:  # Production unitaire
                if production.right_side[0] not in grammar.terminals:
                    return False
            elif len(production.right_side) == 2:  # Production binaire
                if not all(
                    symbol in grammar.variables for symbol in production.right_side
                ):
                    return False
            else:  # Production de plus de 2 symboles
                return False

        # Vérifier qu'il n'y a pas de productions unitaires
        if grammar.has_unit_productions():
            return False

        return True

    def _is_greibach_normal_form(self, grammar: ContextFreeGrammar) -> bool:
        """Vérifie si la grammaire est en forme normale de Greibach.

        :param grammar: Grammaire à analyser
        :return: True si en forme normale de Greibach
        """
        for production in grammar.productions:
            if not production.right_side:  # Production vide
                if production.left_side != grammar.start_symbol:
                    return False
            elif len(production.right_side) == 1:
                # Production unitaire terminale
                if production.right_side[0] not in grammar.terminals:
                    return False
            else:
                # Production avec plusieurs symboles
                if production.right_side[0] not in grammar.terminals:
                    return False
                # Tous les autres symboles doivent être des variables
                for symbol in production.right_side[1:]:
                    if symbol not in grammar.variables:
                        return False

        return True

    def _has_left_recursion(self, grammar: ContextFreeGrammar) -> bool:
        """Vérifie si la grammaire a de la récursivité gauche.

        :param grammar: Grammaire à analyser
        :return: True si récursivité gauche détectée
        """
        for production in grammar.productions:
            if (
                production.right_side
                and production.right_side[0] == production.left_side
            ):
                return True
        return False

    def _has_right_recursion(self, grammar: ContextFreeGrammar) -> bool:
        """Vérifie si la grammaire a de la récursivité droite.

        :param grammar: Grammaire à analyser
        :return: True si récursivité droite détectée
        """
        for production in grammar.productions:
            if (
                production.right_side
                and production.right_side[-1] == production.left_side
            ):
                return True
        return False

    def _detect_ambiguity(self, grammar: ContextFreeGrammar) -> bool:
        """Détecte si une grammaire est ambiguë.

        :param grammar: Grammaire à analyser
        :return: True si la grammaire est ambiguë
        """
        # Détection simple d'ambiguïté : productions avec même côté gauche et droite
        productions_by_left = {}
        for production in grammar.productions:
            if production.left_side not in productions_by_left:
                productions_by_left[production.left_side] = []
            productions_by_left[production.left_side].append(production.right_side)

        for left_side, right_sides in productions_by_left.items():
            if len(right_sides) > 1:
                # Vérification des conflits potentiels
                for i, right1 in enumerate(right_sides):
                    for right2 in right_sides[i + 1 :]:
                        if right1 == right2:
                            return True

        return False

    def _has_empty_productions(self, grammar: ContextFreeGrammar) -> bool:
        """Vérifie si la grammaire a des productions vides.

        :param grammar: Grammaire à analyser
        :return: True si productions vides détectées
        """
        for production in grammar.productions:
            if not production.right_side:
                return True
        return False

    def _get_useless_variables(self, grammar: ContextFreeGrammar) -> Set[str]:
        """Obtient les variables inutiles.

        :param grammar: Grammaire à analyser
        :return: Ensemble des variables inutiles
        """
        accessible = self._get_accessible_variables(grammar)
        generating = self._get_generating_variables(grammar)

        return grammar.variables - (accessible & generating)

    def __str__(self) -> str:
        """Représentation textuelle du parser."""
        if self._grammar is None:
            return "GrammarParser(grammar=None)"
        return f"GrammarParser(grammar={self._grammar.start_symbol})"

    def __repr__(self) -> str:
        """Représentation détaillée du parser."""
        return self.__str__()

    # ============================================================================
    # CONVERSIONS GRAMMAIRE ↔ PDA
    # ============================================================================

    def grammar_to_pda(self, grammar: ContextFreeGrammar) -> "PDA":
        """Convertit une grammaire en PDA.

        :param grammar: Grammaire à convertir
        :return: PDA équivalent
        :raises GrammarConversionError: Si la conversion échoue
        """
        try:
            from .pda import PDA

            # Création des états
            states = {"q0", "q1", "q2"}

            # Création de l'alphabet d'entrée
            input_alphabet = grammar.terminals.copy()

            # Création de l'alphabet de pile
            stack_alphabet = grammar.variables.union(grammar.terminals).union({"Z"})

            # Création des transitions
            transitions = {}

            # Transition initiale : q0 -> q1 avec Z sur la pile
            transitions[("q0", "", "Z")] = {("q1", f"{grammar.start_symbol}Z")}

            # Transitions pour chaque production
            for production in grammar.productions:
                if production.is_empty():
                    # Production vide : consommer la variable de la pile
                    transitions[("q1", "", production.left_side)] = {("q1", "")}
                else:
                    # Production normale : remplacer la variable par les symboles de droite
                    right_side_str = "".join(reversed(production.right_side))
                    transitions[("q1", "", production.left_side)] = {
                        ("q1", right_side_str)
                    }

            # Transitions pour consommer les terminaux
            for terminal in grammar.terminals:
                transitions[("q1", terminal, terminal)] = {("q1", "")}

            # Transition finale : q1 -> q2 avec Z sur la pile
            transitions[("q1", "", "Z")] = {("q2", "Z")}

            # Création du PDA
            pda = PDA(
                states=states,
                input_alphabet=input_alphabet,
                stack_alphabet=stack_alphabet,
                transitions=transitions,
                initial_state="q0",
                initial_stack_symbol="Z",
                final_states={"q2"},
            )

            return pda

        except Exception as e:
            raise GrammarConversionError(
                f"Erreur lors de la conversion grammaire → PDA : {e}"
            )

    def pda_to_grammar(self, pda: "PDA") -> ContextFreeGrammar:
        """Convertit un PDA en grammaire.

        :param pda: PDA à convertir
        :return: Grammaire équivalente
        :raises GrammarConversionError: Si la conversion échoue
        """
        try:
            # Création des variables pour chaque paire d'états
            variables = set()
            for state1 in pda.states:
                for state2 in pda.states:
                    variables.add(f"[{state1},{state2}]")

            # Ajout des variables pour les transitions
            for state in pda.states:
                for stack_symbol in pda.stack_alphabet:
                    variables.add(f"[{state},{stack_symbol},{state}]")

            # Création des terminaux
            terminals = pda.input_alphabet.copy()

            # Création des productions
            productions = set()

            # Productions pour les transitions
            for (
                state,
                input_symbol,
                stack_symbol,
            ), next_states in pda._transitions.items():
                for next_state, stack_operations in next_states.items():
                    if input_symbol == "":
                        # Transition epsilon
                        if not stack_operations:
                            # Dépilage simple
                            productions.add(
                                Production(f"[{state},{stack_symbol},{next_state}]", ())
                            )
                        else:
                            # Empilage
                            if len(stack_operations) == 1:
                                productions.add(
                                    Production(
                                        f"[{state},{stack_symbol},{next_state}]",
                                        (stack_operations,),
                                    )
                                )
                            else:
                                # Empilage multiple - création de variables intermédiaires
                                current_var = f"[{state},{stack_symbol},{next_state}]"
                                for i, symbol in enumerate(stack_operations):
                                    if i == 0:
                                        productions.add(
                                            Production(current_var, (symbol,))
                                        )
                                    else:
                                        new_var = (
                                            f"[{state},{stack_symbol},{next_state}]_{i}"
                                        )
                                        variables.add(new_var)
                                        productions.add(
                                            Production(current_var, (symbol, new_var))
                                        )
                    else:
                        # Transition avec symbole d'entrée
                        if not stack_operations:
                            productions.add(
                                Production(
                                    f"[{state},{stack_symbol},{next_state}]",
                                    (input_symbol,),
                                )
                            )
                        else:
                            # Transition avec empilage
                            if len(stack_operations) == 1:
                                productions.add(
                                    Production(
                                        f"[{state},{stack_symbol},{next_state}]",
                                        (input_symbol, stack_operations),
                                    )
                                )
                            else:
                                # Empilage multiple
                                current_var = f"[{state},{stack_symbol},{next_state}]"
                                for i, symbol in enumerate(stack_operations):
                                    if i == 0:
                                        productions.add(
                                            Production(
                                                current_var, (input_symbol, symbol)
                                            )
                                        )
                                    else:
                                        new_var = (
                                            f"[{state},{stack_symbol},{next_state}]_{i}"
                                        )
                                        variables.add(new_var)
                                        productions.add(
                                            Production(
                                                current_var,
                                                (input_symbol, symbol, new_var),
                                            )
                                        )

            # Symbole de départ
            start_symbol = f"[{pda.initial_state},{pda.initial_stack_symbol},{list(pda.final_states)[0]}]"

            # Création de la grammaire
            grammar = ContextFreeGrammar(
                variables=variables,
                terminals=terminals,
                productions=productions,
                start_symbol=start_symbol,
            )

            return grammar

        except Exception as e:
            raise GrammarConversionError(
                f"Erreur lors de la conversion PDA → grammaire : {e}"
            )

    def grammar_to_dpda(self, grammar: ContextFreeGrammar) -> "DPDA":
        """Convertit une grammaire en DPDA si possible.

        :param grammar: Grammaire à convertir
        :return: DPDA équivalent
        :raises GrammarConversionError: Si la conversion n'est pas possible
        """
        try:
            from .dpda import DPDA

            # Conversion via PDA
            pda = self.grammar_to_pda(grammar)

            # Vérification du déterminisme
            if not self._is_deterministic_pda(pda):
                raise GrammarConversionError(
                    "La grammaire ne peut pas être convertie en DPDA (non-déterministe)"
                )

            # Création du DPDA
            dpda = DPDA(
                states=pda.states,
                input_alphabet=pda.input_alphabet,
                stack_alphabet=pda.stack_alphabet,
                transitions=self._convert_to_dpda_transitions(pda._transitions),
                initial_state=pda.initial_state,
                initial_stack_symbol=pda.initial_stack_symbol,
                final_states=pda.final_states,
            )

            return dpda

        except Exception as e:
            raise GrammarConversionError(
                f"Erreur lors de la conversion grammaire → DPDA : {e}"
            )

    def grammar_to_npda(self, grammar: ContextFreeGrammar) -> "NPDA":
        """Convertit une grammaire en NPDA.

        :param grammar: Grammaire à convertir
        :return: NPDA équivalent
        :raises GrammarConversionError: Si la conversion échoue
        """
        try:
            from .npda import NPDA

            # Conversion via PDA
            pda = self.grammar_to_pda(grammar)

            # Création du NPDA
            npda = NPDA(
                states=pda.states,
                input_alphabet=pda.input_alphabet,
                stack_alphabet=pda.stack_alphabet,
                transitions=pda._transitions,
                initial_state=pda.initial_state,
                initial_stack_symbol=pda.initial_stack_symbol,
                final_states=pda.final_states,
            )

            return npda

        except Exception as e:
            raise GrammarConversionError(
                f"Erreur lors de la conversion grammaire → NPDA : {e}"
            )

    def _is_deterministic_pda(self, pda: "PDA") -> bool:
        """Vérifie si un PDA est déterministe.

        :param pda: PDA à vérifier
        :return: True si le PDA est déterministe
        """
        for (
            state,
            input_symbol,
            stack_symbol,
        ), next_states in pda._transitions.items():
            if len(next_states) > 1:
                return False
        return True

    def _convert_to_dpda_transitions(self, transitions: Dict) -> Dict:
        """Convertit les transitions PDA en transitions DPDA.

        :param transitions: Transitions PDA
        :return: Transitions DPDA
        """
        dpda_transitions = {}
        for (state, input_symbol, stack_symbol), next_states in transitions.items():
            if len(next_states) == 1:
                next_state, stack_operations = list(next_states)[0]
                dpda_transitions[(state, input_symbol, stack_symbol)] = (
                    next_state,
                    stack_operations,
                )
        return dpda_transitions

    # ============================================================================
    # NORMALISATION DES GRAMMAIRES
    # ============================================================================

    def to_chomsky_normal_form(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
        """Convertit une grammaire en forme normale de Chomsky.

        :param grammar: Grammaire à convertir
        :return: Grammaire en forme normale de Chomsky
        :raises GrammarNormalizationError: Si la conversion échoue
        """
        try:
            # Étape 1 : Élimination des productions vides
            grammar = self.eliminate_empty_productions(grammar)

            # Étape 2 : Élimination des productions unitaires
            grammar = self.eliminate_unit_productions(grammar)

            # Étape 3 : Élimination des symboles inaccessibles
            grammar = self.eliminate_inaccessible_symbols(grammar)

            # Étape 4 : Élimination des symboles non-générateurs
            grammar = self.eliminate_non_generating_symbols(grammar)

            # Étape 5 : Conversion en productions binaires
            grammar = self._convert_to_binary_productions(grammar)

            return grammar

        except Exception as e:
            raise GrammarNormalizationError(
                f"Erreur lors de la conversion en forme normale de Chomsky : {e}"
            )

    def to_greibach_normal_form(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Convertit une grammaire en forme normale de Greibach.

        :param grammar: Grammaire à convertir
        :return: Grammaire en forme normale de Greibach
        :raises GrammarNormalizationError: Si la conversion échoue
        """
        try:
            # Étape 1 : Conversion en forme normale de Chomsky
            grammar = self.to_chomsky_normal_form(grammar)

            # Étape 2 : Élimination de la récursivité gauche
            grammar = self.eliminate_left_recursion(grammar)

            # Étape 3 : Conversion en productions de la forme A -> aα
            grammar = self._convert_to_greibach_form(grammar)

            return grammar

        except Exception as e:
            raise GrammarNormalizationError(
                f"Erreur lors de la conversion en forme normale de Greibach : {e}"
            )

    def eliminate_empty_productions(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Élimine les productions vides d'une grammaire.

        :param grammar: Grammaire à traiter
        :return: Grammaire sans productions vides
        :raises GrammarNormalizationError: Si l'élimination échoue
        """
        try:
            # Identification des variables qui peuvent générer ε
            nullable_variables = self._get_nullable_variables(grammar)

            # Création des nouvelles productions
            new_productions = set()

            for production in grammar.productions:
                if not production.is_empty():
                    # Génération de toutes les combinaisons possibles
                    combinations = self._generate_combinations(
                        production.right_side, nullable_variables
                    )
                    for combination in combinations:
                        if combination:  # Éviter les productions vides
                            new_productions.add(
                                Production(production.left_side, combination)
                            )
                else:
                    # Production vide - seulement si c'est le symbole de départ
                    if production.left_side == grammar.start_symbol:
                        new_productions.add(production)

            # Création de la nouvelle grammaire
            new_grammar = ContextFreeGrammar(
                variables=grammar.variables,
                terminals=grammar.terminals,
                productions=new_productions,
                start_symbol=grammar.start_symbol,
                name=grammar.name,
            )

            return new_grammar

        except Exception as e:
            raise GrammarNormalizationError(
                f"Erreur lors de l'élimination des productions vides : {e}"
            )

    def eliminate_left_recursion(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Élimine la récursivité gauche d'une grammaire.

        :param grammar: Grammaire à traiter
        :return: Grammaire sans récursivité gauche
        :raises GrammarNormalizationError: Si l'élimination échoue
        """
        try:
            new_productions = set()
            new_variables = grammar.variables.copy()

            # Traitement de chaque variable
            for variable in sorted(grammar.variables):
                # Séparation des productions récursives et non-récursives
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
                    # Création d'une nouvelle variable pour la récursivité
                    new_var = f"{variable}'"
                    new_variables.add(new_var)

                    # Ajout des productions non-récursives
                    for production in non_recursive_productions:
                        if production.right_side:
                            new_productions.add(
                                Production(variable, production.right_side + (new_var,))
                            )
                        else:
                            new_productions.add(Production(variable, (new_var,)))

                    # Ajout des productions récursives
                    for production in recursive_productions:
                        if len(production.right_side) > 1:
                            new_productions.add(
                                Production(
                                    new_var, production.right_side[1:] + (new_var,)
                                )
                            )
                        else:
                            new_productions.add(Production(new_var, (new_var,)))

                    # Production vide pour la nouvelle variable
                    new_productions.add(Production(new_var, ()))
                else:
                    # Pas de récursivité - ajout des productions telles quelles
                    for production in non_recursive_productions:
                        new_productions.add(production)

            # Création de la nouvelle grammaire
            new_grammar = ContextFreeGrammar(
                variables=new_variables,
                terminals=grammar.terminals,
                productions=new_productions,
                start_symbol=grammar.start_symbol,
                name=grammar.name,
            )

            return new_grammar

        except Exception as e:
            raise GrammarNormalizationError(
                f"Erreur lors de l'élimination de la récursivité gauche : {e}"
            )

    def eliminate_unit_productions(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Élimine les productions unitaires d'une grammaire.

        :param grammar: Grammaire à traiter
        :return: Grammaire sans productions unitaires
        :raises GrammarNormalizationError: Si l'élimination échoue
        """
        try:
            # Identification des chaînes de productions unitaires
            unit_chains = self._get_unit_chains(grammar)

            # Création des nouvelles productions
            new_productions = set()

            # D'abord, ajouter toutes les productions non-unitaires
            for production in grammar.productions:
                if not production.is_unit():
                    new_productions.add(production)

            # Ensuite, remplacer les productions unitaires
            for production in grammar.productions:
                if production.is_unit():
                    target_var = production.right_side[0]
                    if target_var in unit_chains:
                        for chain_var in unit_chains[target_var]:
                            for chain_production in grammar.productions:
                                if (
                                    chain_production.left_side == chain_var
                                    and not chain_production.is_unit()
                                ):
                                    new_productions.add(
                                        Production(
                                            production.left_side,
                                            chain_production.right_side,
                                        )
                                    )

            # Création de la nouvelle grammaire
            new_grammar = ContextFreeGrammar(
                variables=grammar.variables,
                terminals=grammar.terminals,
                productions=new_productions,
                start_symbol=grammar.start_symbol,
                name=grammar.name,
            )

            return new_grammar

        except Exception as e:
            raise GrammarNormalizationError(
                f"Erreur lors de l'élimination des productions unitaires : {e}"
            )

    def eliminate_inaccessible_symbols(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Élimine les symboles inaccessibles d'une grammaire.

        :param grammar: Grammaire à traiter
        :return: Grammaire sans symboles inaccessibles
        :raises GrammarNormalizationError: Si l'élimination échoue
        """
        try:
            # Identification des symboles accessibles
            accessible_variables = self._get_accessible_variables(grammar)
            accessible_terminals = set()

            for production in grammar.productions:
                if production.left_side in accessible_variables:
                    for symbol in production.right_side:
                        if symbol in grammar.terminals:
                            accessible_terminals.add(symbol)

            # Filtrage des productions
            new_productions = {
                production
                for production in grammar.productions
                if production.left_side in accessible_variables
            }

            # Création de la nouvelle grammaire
            new_grammar = ContextFreeGrammar(
                variables=accessible_variables,
                terminals=accessible_terminals,
                productions=new_productions,
                start_symbol=grammar.start_symbol,
                name=grammar.name,
            )

            return new_grammar

        except Exception as e:
            raise GrammarNormalizationError(
                f"Erreur lors de l'élimination des symboles inaccessibles : {e}"
            )

    def eliminate_non_generating_symbols(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Élimine les symboles non-générateurs d'une grammaire.

        :param grammar: Grammaire à traiter
        :return: Grammaire sans symboles non-générateurs
        :raises GrammarNormalizationError: Si l'élimination échoue
        """
        try:
            # Identification des symboles générateurs
            generating_variables = self._get_generating_variables(grammar)
            generating_terminals = grammar.terminals.copy()

            # Filtrage des productions
            new_productions = set()
            for production in grammar.productions:
                if production.left_side in generating_variables and all(
                    symbol in generating_variables or symbol in generating_terminals
                    for symbol in production.right_side
                ):
                    new_productions.add(production)

            # Création de la nouvelle grammaire
            new_grammar = ContextFreeGrammar(
                variables=generating_variables,
                terminals=generating_terminals,
                productions=new_productions,
                start_symbol=grammar.start_symbol,
                name=grammar.name,
            )

            return new_grammar

        except Exception as e:
            raise GrammarNormalizationError(
                f"Erreur lors de l'élimination des symboles non-générateurs : {e}"
            )

    def _get_nullable_variables(self, grammar: ContextFreeGrammar) -> Set[str]:
        """Obtient les variables qui peuvent générer ε.

        :param grammar: Grammaire à analyser
        :return: Ensemble des variables nullables
        """
        nullable = set()
        changed = True

        while changed:
            changed = False
            for production in grammar.productions:
                if production.is_empty():
                    if production.left_side not in nullable:
                        nullable.add(production.left_side)
                        changed = True
                elif all(symbol in nullable for symbol in production.right_side):
                    if production.left_side not in nullable:
                        nullable.add(production.left_side)
                        changed = True

        return nullable

    def _generate_combinations(
        self, symbols: Tuple[str, ...], nullable_variables: Set[str]
    ) -> List[Tuple[str, ...]]:
        """Génère toutes les combinaisons possibles en éliminant les variables nullables.

        :param symbols: Tuple des symboles
        :param nullable_variables: Variables qui peuvent être nullables
        :return: Liste des combinaisons possibles
        """
        if not symbols:
            return [()]

        combinations = []
        first_symbol = symbols[0]
        rest_combinations = self._generate_combinations(symbols[1:], nullable_variables)

        for rest_combo in rest_combinations:
            # Ajout de la combinaison avec le premier symbole
            combinations.append((first_symbol,) + rest_combo)

            # Ajout de la combinaison sans le premier symbole s'il est nullable
            if first_symbol in nullable_variables:
                combinations.append(rest_combo)

        return combinations

    def _get_unit_chains(self, grammar: ContextFreeGrammar) -> Dict[str, Set[str]]:
        """Obtient les chaînes de productions unitaires.

        :param grammar: Grammaire à analyser
        :return: Dictionnaire des chaînes unitaires
        """
        chains = {}

        for variable in grammar.variables:
            chains[variable] = {variable}
            changed = True

            while changed:
                changed = False
                for production in grammar.productions:
                    if (
                        production.left_side in chains[variable]
                        and production.is_unit()
                        and production.right_side[0] not in chains[variable]
                    ):
                        chains[variable].add(production.right_side[0])
                        changed = True

        return chains

    def _convert_to_binary_productions(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Convertit les productions en productions binaires.

        :param grammar: Grammaire à convertir
        :return: Grammaire avec productions binaires
        """
        new_productions = set()
        new_variables = grammar.variables.copy()
        counter = 0

        for production in grammar.productions:
            if len(production.right_side) <= 2:
                new_productions.add(production)
            else:
                # Conversion en productions binaires
                current_var = production.left_side
                symbols = production.right_side

                for i in range(len(symbols) - 2):
                    new_var = f"X{counter}"
                    counter += 1
                    new_variables.add(new_var)

                    new_productions.add(Production(current_var, (symbols[i], new_var)))
                    current_var = new_var

                # Dernière production
                new_productions.add(Production(current_var, symbols[-2:]))

        return ContextFreeGrammar(
            variables=new_variables,
            terminals=grammar.terminals,
            productions=new_productions,
            start_symbol=grammar.start_symbol,
            name=grammar.name,
        )

    def _convert_to_greibach_form(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Convertit une grammaire en forme normale de Greibach.

        :param grammar: Grammaire à convertir
        :return: Grammaire en forme normale de Greibach
        """
        # Cette méthode est complexe et nécessite une implémentation complète
        # Pour l'instant, on retourne la grammaire telle quelle
        return grammar

    # ============================================================================
    # OPTIMISATIONS ET ANALYSES
    # ============================================================================

    def optimize_grammar(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
        """Optimise une grammaire.

        :param grammar: Grammaire à optimiser
        :return: Grammaire optimisée
        :raises GrammarOptimizationError: Si l'optimisation échoue
        """
        try:
            # Étape 1 : Élimination des symboles inutiles
            grammar = self.eliminate_inaccessible_symbols(grammar)
            grammar = self.eliminate_non_generating_symbols(grammar)

            # Étape 2 : Fusion des productions équivalentes
            grammar = self._merge_equivalent_productions(grammar)

            # Étape 3 : Réduction du nombre de productions
            grammar = self._reduce_productions(grammar)

            return grammar

        except Exception as e:
            raise GrammarOptimizationError(f"Erreur lors de l'optimisation : {e}")

    def detect_ambiguity(self, grammar: ContextFreeGrammar) -> bool:
        """Détecte si une grammaire est ambiguë.

        :param grammar: Grammaire à analyser
        :return: True si la grammaire est ambiguë
        """
        return self._detect_ambiguity(grammar)

    def analyze_recursion(self, grammar: ContextFreeGrammar) -> Dict[str, Any]:
        """Analyse la récursivité d'une grammaire.

        :param grammar: Grammaire à analyser
        :return: Dictionnaire avec l'analyse de récursivité
        """
        analysis = {
            "left_recursive": self._has_left_recursion(grammar),
            "right_recursive": self._has_right_recursion(grammar),
            "left_recursive_variables": self._get_left_recursive_variables(grammar),
            "right_recursive_variables": self._get_right_recursive_variables(grammar),
            "recursion_depth": self._get_max_recursion_depth(grammar),
        }

        return analysis

    def _merge_equivalent_productions(
        self, grammar: ContextFreeGrammar
    ) -> ContextFreeGrammar:
        """Fusionne les productions équivalentes.

        :param grammar: Grammaire à traiter
        :return: Grammaire avec productions fusionnées
        """
        # Groupement des productions par côté gauche
        productions_by_left = {}
        for production in grammar.productions:
            if production.left_side not in productions_by_left:
                productions_by_left[production.left_side] = []
            productions_by_left[production.left_side].append(production.right_side)

        # Fusion des productions avec même côté gauche
        new_productions = set()
        for left_side, right_sides in productions_by_left.items():
            # Suppression des doublons
            unique_right_sides = []
            for right_side in right_sides:
                if right_side not in unique_right_sides:
                    unique_right_sides.append(right_side)

            # Création des productions fusionnées
            for right_side in unique_right_sides:
                new_productions.add(Production(left_side, right_side))

        return ContextFreeGrammar(
            variables=grammar.variables,
            terminals=grammar.terminals,
            productions=new_productions,
            start_symbol=grammar.start_symbol,
            name=grammar.name,
        )

    def _reduce_productions(self, grammar: ContextFreeGrammar) -> ContextFreeGrammar:
        """Réduit le nombre de productions.

        :param grammar: Grammaire à traiter
        :return: Grammaire avec moins de productions
        """
        # Pour l'instant, on retourne la grammaire telle quelle
        # Une implémentation complète nécessiterait des algorithmes plus sophistiqués
        return grammar

    def _get_left_recursive_variables(self, grammar: ContextFreeGrammar) -> Set[str]:
        """Obtient les variables avec récursivité gauche.

        :param grammar: Grammaire à analyser
        :return: Ensemble des variables récursives à gauche
        """
        left_recursive = set()
        for production in grammar.productions:
            if (
                production.right_side
                and production.right_side[0] == production.left_side
            ):
                left_recursive.add(production.left_side)
        return left_recursive

    def _get_right_recursive_variables(self, grammar: ContextFreeGrammar) -> Set[str]:
        """Obtient les variables avec récursivité droite.

        :param grammar: Grammaire à analyser
        :return: Ensemble des variables récursives à droite
        """
        right_recursive = set()
        for production in grammar.productions:
            if (
                production.right_side
                and production.right_side[-1] == production.left_side
            ):
                right_recursive.add(production.left_side)
        return right_recursive

    def _get_max_recursion_depth(self, grammar: ContextFreeGrammar) -> int:
        """Obtient la profondeur maximale de récursivité.

        :param grammar: Grammaire à analyser
        :return: Profondeur maximale de récursivité
        """
        # Implémentation simplifiée
        max_depth = 0
        for production in grammar.productions:
            if (
                production.right_side
                and production.right_side[0] == production.left_side
            ):
                max_depth = max(max_depth, len(production.right_side))
        return max_depth

    # ============================================================================
    # MÉTHODES UTILITAIRES
    # ============================================================================

    def to_dict(self, grammar: ContextFreeGrammar) -> Dict[str, Any]:
        """Convertit une grammaire en dictionnaire.

        :param grammar: Grammaire à sérialiser
        :return: Représentation dictionnaire de la grammaire
        """
        return {
            "variables": list(grammar.variables),
            "terminals": list(grammar.terminals),
            "productions": [
                {"left_side": production.left_side, "right_side": production.right_side}
                for production in grammar.productions
            ],
            "start_symbol": grammar.start_symbol,
            "name": grammar.name,
        }

    def from_dict(self, data: Dict[str, Any]) -> ContextFreeGrammar:
        """Crée une grammaire à partir d'un dictionnaire.

        :param data: Données de la grammaire
        :return: Grammaire créée
        :raises GrammarError: Si les données sont invalides
        """
        try:
            productions = set()
            for prod_data in data["productions"]:
                productions.add(
                    Production(prod_data["left_side"], tuple(prod_data["right_side"]))
                )

            return ContextFreeGrammar(
                variables=set(data["variables"]),
                terminals=set(data["terminals"]),
                productions=productions,
                start_symbol=data["start_symbol"],
                name=data.get("name"),
            )
        except Exception as e:
            raise GrammarError(f"Erreur lors de la création de la grammaire : {e}")

    def export_grammar(self, grammar: ContextFreeGrammar, format: str = "text") -> str:
        """Exporte une grammaire dans un format donné.

        :param grammar: Grammaire à exporter
        :param format: Format d'export (text, json, xml)
        :return: Représentation de la grammaire
        """
        if format == "text":
            return str(grammar)
        elif format == "json":
            return json.dumps(self.to_dict(grammar), indent=2)
        elif format == "xml":
            return self._export_to_xml(grammar)
        else:
            raise GrammarError(f"Format d'export non supporté : {format}")

    def import_grammar(self, data: str, format: str = "text") -> ContextFreeGrammar:
        """Importe une grammaire depuis un format donné.

        :param data: Données de la grammaire
        :param format: Format d'import (text, json, xml)
        :return: Grammaire importée
        :raises GrammarError: Si l'import échoue
        """
        if format == "text":
            return self.parse_grammar(data)
        elif format == "json":
            return self.from_dict(json.loads(data))
        elif format == "xml":
            return self._import_from_xml(data)
        else:
            raise GrammarError(f"Format d'import non supporté : {format}")

    def to_string(self, grammar: ContextFreeGrammar) -> str:
        """Convertit une grammaire en chaîne de caractères.

        :param grammar: Grammaire à convertir
        :return: Représentation textuelle de la grammaire
        """
        return str(grammar)

    def _export_to_xml(self, grammar: ContextFreeGrammar) -> str:
        """Exporte une grammaire en XML.

        :param grammar: Grammaire à exporter
        :return: Représentation XML de la grammaire
        """
        xml_lines = ["<grammar>"]
        if grammar.name:
            xml_lines.append(f"  <name>{grammar.name}</name>")
        xml_lines.append(f"  <start_symbol>{grammar.start_symbol}</start_symbol>")

        xml_lines.append("  <variables>")
        for variable in sorted(grammar.variables):
            xml_lines.append(f"    <variable>{variable}</variable>")
        xml_lines.append("  </variables>")

        xml_lines.append("  <terminals>")
        for terminal in sorted(grammar.terminals):
            xml_lines.append(f"    <terminal>{terminal}</terminal>")
        xml_lines.append("  </terminals>")

        xml_lines.append("  <productions>")
        for production in sorted(
            grammar.productions, key=lambda p: (p.left_side, p.right_side)
        ):
            xml_lines.append("    <production>")
            xml_lines.append(f"      <left_side>{production.left_side}</left_side>")
            xml_lines.append("      <right_side>")
            for symbol in production.right_side:
                xml_lines.append(f"        <symbol>{symbol}</symbol>")
            xml_lines.append("      </right_side>")
            xml_lines.append("    </production>")
        xml_lines.append("  </productions>")

        xml_lines.append("</grammar>")
        return "\n".join(xml_lines)

    def _import_from_xml(self, xml_data: str) -> ContextFreeGrammar:
        """Importe une grammaire depuis XML.

        :param xml_data: Données XML de la grammaire
        :return: Grammaire importée
        """
        # Implémentation simplifiée - nécessiterait un parser XML complet
        raise GrammarError("Import XML non implémenté")

"""
Machine de Turing multi-bandes.

Ce module implémente la classe MultiTapeTM qui représente une machine de Turing
avec plusieurs bandes et des capacités de synchronisation optimisées.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict

from .tm import TM
from .multitape_configuration import MultiTapeConfiguration
from ..interfaces.multitape_turing_machine import (
    IMultiTapeTuringMachine,
    TapeHead,
)
from ..interfaces.turing_machine import TapeDirection
from ..exceptions.multitape_tm_exceptions import (
    InvalidMultiTapeTMError,
    MultiTapeTMSimulationError,
    MultiTapeTMConversionError,
    MultiTapeTMOptimizationError,
    MultiTapeTMSynchronizationError,
)


class MultiTapeTM(TM, IMultiTapeTuringMachine):
    """Machine de Turing multi-bandes avec synchronisation optimisée.

    Cette classe étend la classe TM de base avec des capacités multi-bandes,
    incluant la gestion de plusieurs bandes avec alphabets distincts,
    la synchronisation des têtes de lecture/écriture et des optimisations
    d'accès aux bandes.

    :param states: Ensemble des états de la machine
    :param alphabet: Alphabet d'entrée
    :param tape_alphabets: Alphabets de chaque bande
    :param transitions: Fonction de transition multi-bande
    :param initial_state: État initial
    :param accept_states: États d'acceptation
    :param reject_states: États de rejet
    :param blank_symbols: Symboles blancs pour chaque bande
    :param name: Nom optionnel de la machine
    :param enable_synchronization: Active la synchronisation des têtes
    :param tape_count: Nombre de bandes (auto-détecté si None)
    :raises InvalidMultiTapeTMError: Si la machine n'est pas valide
    """

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        tape_alphabets: List[Set[str]],
        transitions: Dict[
            Tuple[str, Tuple[str, ...]],
            Tuple[str, Tuple[str, ...], Tuple[TapeDirection, ...]],
        ],
        initial_state: str,
        accept_states: Set[str],
        reject_states: Set[str],
        blank_symbols: Optional[List[str]] = None,
        name: Optional[str] = None,
        enable_synchronization: bool = True,
        tape_count: Optional[int] = None,
    ) -> None:
        """Initialise une machine de Turing multi-bandes.

        :param states: Ensemble des états
        :param alphabet: Alphabet d'entrée
        :param tape_alphabets: Alphabets de chaque bande
        :param transitions: Fonction de transition multi-bande
        :param initial_state: État initial
        :param accept_states: États d'acceptation
        :param reject_states: États de rejet
        :param blank_symbols: Symboles blancs pour chaque bande
        :param name: Nom optionnel de la machine
        :param enable_synchronization: Active la synchronisation
        :param tape_count: Nombre de bandes (auto-détecté si None)
        :raises InvalidMultiTapeTMError: Si la machine n'est pas valide
        """
        # Validation des paramètres multi-bandes
        self._tape_count = tape_count or len(tape_alphabets)
        if self._tape_count != len(tape_alphabets):
            raise ValueError(
                f"Tape count ({self._tape_count}) must match "
                f"number of tape alphabets ({len(tape_alphabets)})"
            )

        # Initialisation des symboles blancs
        if blank_symbols is None:
            self._blank_symbols = ["B"] * self._tape_count
        else:
            if len(blank_symbols) != self._tape_count:
                raise ValueError(
                    f"Number of blank symbols ({len(blank_symbols)}) "
                    f"must match tape count ({self._tape_count})"
                )
            self._blank_symbols = blank_symbols

        # Validation des symboles blancs
        for i, blank_symbol in enumerate(self._blank_symbols):
            if blank_symbol not in tape_alphabets[i]:
                raise ValueError(
                    f"Blank symbol '{blank_symbol}' not in tape alphabet {i}"
                )

        # Construction de l'alphabet de bande unifié pour compatibilité avec TM
        unified_tape_alphabet = set()
        for tape_alphabet in tape_alphabets:
            unified_tape_alphabet.update(tape_alphabet)

        # Attribution des attributs spécifiques AVANT l'appel au constructeur parent
        self._tape_alphabets = tape_alphabets
        self._multi_tape_transitions = transitions
        self._enable_synchronization = enable_synchronization

        # Construction des transitions unifiées pour compatibilité
        unified_transitions = self._build_unified_transitions(transitions)

        # Appel du constructeur parent
        super().__init__(
            states,
            alphabet,
            unified_tape_alphabet,
            unified_transitions,
            initial_state,
            accept_states,
            reject_states,
            self._blank_symbols[0],
            name,
        )

        # Optimisations
        self._tape_access_cache = {}
        self._head_synchronization_cache = {}

        if enable_synchronization:
            self._build_synchronization_caches()

        # Validation de la cohérence multi-bande après initialisation complète
        # Seulement si les attributs sont définis
        if hasattr(self, '_multi_tape_transitions'):
            consistency_errors = self.validate_multi_tape_consistency()
            if consistency_errors:
                raise InvalidMultiTapeTMError(
                    f"Multi-tape consistency validation failed: {'; '.join(consistency_errors)}"
                )

    def _build_unified_transitions(
        self, multi_tape_transitions: Dict
    ) -> Dict[Tuple[str, str], Tuple[str, str, TapeDirection]]:
        """Construit les transitions unifiées pour compatibilité avec TM.

        :param multi_tape_transitions: Transitions multi-bandes
        :return: Transitions unifiées pour compatibilité avec TM
        """
        unified_transitions = {}

        for (state, tape_symbols), (
            new_state,
            write_symbols,
            directions,
        ) in multi_tape_transitions.items():
            # Utiliser le premier symbole de bande comme symbole unifié
            unified_symbol = tape_symbols[0] if tape_symbols else self._blank_symbols[0]
            unified_write_symbol = (
                write_symbols[0] if write_symbols else self._blank_symbols[0]
            )
            unified_direction = directions[0] if directions else TapeDirection.STAY

            unified_transitions[(state, unified_symbol)] = (
                new_state,
                unified_write_symbol,
                unified_direction,
            )

        return unified_transitions

    def validate_multi_tape_consistency(self) -> List[str]:
        """Valide la cohérence multi-bande de la machine.

        :return: Liste des erreurs de validation
        """
        errors = []

        # Vérifier la cohérence du nombre de bandes
        for (state, tape_symbols), (
            new_state,
            write_symbols,
            directions,
        ) in self._multi_tape_transitions.items():
            if len(tape_symbols) != self._tape_count:
                errors.append(
                    f"Transition reads from {len(tape_symbols)} tapes, "
                    f"expected {self._tape_count}"
                )
            if len(write_symbols) != self._tape_count:
                errors.append(
                    f"Transition writes to {len(write_symbols)} tapes, "
                    f"expected {self._tape_count}"
                )
            if len(directions) != self._tape_count:
                errors.append(
                    f"Transition has {len(directions)} directions, "
                    f"expected {self._tape_count}"
                )

        # Vérifier la cohérence des alphabets
        for i, tape_alphabet in enumerate(self._tape_alphabets):
            if not tape_alphabet:
                errors.append(f"Tape alphabet {i} cannot be empty")

            # Vérifier que les symboles des transitions sont dans l'alphabet approprié
            for (state, tape_symbols), (
                new_state,
                write_symbols,
                directions,
            ) in self._multi_tape_transitions.items():
                if i < len(tape_symbols) and tape_symbols[i] not in tape_alphabet:
                    errors.append(
                        f"Transition reads symbol '{tape_symbols[i]}' "
                        f"not in tape alphabet {i}"
                    )
                if i < len(write_symbols) and write_symbols[i] not in tape_alphabet:
                    errors.append(
                        f"Transition writes symbol '{write_symbols[i]}' "
                        f"not in tape alphabet {i}"
                    )

        return errors

    @property
    def tape_count(self) -> int:
        """Nombre de bandes.

        :return: Nombre de bandes de la machine
        """
        return self._tape_count

    @property
    def tape_alphabets(self) -> List[Set[str]]:
        """Alphabets de chaque bande.

        :return: Liste des alphabets pour chaque bande
        """
        return [alphabet.copy() for alphabet in self._tape_alphabets]

    @property
    def blank_symbols(self) -> List[str]:
        """Symboles blancs de chaque bande.

        :return: Liste des symboles blancs pour chaque bande
        """
        return self._blank_symbols.copy()

    @property
    def synchronization_enabled(self) -> bool:
        """Indique si la synchronisation est activée.

        :return: True si la synchronisation est activée
        """
        return self._enable_synchronization

    @property
    def cache_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache.

        :return: Statistiques des caches d'optimisation
        """
        if not self._enable_synchronization:
            return {"enabled": False}

        return {
            "enabled": True,
            "state_tape_access_cache_size": len(self._tape_access_cache),
            "head_position_cache_size": len(self._head_synchronization_cache),
        }

    def simulate_multi_tape(
        self, input_strings: List[str], max_steps: int = 10000
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """Simule l'exécution multi-bande de la machine.

        :param input_strings: Chaînes d'entrée pour chaque bande
        :param max_steps: Nombre maximum d'étapes
        :return: Tuple (accepté, trace_d_exécution)
        :raises MultiTapeTMSimulationError: En cas d'erreur de simulation
        """
        trace = []

        try:
            # Validation des entrées
            if len(input_strings) != self._tape_count:
                raise ValueError(
                    f"Expected {self._tape_count} input strings, "
                    f"got {len(input_strings)}"
                )

            # Initialisation des bandes
            tapes = list(input_strings)
            head_positions = [0] * self._tape_count
            current_state = self._initial_state
            step_count = 0

            # Configuration initiale
            config = MultiTapeConfiguration(
                current_state, tapes, head_positions, step_count
            )
            trace.append(config.to_dict())

            # Simulation multi-bande
            while step_count < max_steps:
                # Vérification des états d'arrêt
                if current_state in self._accept_states:
                    config = MultiTapeConfiguration(
                        current_state,
                        tapes,
                        head_positions,
                        step_count,
                        is_accepting=True,
                    )
                    trace.append(config.to_dict())
                    return True, trace

                if current_state in self._reject_states:
                    config = MultiTapeConfiguration(
                        current_state,
                        tapes,
                        head_positions,
                        step_count,
                        is_rejecting=True,
                    )
                    trace.append(config.to_dict())
                    return False, trace

                # Lecture des symboles sous toutes les têtes
                tape_symbols = self.get_tape_symbols(tapes, head_positions)

                # Recherche de la transition
                transition_key = (current_state, tuple(tape_symbols))
                if transition_key not in self._multi_tape_transitions:
                    # Pas de transition définie - rejet
                    config = MultiTapeConfiguration(
                        current_state,
                        tapes,
                        head_positions,
                        step_count,
                        is_rejecting=True,
                    )
                    trace.append(config.to_dict())
                    return False, trace

                # Application de la transition
                (
                    new_state,
                    write_symbols,
                    directions,
                ) = self._multi_tape_transitions[transition_key]

                # Mise à jour de toutes les bandes
                for i in range(self._tape_count):
                    tapes[i] = self._write_to_tape(
                        tapes[i], head_positions[i], write_symbols[i], i
                    )
                    head_positions[i] = self._move_head(
                        head_positions[i], directions[i]
                    )

                # Synchronisation des têtes si activée
                if self._enable_synchronization:
                    heads = [TapeHead(i, pos) for i, pos in enumerate(head_positions)]
                    synchronized_heads = self.synchronize_heads(heads)
                    head_positions = [head.position for head in synchronized_heads]

                # Mise à jour de l'état
                current_state = new_state
                step_count += 1

                # Enregistrement de la configuration
                config = MultiTapeConfiguration(
                    current_state, tapes, head_positions, step_count
                )
                trace.append(config.to_dict())

            # Timeout - considéré comme rejet
            config = MultiTapeConfiguration(
                current_state, tapes, head_positions, step_count, is_rejecting=True
            )
            trace.append(config.to_dict())
            return False, trace

        except Exception as e:
            # Utiliser step_count s'il est défini, sinon 0
            error_step_count = step_count if 'step_count' in locals() else 0
            raise MultiTapeTMSimulationError(
                f"Multi-tape simulation failed: {e}", error_step_count
            ) from e

    def get_tape_symbols(
        self, tape_configurations: List[str], head_positions: List[int]
    ) -> List[str]:
        """Récupère les symboles sous toutes les têtes.

        :param tape_configurations: Configurations des bandes
        :param head_positions: Positions des têtes
        :return: Liste des symboles sous chaque tête
        """
        symbols = []
        for i, (tape, position) in enumerate(zip(tape_configurations, head_positions)):
            if 0 <= position < len(tape):
                symbols.append(tape[position])
            else:
                symbols.append(self._blank_symbols[i])
        return symbols

    def _write_to_tape(
        self, tape: str, position: int, symbol: str, tape_id: int = 0
    ) -> str:
        """Écrit un symbole à une position donnée sur une bande spécifique.

        :param tape: Contenu actuel de la bande
        :param position: Position où écrire
        :param symbol: Symbole à écrire
        :param tape_id: Identifiant de la bande
        :return: Nouveau contenu de la bande
        """
        if 0 <= position < len(tape):
            return tape[:position] + symbol + tape[position + 1 :]
        if position == len(tape):
            return tape + symbol
        # Position négative - étendre la bande vers la gauche
        padding = self._blank_symbols[tape_id] * (-position - 1)
        return padding + symbol + tape

    def _move_head(self, position: int, direction: TapeDirection) -> int:
        """Déplace une tête selon la direction.

        :param position: Position actuelle de la tête
        :param direction: Direction de déplacement
        :return: Nouvelle position de la tête
        """
        if direction == TapeDirection.LEFT:
            return position - 1
        if direction == TapeDirection.RIGHT:
            return position + 1
        # STAY
        return position

    def synchronize_heads(self, heads: List[TapeHead]) -> List[TapeHead]:
        """Synchronise les positions des têtes.

        :param heads: Liste des têtes à synchroniser
        :return: Liste des têtes synchronisées
        :raises MultiTapeTMSynchronizationError: En cas d'erreur de synchronisation
        """
        if not self._enable_synchronization:
            return heads

        try:
            # Cache de synchronisation
            head_key = tuple((head.tape_id, head.position) for head in heads)
            if head_key in self._head_synchronization_cache:
                return self._head_synchronization_cache[head_key]

            # Algorithme de synchronisation simple : aligner sur la position minimale
            min_position = min(head.position for head in heads)
            synchronized_heads = []

            for head in heads:
                synchronized_head = TapeHead(head.tape_id, min_position)
                synchronized_heads.append(synchronized_head)

            # Cache du résultat
            self._head_synchronization_cache[head_key] = synchronized_heads
            return synchronized_heads

        except Exception as e:
            raise MultiTapeTMSynchronizationError(
                f"Head synchronization failed: {e}",
                [head.tape_id for head in heads],
            ) from e

    def convert_to_single_tape(self) -> TM:
        """Convertit la machine multi-bande en machine à bande unique.

        :return: Machine de Turing à bande unique équivalente
        :raises MultiTapeTMConversionError: Si la conversion échoue
        """
        try:
            # Construction de l'alphabet de la bande unique
            # Utiliser des symboles spéciaux pour séparer les bandes
            separator_symbol = "#"
            track_symbols = set()

            # Collecter tous les symboles de toutes les bandes
            for tape_alphabet in self._tape_alphabets:
                track_symbols.update(tape_alphabet)

            # Ajouter le symbole séparateur
            single_tape_alphabet = track_symbols | {separator_symbol}

            # Construction des états étendus
            extended_states = set(self._states)
            for state in self._states:
                extended_states.add(f"{state}_track")

            # Construction des transitions
            single_tape_transitions = {}

            for (state, tape_symbols), (
                new_state,
                write_symbols,
                directions,
            ) in self._multi_tape_transitions.items():
                # Créer une transition qui simule toutes les bandes sur une seule bande
                # Format: [symbole_bande_1, symbole_bande_2, ..., symbole_bande_n]
                combined_symbol = separator_symbol.join(tape_symbols)
                combined_write_symbol = separator_symbol.join(write_symbols)

                # Déterminer la direction principale (utiliser la direction de la première bande)
                main_direction = directions[0] if directions else TapeDirection.STAY

                single_tape_transitions[(state, combined_symbol)] = (
                    new_state,
                    combined_write_symbol,
                    main_direction,
                )

            # Créer la machine à bande unique avec validation désactivée temporairement
            # car les symboles combinés ne sont pas dans l'alphabet d'entrée
            tm = TM.__new__(TM)
            tm._states = extended_states.copy()
            tm._alphabet = self._alphabet.copy()
            tm._tape_alphabet = single_tape_alphabet.copy()
            tm._transitions = single_tape_transitions.copy()
            tm._initial_state = self._initial_state
            tm._accept_states = self._accept_states.copy()
            tm._reject_states = self._reject_states.copy()
            tm._blank_symbol = self._blank_symbols[0]
            tm._name = f"{self._name}_single_tape"
            return tm

        except Exception as e:
            raise MultiTapeTMConversionError(
                f"Failed to convert multi-tape TM to single-tape: {e}"
            ) from e

    def _build_synchronization_caches(self) -> None:
        """Construit les caches pour l'optimisation de synchronisation."""
        # Cache des accès aux bandes par état
        self._state_tape_access_cache = defaultdict(dict)

        for (state, tape_symbols), (
            new_state,
            write_symbols,
            directions,
        ) in self._multi_tape_transitions.items():
            # Indexer par état et combinaison de symboles
            symbol_key = tuple(tape_symbols)
            self._state_tape_access_cache[state][symbol_key] = (
                new_state,
                write_symbols,
                directions,
            )

        # Cache des positions de tête fréquentes
        self._head_position_cache = {}

        # Cache des synchronisations de têtes
        self._head_synchronization_cache = {}

    def optimize_tape_access(self) -> "MultiTapeTM":
        """Optimise l'accès aux bandes.

        :return: Nouvelle MultiTapeTM optimisée
        :raises MultiTapeTMOptimizationError: Si l'optimisation échoue
        """
        try:
            # Réorganisation des transitions par fréquence d'accès aux bandes
            optimized_transitions = {}

            # Analyser la fréquence d'accès à chaque bande
            tape_access_frequency = defaultdict(int)
            for (_, tape_symbols), _ in self._multi_tape_transitions.items():
                for i, _ in enumerate(tape_symbols):
                    tape_access_frequency[i] += 1

            # Réorganiser les transitions pour optimiser l'accès aux bandes les plus utilisées
            for (state, tape_symbols), (
                new_state,
                write_symbols,
                directions,
            ) in self._multi_tape_transitions.items():
                optimized_transitions[(state, tape_symbols)] = (
                    new_state,
                    write_symbols,
                    directions,
                )

            return MultiTapeTM(
                states=self._states,
                alphabet=self._alphabet,
                tape_alphabets=self._tape_alphabets,
                transitions=optimized_transitions,
                initial_state=self._initial_state,
                accept_states=self._accept_states,
                reject_states=self._reject_states,
                blank_symbols=self._blank_symbols,
                name=f"{self._name}_optimized",
                enable_synchronization=True,
                tape_count=self._tape_count,
            )

        except Exception as e:
            raise MultiTapeTMOptimizationError(
                f"Failed to optimize multi-tape TM: {e}"
            ) from e

    def validate(self) -> List[str]:
        """Valide la cohérence de la machine multi-bande.

        :return: Liste des erreurs de validation
        """
        errors = super().validate()

        # Validation spécifique multi-bande
        multi_tape_errors = self.validate_multi_tape_consistency()
        errors.extend(multi_tape_errors)

        # Validation des optimisations
        if self._enable_synchronization:
            optimization_errors = self._validate_synchronization_optimizations()
            errors.extend(optimization_errors)

        return errors

    def _validate_synchronization_optimizations(self) -> List[str]:
        """Valide les optimisations de synchronisation.

        :return: Liste des erreurs de validation
        """
        errors = []

        # Vérifier la cohérence du cache
        if hasattr(self, "_state_tape_access_cache"):
            for state, _ in self._state_tape_access_cache.items():
                if state not in self._states:
                    errors.append(f"Cache references unknown state '{state}'")

        return errors

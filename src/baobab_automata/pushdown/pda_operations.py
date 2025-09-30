"""
Opérations sur les langages pour les automates à pile non-déterministes (PDA).

Ce module implémente les opérations de base sur les langages reconnus par les PDA :
union, concaténation, étoile de Kleene, etc.
"""

from typing import TYPE_CHECKING

from .pda_exceptions import PDAOperationError

if TYPE_CHECKING:
    from .pda import PDA


class PDAOperations:
    """Classe utilitaire pour les opérations sur les langages des PDA."""

    @staticmethod
    def union(pda1: "PDA", pda2: "PDA") -> "PDA":
        """Crée l'union de deux PDA.

        L'union de deux PDA reconnaît tous les mots reconnus par au moins
        un des deux automates.

        :param pda1: Premier PDA
        :param pda2: Deuxième PDA
        :return: PDA reconnaissant l'union des langages
        :raises PDAOperationError: Si les PDA ne sont pas compatibles
        """
        try:
            # Vérification de la compatibilité des alphabets
            if pda1.input_alphabet != pda2.input_alphabet:
                raise PDAOperationError(
                    "union",
                    f"Alphabets d'entrée incompatibles: {pda1.input_alphabet} vs {pda2.input_alphabet}",
                )

            # Création des nouveaux états
            new_states = set()
            new_states.add("q0_union")  # Nouvel état initial
            new_states.add("qf_union")  # Nouvel état final

            # Renommage des états pour éviter les conflits
            pda1_states = {f"pda1_{state}" for state in pda1.states}
            pda2_states = {f"pda2_{state}" for state in pda2.states}
            new_states.update(pda1_states)
            new_states.update(pda2_states)

            # Nouvel alphabet de pile (union des deux alphabets)
            new_stack_alphabet = pda1.stack_alphabet | pda2.stack_alphabet
            new_stack_alphabet.add("Z_union")  # Nouveau symbole de fond de pile

            # Nouvelles transitions
            new_transitions = {}

            # Transitions depuis le nouvel état initial vers les états initiaux des PDA
            new_transitions[("q0_union", "", "Z_union")] = {
                (f"pda1_{pda1.initial_state}", "Z_union" + pda1.initial_stack_symbol),
                (f"pda2_{pda2.initial_state}", "Z_union" + pda2.initial_stack_symbol),
            }

            # Copie des transitions du premier PDA
            for (
                state,
                input_sym,
                stack_sym,
            ), destinations in pda1._transitions.items():
                new_state = f"pda1_{state}"
                new_stack_sym = (
                    "Z_union" + stack_sym
                    if stack_sym == pda1.initial_stack_symbol
                    else stack_sym
                )

                new_destinations = set()
                for dest_state, stack_symbols in destinations:
                    new_dest_state = f"pda1_{dest_state}"
                    new_stack_symbols = stack_symbols
                    if stack_symbols == pda1.initial_stack_symbol:
                        new_stack_symbols = "Z_union" + stack_symbols
                    new_destinations.add((new_dest_state, new_stack_symbols))

                new_transitions[(new_state, input_sym, new_stack_sym)] = (
                    new_destinations
                )

            # Copie des transitions du deuxième PDA
            for (
                state,
                input_sym,
                stack_sym,
            ), destinations in pda2._transitions.items():
                new_state = f"pda2_{state}"
                new_stack_sym = (
                    "Z_union" + stack_sym
                    if stack_sym == pda2.initial_stack_symbol
                    else stack_sym
                )

                new_destinations = set()
                for dest_state, stack_symbols in destinations:
                    new_dest_state = f"pda2_{dest_state}"
                    new_stack_symbols = stack_symbols
                    if stack_symbols == pda2.initial_stack_symbol:
                        new_stack_symbols = "Z_union" + stack_symbols
                    new_destinations.add((new_dest_state, new_stack_symbols))

                new_transitions[(new_state, input_sym, new_stack_sym)] = (
                    new_destinations
                )

            # Transitions des états finaux vers le nouvel état final
            for final_state in pda1.final_states:
                new_final = f"pda1_{final_state}"
                new_transitions[(new_final, "", "Z_union")] = {("qf_union", "Z_union")}

            for final_state in pda2.final_states:
                new_final = f"pda2_{final_state}"
                new_transitions[(new_final, "", "Z_union")] = {("qf_union", "Z_union")}

            # Import dynamique pour éviter l'importation circulaire
            from .pda import PDA

            return PDA(
                states=new_states,
                input_alphabet=pda1.input_alphabet,
                stack_alphabet=new_stack_alphabet,
                transitions=new_transitions,
                initial_state="q0_union",
                initial_stack_symbol="Z_union",
                final_states={"qf_union"},
                name=f"union_{pda1.name or 'pda1'}_{pda2.name or 'pda2'}",
            )

        except Exception as e:
            raise PDAOperationError("union", f"Erreur lors de l'union: {e}")

    @staticmethod
    def concatenation(pda1: "PDA", pda2: "PDA") -> "PDA":
        """Crée la concaténation de deux PDA.

        La concaténation de deux PDA reconnaît tous les mots de la forme
        w1w2 où w1 est reconnu par le premier PDA et w2 par le deuxième.

        :param pda1: Premier PDA
        :param pda2: Deuxième PDA
        :return: PDA reconnaissant la concaténation des langages
        :raises PDAOperationError: Si les PDA ne sont pas compatibles
        """
        try:
            # Vérification de la compatibilité des alphabets
            if pda1.input_alphabet != pda2.input_alphabet:
                raise PDAOperationError(
                    "concatenation",
                    f"Alphabets d'entrée incompatibles: {pda1.input_alphabet} vs {pda2.input_alphabet}",
                )

            # Création des nouveaux états
            new_states = set()
            new_states.add("q0_concat")  # Nouvel état initial

            # Renommage des états pour éviter les conflits
            pda1_states = {f"pda1_{state}" for state in pda1.states}
            pda2_states = {f"pda2_{state}" for state in pda2.states}
            new_states.update(pda1_states)
            new_states.update(pda2_states)

            # Nouvel alphabet de pile
            new_stack_alphabet = pda1.stack_alphabet | pda2.stack_alphabet
            new_stack_alphabet.add("Z_concat")

            # Nouvelles transitions
            new_transitions = {}

            # Transition depuis le nouvel état initial vers l'état initial du premier PDA
            new_transitions[("q0_concat", "", "Z_concat")] = {
                (f"pda1_{pda1.initial_state}", "Z_concat" + pda1.initial_stack_symbol)
            }

            # Copie des transitions du premier PDA
            for (
                state,
                input_sym,
                stack_sym,
            ), destinations in pda1._transitions.items():
                new_state = f"pda1_{state}"
                new_stack_sym = (
                    "Z_concat" + stack_sym
                    if stack_sym == pda1.initial_stack_symbol
                    else stack_sym
                )

                new_destinations = set()
                for dest_state, stack_symbols in destinations:
                    new_dest_state = f"pda1_{dest_state}"
                    new_stack_symbols = stack_symbols
                    if stack_symbols == pda1.initial_stack_symbol:
                        new_stack_symbols = "Z_concat" + stack_symbols
                    new_destinations.add((new_dest_state, new_stack_symbols))

                new_transitions[(new_state, input_sym, new_stack_sym)] = (
                    new_destinations
                )

            # Transitions des états finaux du premier PDA vers l'état initial du deuxième
            for final_state in pda1.final_states:
                new_final = f"pda1_{final_state}"
                new_transitions[(new_final, "", "Z_concat")] = {
                    (
                        f"pda2_{pda2.initial_state}",
                        "Z_concat" + pda2.initial_stack_symbol,
                    )
                }

            # Copie des transitions du deuxième PDA
            for (
                state,
                input_sym,
                stack_sym,
            ), destinations in pda2._transitions.items():
                new_state = f"pda2_{state}"
                new_stack_sym = (
                    "Z_concat" + stack_sym
                    if stack_sym == pda2.initial_stack_symbol
                    else stack_sym
                )

                new_destinations = set()
                for dest_state, stack_symbols in destinations:
                    new_dest_state = f"pda2_{dest_state}"
                    new_stack_symbols = stack_symbols
                    if stack_symbols == pda2.initial_stack_symbol:
                        new_stack_symbols = "Z_concat" + stack_symbols
                    new_destinations.add((new_dest_state, new_stack_symbols))

                new_transitions[(new_state, input_sym, new_stack_sym)] = (
                    new_destinations
                )

            # Les états finaux sont ceux du deuxième PDA
            new_final_states = {f"pda2_{state}" for state in pda2.final_states}

            # Import dynamique pour éviter l'importation circulaire
            from .pda import PDA

            return PDA(
                states=new_states,
                input_alphabet=pda1.input_alphabet,
                stack_alphabet=new_stack_alphabet,
                transitions=new_transitions,
                initial_state="q0_concat",
                initial_stack_symbol="Z_concat",
                final_states=new_final_states,
                name=f"concat_{pda1.name or 'pda1'}_{pda2.name or 'pda2'}",
            )

        except Exception as e:
            raise PDAOperationError(
                "concatenation", f"Erreur lors de la concaténation: {e}"
            )

    @staticmethod
    def kleene_star(pda: "PDA") -> "PDA":
        """Crée l'étoile de Kleene d'un PDA.

        L'étoile de Kleene d'un PDA reconnaît tous les mots de la forme
        w1w2...wn où chaque wi est reconnu par le PDA original (n >= 0).

        :param pda: PDA original
        :return: PDA reconnaissant l'étoile de Kleene du langage
        :raises PDAOperationError: Si l'opération échoue
        """
        try:
            # Création des nouveaux états
            new_states = set()
            new_states.add("q0_star")  # Nouvel état initial
            new_states.add("qf_star")  # Nouvel état final

            # Renommage des états du PDA original
            pda_states = {f"pda_{state}" for state in pda.states}
            new_states.update(pda_states)

            # Nouvel alphabet de pile
            new_stack_alphabet = pda.stack_alphabet.copy()
            new_stack_alphabet.add("Z_star")

            # Nouvelles transitions
            new_transitions = {}

            # Transition depuis le nouvel état initial vers l'état initial du PDA
            new_transitions[("q0_star", "", "Z_star")] = {
                (f"pda_{pda.initial_state}", "Z_star" + pda.initial_stack_symbol)
            }

            # Transition depuis le nouvel état initial vers l'état final (mot vide)
            new_transitions[("q0_star", "", "Z_star")] = {("qf_star", "Z_star")}

            # Copie des transitions du PDA original
            for (state, input_sym, stack_sym), destinations in pda._transitions.items():
                new_state = f"pda_{state}"
                new_stack_sym = (
                    "Z_star" + stack_sym
                    if stack_sym == pda.initial_stack_symbol
                    else stack_sym
                )

                new_destinations = set()
                for dest_state, stack_symbols in destinations:
                    new_dest_state = f"pda_{dest_state}"
                    new_stack_symbols = stack_symbols
                    if stack_symbols == pda.initial_stack_symbol:
                        new_stack_symbols = "Z_star" + stack_symbols
                    new_destinations.add((new_dest_state, new_stack_symbols))

                new_transitions[(new_state, input_sym, new_stack_sym)] = (
                    new_destinations
                )

            # Transitions des états finaux vers l'état initial (pour la répétition)
            for final_state in pda.final_states:
                new_final = f"pda_{final_state}"
                new_transitions[(new_final, "", "Z_star")] = {
                    (f"pda_{pda.initial_state}", "Z_star" + pda.initial_stack_symbol)
                }

            # Transitions des états finaux vers l'état final
            for final_state in pda.final_states:
                new_final = f"pda_{final_state}"
                new_transitions[(new_final, "", "Z_star")] = {("qf_star", "Z_star")}

            # Import dynamique pour éviter l'importation circulaire
            from .pda import PDA

            return PDA(
                states=new_states,
                input_alphabet=pda.input_alphabet,
                stack_alphabet=new_stack_alphabet,
                transitions=new_transitions,
                initial_state="q0_star",
                initial_stack_symbol="Z_star",
                final_states={"qf_star"},
                name=f"star_{pda.name or 'pda'}",
            )

        except Exception as e:
            raise PDAOperationError(
                "kleene_star", f"Erreur lors de l'étoile de Kleene: {e}"
            )

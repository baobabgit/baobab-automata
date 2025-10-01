#!/usr/bin/env python3
"""Script de débogage très détaillé pour a^n b^n."""

from src.baobab_automata.pushdown.dpda import DPDA
from src.baobab_automata.pushdown.dpda_configuration import DPDAConfiguration

def debug_anbn():
    """Débogage très détaillé pour a^n b^n."""
    dpda = DPDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'Z', 'A'},
        transitions={
            ('q0', 'a', 'Z'): ('q0', 'AZ'),
            ('q0', 'a', 'A'): ('q0', 'AA'),
            ('q0', 'b', 'A'): ('q1', ''),
            ('q1', 'b', 'A'): ('q1', ''),
            ('q1', 'b', 'Z'): ('q2', 'Z')
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q2'}
    )
    
    print("=== Test détaillé du mot 'ab' ===")
    word = 'ab'
    
    # Configuration initiale
    current_config = DPDAConfiguration(
        state='q0',
        remaining_input=word,
        stack='Z'
    )
    
    print(f"Configuration initiale: {current_config}")
    print(f"Est acceptante: {current_config.is_accepting}")
    print(f"État final: {dpda.is_final_state(current_config.state)}")
    
    step = 1
    while True:
        print(f"\n--- Étape {step} ---")
        print(f"Configuration: {current_config}")
        
        # Vérification de l'acceptation
        is_accepting = current_config.is_accepting
        is_final = dpda.is_final_state(current_config.state)
        print(f"Est acceptante: {is_accepting}")
        print(f"État final: {is_final}")
        
        if is_accepting and is_final:
            print("✓ Mot accepté !")
            break
        
        # Récupération de la transition
        input_symbol = current_config.remaining_input[0] if current_config.remaining_input else ''
        stack_symbol = current_config.stack_top
        
        print(f"Symbole d'entrée: '{input_symbol}'")
        print(f"Symbole de pile: '{stack_symbol}'")
        
        if stack_symbol is None:
            print("✗ Pile vide, mot rejeté")
            break
        
        # Recherche de transition avec symbole d'entrée
        transition = dpda.get_transition(
            current_config.state, 
            input_symbol, 
            stack_symbol
        )
        
        print(f"Transition avec symbole '{input_symbol}': {transition}")
        
        # Si pas de transition avec symbole d'entrée, chercher transition epsilon
        if transition is None:
            transition = dpda.get_transition(
                current_config.state, 
                '', 
                stack_symbol
            )
            print(f"Transition epsilon: {transition}")
        
        if transition is None:
            print("✗ Aucune transition possible, mot rejeté")
            break
        
        # Application de la transition
        new_state, stack_operation = transition
        print(f"Nouvel état: {new_state}")
        print(f"Opération de pile: '{stack_operation}'")
        
        # Mise à jour de la configuration
        if input_symbol and input_symbol != '':
            current_config = current_config.consume_input(1)
            print(f"Après consommation: {current_config}")
        
        current_config = current_config.change_state(new_state)
        print(f"Après changement d'état: {current_config}")
        
        # Gestion de la pile
        if stack_operation == '':
            # Dépilage
            current_config = current_config.pop_symbols(1)
            print(f"Après dépilage: {current_config}")
        else:
            # Remplacement du sommet
            current_config = current_config.replace_stack_top(stack_operation)
            print(f"Après remplacement: {current_config}")
        
        step += 1
        
        if step > 10:  # Protection contre les boucles infinies
            print("✗ Trop d'étapes, arrêt")
            break

if __name__ == "__main__":
    debug_anbn()
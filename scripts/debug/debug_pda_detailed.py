import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
#!/usr/bin/env python3
"""Script de debug détaillé pour tester la reconnaissance de mots par PDA."""

from src.baobab_automata.pushdown import PDA
from src.baobab_automata.pushdown.pda_configuration import PDAConfiguration
from collections import deque

def debug_pda_detailed():
    """Debug détaillé de la reconnaissance de mots par PDA."""
    # PDA pour a^n b^n
    pda = PDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'Z', 'A'},
        transitions={
            ('q0', 'a', 'Z'): {('q0', 'AZ')},
            ('q0', 'a', 'A'): {('q0', 'AA')},
            ('q0', 'b', 'A'): {('q1', '')},
            ('q1', 'b', 'A'): {('q1', '')},
            ('q1', '', 'Z'): {('q2', 'Z')}
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q2'}
    )
    
    print("=== DEBUG PDA DÉTAILLÉ ===")
    print(f"PDA: {pda}")
    print(f"Transitions: {pda._transitions}")
    
    # Test avec le mot 'ab'
    word = 'ab'
    print(f"\n=== SIMULATION DU MOT '{word}' ===")
    
    # Configuration initiale
    initial_config = PDAConfiguration(
        state=pda.initial_state,
        remaining_input=word,
        stack=pda.initial_stack_symbol
    )
    print(f"Configuration initiale: {initial_config}")
    
    # Simulation manuelle
    config_queue = deque([initial_config])
    visited_configs = set()
    step = 0
    
    while config_queue and step < 10:  # Limite pour éviter les boucles infinies
        step += 1
        print(f"\n--- Étape {step} ---")
        print(f"File de configurations: {len(config_queue)} éléments")
        
        current_config = config_queue.popleft()
        print(f"Configuration actuelle: {current_config}")
        
        # Vérification de l'acceptation
        if (current_config.remaining_input == '' and 
            pda.is_final_state(current_config.state)):
            print("✓ MOT ACCEPTÉ !")
            return True
        
        # Éviter les configurations déjà visitées
        config_key = (current_config.state, current_config.remaining_input, current_config.stack)
        if config_key in visited_configs:
            print("Configuration déjà visitée, ignorée")
            continue
        visited_configs.add(config_key)
        
        # Exploration des transitions possibles
        print(f"Exploration des transitions...")
        
        # Transition avec symbole d'entrée
        if current_config.remaining_input:
            input_symbol = current_config.remaining_input[0]
            print(f"  Symbole d'entrée: '{input_symbol}'")
            print(f"  Sommet de pile: '{current_config.stack_top}'")
            
            transitions = pda.get_transitions(
                current_config.state,
                input_symbol,
                current_config.stack_top or ''
            )
            print(f"  Transitions trouvées: {transitions}")
            
            for next_state, stack_symbols in transitions:
                print(f"    Transition vers: état={next_state}, pile={stack_symbols}")
                new_config = pda._apply_transition(current_config, next_state, stack_symbols)
                if new_config is not None:
                    print(f"    Nouvelle configuration: {new_config}")
                    config_queue.append(new_config)
                else:
                    print(f"    Transition non applicable")
        
        # Transitions epsilon
        epsilon_transitions = pda.get_transitions(
            current_config.state,
            '',  # Symbole epsilon
            current_config.stack_top or ''
        )
        print(f"  Transitions epsilon: {epsilon_transitions}")
        
        for next_state, stack_symbols in epsilon_transitions:
            print(f"    Transition epsilon vers: état={next_state}, pile={stack_symbols}")
            new_config = pda._apply_epsilon_transition(current_config, next_state, stack_symbols)
            if new_config is not None:
                print(f"    Nouvelle configuration: {new_config}")
                config_queue.append(new_config)
            else:
                print(f"    Transition epsilon non applicable")
    
    print(f"\n=== FIN DE SIMULATION ===")
    print(f"Mot non accepté après {step} étapes")
    return False

if __name__ == "__main__":
    debug_pda_detailed()
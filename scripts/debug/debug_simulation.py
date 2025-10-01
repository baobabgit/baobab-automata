import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
#!/usr/bin/env python3
"""Debug détaillé de la simulation PDA."""

from src.baobab_automata.pushdown import PDA
from src.baobab_automata.pushdown.pda_configuration import PDAConfiguration
from collections import deque

def debug_simulation():
    """Debug détaillé de la simulation."""
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
    
    print("=== DEBUG SIMULATION DÉTAILLÉ ===")
    
    # Test avec le mot 'ab'
    word = 'ab'
    print(f"Mot à tester: '{word}'")
    
    # Configuration initiale
    initial_config = PDAConfiguration(
        state=pda.initial_state,
        remaining_input=word,
        stack=pda.initial_stack_symbol
    )
    print(f"Configuration initiale: {initial_config}")
    
    # Simulation manuelle étape par étape
    config_queue = deque([initial_config])
    visited_configs = set()
    step = 0
    
    while config_queue and step < 20:
        step += 1
        print(f"\n--- ÉTAPE {step} ---")
        
        current_config = config_queue.popleft()
        print(f"Configuration actuelle: {current_config}")
        print(f"  État: {current_config.state}")
        print(f"  Mot restant: '{current_config.remaining_input}'")
        print(f"  Pile: '{current_config.stack}'")
        print(f"  Sommet de pile: '{current_config.stack_top}'")
        
        # Vérification de l'acceptation
        if current_config.remaining_input == '':
            print(f"  Mot entièrement lu")
            if pda.is_final_state(current_config.state):
                print(f"  État final: {current_config.state}")
                print("  ✓ MOT ACCEPTÉ !")
                return True
            else:
                print(f"  État non final: {current_config.state}")
        else:
            print(f"  Mot non entièrement lu")
        
        # Éviter les configurations déjà visitées
        config_key = (current_config.state, current_config.remaining_input, current_config.stack)
        if config_key in visited_configs:
            print(f"  Configuration déjà visitée, ignorée")
            continue
        visited_configs.add(config_key)
        
        # Exploration des transitions
        print(f"  Exploration des transitions...")
        
        # Transition avec symbole d'entrée
        if current_config.remaining_input:
            input_symbol = current_config.remaining_input[0]
            print(f"    Symbole d'entrée: '{input_symbol}'")
            print(f"    Sommet de pile: '{current_config.stack_top}'")
            
            transitions = pda.get_transitions(
                current_config.state,
                input_symbol,
                current_config.stack_top or ''
            )
            print(f"    Transitions trouvées: {transitions}")
            
            for next_state, stack_symbols in transitions:
                print(f"      Transition: {current_config.state} --{input_symbol},{current_config.stack_top}--> {next_state},{stack_symbols}")
                
                # Application manuelle de la transition
                try:
                    # Consommer le symbole d'entrée
                    new_config = current_config.consume_input(input_symbol)
                    print(f"        Après consommation: {new_config}")
                    
                    # Changer d'état
                    new_config = new_config.change_state(next_state)
                    print(f"        Après changement d'état: {new_config}")
                    
                    # Gestion de la pile
                    if current_config.stack_top:
                        new_config = new_config.pop_symbol()
                        print(f"        Après dépilage: {new_config}")
                    
                    if stack_symbols:
                        new_config = new_config.push_symbols(stack_symbols)
                        print(f"        Après empilage de '{stack_symbols}': {new_config}")
                    
                    print(f"        Nouvelle configuration: {new_config}")
                    config_queue.append(new_config)
                    
                except Exception as e:
                    print(f"        Erreur lors de l'application: {e}")
        
        # Transitions epsilon
        epsilon_transitions = pda.get_transitions(
            current_config.state,
            '',
            current_config.stack_top or ''
        )
        print(f"    Transitions epsilon: {epsilon_transitions}")
        
        for next_state, stack_symbols in epsilon_transitions:
            print(f"      Transition epsilon: {current_config.state} --ε,{current_config.stack_top}--> {next_state},{stack_symbols}")
            
            # Application manuelle de la transition epsilon
            try:
                new_config = current_config.change_state(next_state)
                print(f"        Après changement d'état: {new_config}")
                
                if current_config.stack_top:
                    new_config = new_config.pop_symbol()
                    print(f"        Après dépilage: {new_config}")
                
                if stack_symbols:
                    new_config = new_config.push_symbols(stack_symbols)
                    print(f"        Après empilage de '{stack_symbols}': {new_config}")
                
                print(f"        Nouvelle configuration: {new_config}")
                config_queue.append(new_config)
                
            except Exception as e:
                print(f"        Erreur lors de l'application epsilon: {e}")
    
    print(f"\n=== FIN DE SIMULATION ===")
    print(f"Mot non accepté après {step} étapes")
    return False

if __name__ == "__main__":
    debug_simulation()
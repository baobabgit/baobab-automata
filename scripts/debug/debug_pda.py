import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
#!/usr/bin/env python3
"""Script de debug pour tester la reconnaissance de mots par PDA."""

from src.baobab_automata.pushdown import PDA

def debug_pda():
    """Debug de la reconnaissance de mots par PDA."""
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
    
    print("PDA créé:")
    print(f"  États: {pda.states}")
    print(f"  Alphabet d'entrée: {pda.input_alphabet}")
    print(f"  Alphabet de pile: {pda.stack_alphabet}")
    print(f"  État initial: {pda.initial_state}")
    print(f"  Symbole initial de pile: {pda.initial_stack_symbol}")
    print(f"  États finaux: {pda.final_states}")
    print(f"  Transitions: {pda._transitions}")
    
    # Test avec le mot 'ab'
    word = 'ab'
    print(f"\nTest avec le mot '{word}':")
    
    # Configuration initiale
    from src.baobab_automata.pushdown.pda_configuration import PDAConfiguration
    initial_config = PDAConfiguration(
        state=pda.initial_state,
        remaining_input=word,
        stack=pda.initial_stack_symbol
    )
    print(f"  Configuration initiale: {initial_config}")
    
    # Test des transitions possibles
    print(f"\nTransitions possibles depuis q0 avec 'a' et pile 'Z':")
    transitions = pda.get_transitions('q0', 'a', 'Z')
    print(f"  {transitions}")
    
    print(f"\nTransitions possibles depuis q0 avec '' et pile 'Z':")
    epsilon_transitions = pda.get_transitions('q0', '', 'Z')
    print(f"  {epsilon_transitions}")
    
    # Test de reconnaissance
    result = pda.accepts(word)
    print(f"\nRésultat de la reconnaissance: {result}")

if __name__ == "__main__":
    debug_pda()
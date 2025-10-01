import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
#!/usr/bin/env python3
"""Script de débogage pour les DPDA."""

from src.baobab_automata.pushdown.dpda import DPDA

def test_dpda():
    """Test simple d'un DPDA."""
    dpda = DPDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'Z', 'A'},
        transitions={
            ('q0', 'a', 'Z'): ('q0', 'AZ'),
            ('q0', 'a', 'A'): ('q0', 'AA'),
            ('q0', 'b', 'A'): ('q1', ''),
            ('q1', 'b', 'A'): ('q1', ''),
            ('q1', 'b', 'Z'): ('q2', 'Z')  # Transition directe sans epsilon
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q2'}
    )
    
    print("DPDA créé avec succès")
    print(f"États: {dpda.states}")
    print(f"Alphabet d'entrée: {dpda.input_alphabet}")
    print(f"Alphabet de pile: {dpda.stack_alphabet}")
    print(f"État initial: {dpda.initial_state}")
    print(f"Symbole initial de pile: {dpda.initial_stack_symbol}")
    print(f"États finaux: {dpda.final_states}")
    print(f"Transitions: {dpda._transitions}")
    
    # Test de reconnaissance
    test_words = ['ab', 'aabb', 'aaabbb', 'a', 'b', 'abab']
    
    for word in test_words:
        result = dpda.accepts(word)
        print(f"Mot '{word}': {'Accepté' if result else 'Rejeté'}")

if __name__ == "__main__":
    test_dpda()
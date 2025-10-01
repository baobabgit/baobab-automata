#!/usr/bin/env python3
"""Script de débogage avec un DPDA qui fonctionne."""

from src.baobab_automata.pushdown.dpda import DPDA

def test_working_dpda():
    """Test avec un DPDA qui fonctionne pour a^n b^n."""
    # DPDA pour reconnaître a^n b^n
    dpda = DPDA(
        states={'q0', 'q1', 'q2'},
        input_alphabet={'a', 'b'},
        stack_alphabet={'Z', 'A'},
        transitions={
            ('q0', 'a', 'Z'): ('q0', 'AZ'),  # Empiler A pour chaque a
            ('q0', 'a', 'A'): ('q0', 'AA'),  # Empiler A pour chaque a
            ('q0', 'b', 'A'): ('q1', ''),    # Dépiler A pour chaque b
            ('q1', 'b', 'A'): ('q1', ''),    # Dépiler A pour chaque b
            ('q1', 'b', 'Z'): ('q2', 'Z')    # Transition directe vers état final
        },
        initial_state='q0',
        initial_stack_symbol='Z',
        final_states={'q2'}
    )
    
    print("=== Test du DPDA pour a^n b^n ===")
    test_words = ['ab', 'aabb', 'aaabbb', 'a', 'b', 'abab', '']
    
    for word in test_words:
        result = dpda.accepts(word)
        print(f"Mot '{word}': {'Accepté' if result else 'Rejeté'}")

if __name__ == "__main__":
    test_working_dpda()